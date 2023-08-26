# monitor/core/utils.py

import paramiko


class SSHConnection:
    def __init__(self, host, username, password):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, username=username, password=password)

    def execute(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read()

    def close(self):
        self.client.close()


class CommandInvoker:
    def __init__(self, ssh_connection, strategy):
        self.ssh_connection = ssh_connection
        self.strategy = strategy

    def execute(self, metric):
        command, parser = metric
        result = self.ssh_connection.execute(command)
        return parser(result)


class ExecutionManager:
    def __init__(self, strategy):
        self.strategy = strategy

    def execute(self, nodes, command):
        for node in nodes:
            ssh_conn = SSHConnection(node['address'], node['username'], node['password'])
            invoker = CommandInvoker(ssh_conn, self.strategy)
            result = invoker.execute(command)
            print(result)
