import re
from monitor.core.db_writer import write

MEASUREMENT_NODE = 'node_monitoring'
MEASUREMENT_CONTAINER = 'container_monitoring'
TAG_NODE_NAME = 'name'
TAG_CONTAINER_ROLE = 'role'
FILED_CPU_USAGE = 'cpu_usage'
FILED_MEMORY_USAGE = 'memory_usage'


class TaskProfile:
    def __init__(self, command, repeat=False):
        self.command = command
        self.repeat = repeat

    def flush_function(self, node_name, command):
        print(node_name, command)


class CPUTimeTaskProfile(TaskProfile):
    def __init__(self):
        super().__init__('uptime', repeat=True)

    @staticmethod
    def extract_one_min_load_average(line):
        match = re.search(r'load average: ([\d.]+),', line)
        if match:
            return float(match.group(1))
        return None

    def flush_function(self, node_name, lines):
        for line in lines:
            field_value = float(self.extract_one_min_load_average(line))
            write(
                measurement_name=MEASUREMENT_NODE,
                tags={TAG_NODE_NAME: node_name},
                fields={FILED_CPU_USAGE: field_value},
                verbose=True,
            )


class MemoryUsageTaskProfile(TaskProfile):
    def __init__(self):
        super().__init__('free', repeat=True)

    @staticmethod
    def extract_memory_info(line):
        match = re.search(r'Mem:\s+(\d+)\s+(\d+)\s+(\d+)', line)
        if match:
            total, used, free = map(int, match.groups())
            usage_percent = (used / total) * 100
            return usage_percent
        return None

    def flush_function(self, node_name, lines):
        for line in lines:
            mem_info = self.extract_memory_info(line)
            if mem_info is not None:
                write(
                    measurement_name=MEASUREMENT_NODE,
                    tags={TAG_NODE_NAME: node_name},
                    fields={'memory_usage': mem_info},
                    verbose=True,
                )
