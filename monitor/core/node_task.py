from monitor.core.connection import *


class NodeTask:
    def __init__(self, node, command, repeat=False):
        self.node = node
        self.command = command
        self.repeat = repeat
        self.connector = None

    def run(self):
        # Connect
        connector = SSHConnector(**self.node.model_dump())
        self.connector = connector

        # Execute
        executor = SSHExecutor(connector, self.command, repeat=self.repeat)
        executor.execute()

        # Post-process
        processor = SSHOutputProcessor(connector, self.node.name)
        processor.read_output()

        # Close connection
        connector.close()

    def close(self):
        self.connector.close()
