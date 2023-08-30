from typing import List
from monitor.models import NodeInfo
from monitor.core.connection import SSHExecutor, SSHConnector, SSHOutputProcessor
from monitor.core.task_profile import TaskProfile


class NodeTask:
    def __init__(self, node: NodeInfo, task_profile: TaskProfile):
        self.node = node
        self.node_name = node.name
        self.task_profile = task_profile
        self.connector = None

    def run(self):
        # Connect
        self.connector = SSHConnector(**self.node.model_dump())
        self.connector.execute(self.task_profile.command)

        # Post-process
        processor = SSHOutputProcessor(
            self.connector,
            self.node.name,
            flush_output_callback=self.task_profile.flush_function)
        processor.read_output()

        # Close connection
        self.connector.close()

    def close(self):
        self.connector.close()


class TaskExecutor:
    def __init__(self, concurrency_manager, registry):
        self.concurrency_manager = concurrency_manager
        self.registry = registry

    def execute_task(self, task_list: List[NodeTask]):
        for task in task_list:
            key = task.node_name
            self.registry.add_connection(key, task)
            if self.concurrency_manager is None:
                task.run()
            else:
                self.concurrency_manager.execute(task.run)


