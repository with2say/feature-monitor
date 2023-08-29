from monitor.core.connection import *


class NodeTask:
    def __init__(self, node, task_profile):
        self.node = node
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

    def get_node_name(self):
        return self.node.name

    def close(self):
        self.connector.close()
