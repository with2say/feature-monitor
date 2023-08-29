import time
import paramiko

from monitor.settings import USERNAME, PRIVATE_KEY, SSH_STREAM_READ_INTERVAL, SSH_COMMAND_SEND_INTERVAL


class SSHConnector:
    def __init__(self, hostname, port, username=USERNAME, name='unknown'):
        self.name = name
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey(filename=PRIVATE_KEY)
        self.client.connect(hostname=hostname, port=port, username=username, pkey=private_key)
        self.channel = self.client.get_transport().open_session()

    def close(self):
        self.client.close()


class SSHExecutor:
    def __init__(self, connector, command, repeat=False, interval=SSH_COMMAND_SEND_INTERVAL):
        self.connector = connector
        self.command = command
        self.repeat = repeat
        self.interval = interval

    def execute(self):
        if self.repeat:
            self.command = f'for i in {{1..50}}; do {self.command}; sleep {self.interval}; done'
        self.connector.channel.exec_command(self.command)


class SSHOutputProcessor:
    def __init__(self, connector, name='unknown', flush_output_callback=None):
        self.connector = connector
        self.name = name
        self.flush_output_callback = flush_output_callback or print

    def read_output(self):
        channel = self.connector.channel
        buffer = ''
        while True:
            buffer = self._read_from_channel(channel, buffer)
            if channel.exit_status_ready():
                self._read_from_channel(channel, buffer, exit_ready=True)
                break
            time.sleep(SSH_STREAM_READ_INTERVAL)
        print(f"Exit {self.name} ({channel.recv_exit_status()})")

    def _read_from_channel(self, channel, buffer, exit_ready=False):
        if channel.recv_ready() or exit_ready:
            buffer += channel.recv(1024).decode('utf-8')
            lines = buffer.split('\n')
            if len(lines) > 1:
                self.flush_output_callback(self.name, lines[:-1])
                buffer = lines[-1]
        return buffer
