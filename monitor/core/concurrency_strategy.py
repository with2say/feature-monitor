import threading

from abc import ABC, abstractmethod
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from monitor.models import NodeInfo


class ConcurrencyManager(ABC):
    @abstractmethod
    def execute(self, func, *args, **kwargs):
        pass


class ThreadPoolConcurrency(ConcurrencyManager):
    def __init__(self, max_workers=10):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def execute(self, func, *args, **kwargs):
        return self.executor.submit(func, *args, **kwargs)