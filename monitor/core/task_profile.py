import re
from typing import Optional

from monitor.core.db_writer import write

MEASUREMENT_NODE = 'node_monitoring'
MEASUREMENT_CONTAINER = 'container_monitoring'
TAG_NODE_NAME = 'name'
TAG_CONTAINER_ROLE = 'role'
FILED_CPU_USAGE = 'cpu_usage'
FILED_MEMORY_USAGE = 'memory_usage'


def build_loop_command(command: str, repeat: Optional[int], interval: float) -> str:
    if repeat != 1:
        if repeat is None:  # 무한 반복
            loop_command = f'while true; do {command}; sleep {interval}; done'
        else:  # 정해진 횟수만큼 반복
            loop_command = f'for i in $(seq 1 {repeat}); do {command}; sleep {interval}; done'

        return f'/bin/bash -c "{loop_command}"'
    else:
        return command


class TaskProfile:
    def __init__(self, command: str, repeat: Optional[int] = 1, interval: float = 0.5):
        self.command = build_loop_command(command, repeat, interval)

    def flush_function(self, node_name: str, command: str) -> None:
        print(node_name, command)


class CPUTimeTaskProfile(TaskProfile):
    def __init__(self):
        super().__init__('uptime', repeat=None)

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
        super().__init__('free', repeat=None)

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
