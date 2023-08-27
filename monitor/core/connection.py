import paramiko
import time


class SSHConnector:
    def __init__(self, hostname, port, username, password, name='unknown'):
        self.name = name
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=hostname, port=port, username=username, password=password)
        self.channel = self.client.get_transport().open_session()

    def close(self):
        self.client.close()


class SSHExecutor:
    def __init__(self, connector, command, repeat=False, interval=0.5):
        self.connector = connector
        self.command = command
        self.repeat = repeat
        self.interval = interval

    def execute(self):
        if self.repeat:
            self.command = f'for i in {{1..20}}; do {self.command}; sleep {self.interval}; done'
        self.connector.channel.exec_command(self.command)


class SSHOutputProcessor:
    def __init__(self, connector, name='unknown'):
        self.connector = connector
        self.name = name
        self.output_buffer = []

    def _flush_output(self, lines, flush_fn):
        flush_fn(self.name, lines)
        self.output_buffer.extend(lines)

    def read_output(self, flush_fn=print):
        channel = self.connector.channel
        buffer = ''
        while True:
            self._read_from_channel(channel, buffer, flush_fn)
            if channel.exit_status_ready():
                self._read_from_channel(channel, buffer, flush_fn, exit_ready=True)
                break
            time.sleep(1)
        print(f"Exit status: {channel.recv_exit_status()}")

    def _read_from_channel(self, channel, buffer, flush_fn, exit_ready=False):
        if channel.recv_ready() or exit_ready:
            buffer += channel.recv(1024).decode('utf-8')
            lines = buffer.split('\n')
            if len(lines) > 1:
                self._flush_output(lines[:-1], flush_fn)
                buffer = lines[-1]
