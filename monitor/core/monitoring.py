import time
from typing import List

from monitor.models import NodeInfo
from monitor.core.task import NodeTask
from monitor.core.task_profile import CPUTimeTaskProfile, TaskProfile
from monitor.core.conntection_registry import ConnectionRegistry
from monitor.core.concurrency_strategy import ThreadPoolConcurrency


class TaskExecutor:
    def __init__(self, concurrency_manager, registry):
        self.concurrency_manager = concurrency_manager
        self.registry = registry

    def execute_task(self, task_list: List[NodeTask]):
        for task in task_list:
            key = task.get_node_name()
            self.registry.add_connection(key, task)
            if self.concurrency_manager is None:
                task.run()
            else:
                future = self.concurrency_manager.execute(task.run)
                self.registry.add_execution_unit(key, future)


def add_node(node_info: NodeInfo):
    task_cpu_monitor = NodeTask(node=node_info, task_profile=CPUTimeTaskProfile())
    registry = ConnectionRegistry()
    concurrency_manager = ThreadPoolConcurrency(max_workers=20)
    task_executor = TaskExecutor(concurrency_manager, registry)
    task_executor.execute_task([task_cpu_monitor])


def delete_node(node_name: str):
    registry = ConnectionRegistry()
    registry.remove_connection(node_name)


if __name__ == '__main__':
    nodes = [
        NodeInfo(name='node01', hostname="172.28.201.169", port=10001),
        NodeInfo(name='node02', hostname="172.28.201.169", port=10002),
    ]

    add_node(nodes[0])
    time.sleep(2)
    add_node(nodes[1])
    time.sleep(1)
    delete_node('node01')
    exit()

    # task_profile = TaskProfile(command='uptime', repeat=False)
    # task_profile_repeat = TaskProfile(command='uptime', repeat=True)
    #
    # task_cpu = NodeTask(node=nodes[0], task_profile=task_profile)
    # task_cpu_repeat = NodeTask(node=nodes[1], task_profile=task_profile_repeat)
    #
    # cpu_monitor_profile = CPUTimeTaskProfile()
    # task_cpu_monitor = NodeTask(node=nodes[1], task_profile=cpu_monitor_profile)
    #
    # registry = ConnectionRegistry()
    # concurrency_manager = None  # ThreadPoolConcurrency(max_workers=20)
    # task_executor = TaskExecutor(concurrency_manager, registry)
    # task_executor.execute_task([task_cpu, task_cpu_monitor])
    # time.sleep(3)
    # registry.remove_connection("node02")
