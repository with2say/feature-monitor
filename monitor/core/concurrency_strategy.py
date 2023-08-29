from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from threading import Thread, Lock
import threading


class ConcurrencyManager(ABC):
    _instances = {}
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super(ConcurrencyManager, cls).__new__(cls)
                cls._instances[cls] = instance
            return cls._instances[cls]

    @abstractmethod
    def execute(self, func, *args, **kwargs):
        pass


class ThreadPoolConcurrency(ConcurrencyManager):
    def __init__(self, max_workers=10):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def execute(self, func, *args, **kwargs):
        return self.executor.submit(func, *args, **kwargs)


# TODO: DO NOT USE
# class ProcessThreadHybrid(ConcurrencyManager):
#     def __init__(self, max_workers=10):
#         self.process_pool = ProcessPoolExecutor(max_workers)
#
#     @staticmethod
#     def _thread_function(func, *args, **kwargs):
#         thread = Thread(target=func, args=args, kwargs=kwargs)
#         thread.start()
#
#     def execute(self, func, *args, **kwargs):
#         future = self.process_pool.submit(self._thread_function, func, *args, **kwargs)
#         try:
#             result = future.result()
#         except Exception as e:
#             print(f"An error occurred: {e}")
#         return future
