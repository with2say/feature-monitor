from typing import List
from monitor.models import NodeInfo
from monitor.core.connection import SSHExecutor, SSHConnector, SSHOutputProcessor
from monitor.core.task_profile import TaskProfile


class NodeTask:
    def __init__(self, node: NodeInfo, task_profile: TaskProfile):
        self.node = node
        self.node_name = node.name
        self.command = task_profile.command
        self.repeat = task_profile.repeat
        self.flush_function = task_profile.flush_function
        self.connector = None

    def run(self):
        # Connect
        connector = SSHConnector(**self.node.model_dump())
        self.connector = connector

        # Execute
        executor = SSHExecutor(connector, self.command, repeat=self.repeat)
        executor.execute()

        # Post-process
        processor = SSHOutputProcessor(
            connector,
            self.node.name,
            flush_output_callback=self.flush_function)
        processor.read_output()

        # Close connection
        connector.close()

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


