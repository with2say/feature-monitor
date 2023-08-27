# monitor/core/monitoring.py

from .connection import SSHConnectionManager
from .concurrency_strategy import OneThreadPerTaskStrategy
from .metrics import Metric


class ExecutionManager:
    def __init__(self, strategy):
        self.strategy = strategy

    def run(self, nodes, command):


    def execute(self, nodes, command):
        OneThreadPerTaskStrategy().execute()

        for node in nodes:
            conn_manager = SSHConnectionManager(
                node.hostname,
                node.port,
                node.username,
                node.password
            )
            conn_manager.execute('uptime', repeat=False)


            threads = []
            for node in nodes:
                t = threading.Thread(target=execute_ssh_command, args=(node,))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()


            ssh_conn = SSHConnectionManager(node['address'], node['username'], node['password'])
            invoker = CommandInvoker(ssh_conn, self.strategy)
            result = invoker.execute(command)
            print(result)



