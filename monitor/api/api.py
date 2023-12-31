import time
from monitor.models import NodeInfo, NodeName
from monitor.core.task import NodeTask, TaskExecutor
from monitor.core.task_profile import TaskProfile, CPUTimeTaskProfile, MemoryUsageTaskProfile
from monitor.core.conntection_registry import ConnectionRegistry
from monitor.core.concurrency_strategy import ThreadPoolConcurrency


def add_node_api(node_info: NodeInfo):
    task_cpu_monitor = NodeTask(node=node_info, task_profile=CPUTimeTaskProfile())
    task_memory_monitor = NodeTask(node=node_info, task_profile=MemoryUsageTaskProfile())

    registry = ConnectionRegistry()
    concurrency_manager = ThreadPoolConcurrency(max_workers=20)

    task_executor = TaskExecutor(concurrency_manager, registry)
    task_executor.execute_task([task_cpu_monitor, task_memory_monitor])


def delete_node_api(node_name: NodeName):
    registry = ConnectionRegistry()
    registry.stop_connection(node_name.name)


if __name__ == '__main__':
    nodes = [
        NodeInfo(name='node01', hostname="172.28.201.169", port=10001),
        NodeInfo(name='node02', hostname="172.28.201.169", port=10002),
    ]
    node_names = [NodeName(name='node02'), NodeName(name='node03')]
    # # add_node_api(nodes[0])
    # add_node_api(nodes[0])
    # time.sleep(2)
    # delete_node_api(node_names[0])
    # delete_node_api(node_names[1])
    # exit()

    # from concurrent.futures import ProcessPoolExecutor
    # with ProcessPoolExecutor(max_workers=1) as executor:
    #     future = executor.submit(simple_func, 1, 2, 3)
    #     try:
    #         result = future.result()
    #     except Exception as e:
    #         print(f"An error occurred: {e}")

    # exit()

    task = NodeTask(node=nodes[0], task_profile=TaskProfile(command='uptime'))
    task_cpu = NodeTask(node=nodes[0], task_profile=CPUTimeTaskProfile())
    task_mem = NodeTask(node=nodes[1], task_profile=MemoryUsageTaskProfile())

    registry = ConnectionRegistry()
    concurrency_manager = ThreadPoolConcurrency()
    task_executor = TaskExecutor(concurrency_manager, registry)
    task_executor.execute_task([task, task_cpu, task_mem])

    # time.sleep(2)
    # registry.stop_connection('node01')
