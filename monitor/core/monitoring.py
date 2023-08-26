# monitor/core/monitoring.py

from .connection import SSHConnection, CommandInvoker
from .metrics import Metric


class ExecutionManager:
    def __init__(self, strategy):
        self.strategy = strategy

    def execute(self, nodes, command):
        for node in nodes:
            ssh_conn = SSHConnection(node['address'], node['username'], node['password'])
            invoker = CommandInvoker(ssh_conn, self.strategy)
            result = invoker.execute(command)
            print(result)



