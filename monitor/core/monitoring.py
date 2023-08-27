import time
from connection_old import SSHConnectionManager, ConnectionRegistry
from node_task import NodeTask
from concurrency_strategy import ThreadPoolConcurrency


class TaskExecutor:
    def __init__(self, concurrency_manager, registry):
        self.concurrency_manager = concurrency_manager
        self.registry = registry

    def execute_task(self, nodes, command, repeat=False):
        for node in nodes:
            task = NodeTask(node, command, repeat)
            key = node.name
            self.registry.add_connection(key, task)
            future = self.concurrency_manager.execute(task.run)
            self.registry.add_execution_unit(key, future)

    def execute_task_old(self, nodes, command, repeat=False):
        for node in nodes:
            node_info = node.model_dump()
            key = node_info['name']

            conn = SSHConnectionManager(**node_info)
            self.registry.add_connection(key, conn)

            future = self.concurrency_manager.execute(conn.execute, command, repeat=repeat)
            self.registry.add_execution_unit(key, future)


if __name__ == '__main__':
    from monitor.models import NodeInfo

    nodes = [
        NodeInfo(name='node01', hostname="172.28.201.169", port=10001, username='root', password='qwer1234'),
        NodeInfo(name='node02', hostname="172.28.201.169", port=10002, username='root', password='qwer1234'),
    ]

    registry = ConnectionRegistry()
    concurrency_manager = ThreadPoolConcurrency(max_workers=20)

    task_executor = TaskExecutor(concurrency_manager, registry)
    task_executor.execute_task(nodes=nodes, command='uptime', repeat=True)
    time.sleep(3)
    registry.remove_connection("node02")


