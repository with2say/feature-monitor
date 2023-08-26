# monitor/core/strategy.py

from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def execute(self, command):
        pass


class ThreadPoolStrategy(Strategy):
    def execute(self, command):
        # 스레드 풀을 사용하여 명령 실행
        pass


class EventLoopStrategy(Strategy):
    def execute(self, command):
        # 이벤트 루프를 사용하여 명령 실행
        pass
