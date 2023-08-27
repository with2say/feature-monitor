from abc import ABC, abstractmethod
import threading


class Strategy(ABC):
    @abstractmethod
    def execute(self, nodes, target, args):
        pass


class OneThreadPerTaskStrategy(Strategy):

    def execute(self, target, args_list):
        threads = []
        for args in args_list:
            t = threading.Thread(target=target, args=args)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()


class EventLoopStrategy(Strategy):
    def execute(self, command):
        # 이벤트 루프를 사용하여 명령 실행
        pass
