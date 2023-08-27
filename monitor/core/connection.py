import time
import paramiko
import threading


class SSHConnectionManager:
    def __init__(self, hostname, port, username, password):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=hostname, port=port, username=username, password=password)
        self.channel = self.client.get_transport().open_session()
        self.output_buffer = []

    def execute(self, command, repeat=False, interval=0.5):
        if repeat:
            command = 'for i in {{1..20}}; do {}; sleep {}; done'.format(command, str(interval))
        try:
            self.channel.exec_command(command)
            self.read_output(self.channel)
        finally:
            self.close()

    def _process_buffer(self, buffer, flush_fn=print):
        lines = buffer.split('\n')
        if len(lines) > 1:
            flush_fn(lines[:-1])
            self.output_buffer += lines[:-1]
            return lines[-1]
        return buffer

    def read_output(self, channel):
        buffer = ''
        while True:
            if channel.recv_ready():
                buffer += channel.recv(1024).decode('utf-8')
                buffer = self._process_buffer(buffer)

            if channel.exit_status_ready():
                if channel.recv_ready():
                    buffer += channel.recv(1024).decode('utf-8')
                    self._process_buffer(buffer)
                break

            time.sleep(1)  # 3초 대기

        exit_status = channel.recv_exit_status()
        print(f"Exit status: {exit_status}")

    def close(self):
        self.client.close()


if __name__ == '__main__':
    from monitor.models import NodeInfo
    nodes = [
        NodeInfo(name='node01', hostname="172.28.201.169", port=10001, username='root', password='qwer1234'),
        NodeInfo(name='node02', hostname="172.28.201.169", port=10002, username='root', password='qwer1234'),
    ]
    script = """for i in {1..20}; do uptime; sleep 0.2; done;"""

    conn_manager = SSHConnectionManager(nodes[0].hostname, nodes[0].port, nodes[0].username, nodes[0].password)
    conn_manager.execute('uptime', repeat=False)

    threads = []
    for node in nodes:
        t = threading.Thread(target=execute_ssh_command, args=(node,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
