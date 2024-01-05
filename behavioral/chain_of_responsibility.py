import abc
from typing import Any


class Handler(metaclass=abc.ABCMeta):
    def __init__(self, successor: Any | None = None) -> None:
        self.successor = successor

    def handle(self, request: int) -> None:
        res = self.check_range(request)
        if not res and self.successor:
            self.successor.handle(request)

    @abc.abstractmethod
    def check_range(self, request: int) -> None:
        ...


class ConcreteHandler0(Handler):
    @staticmethod
    def check_range(request: int) -> bool:
        if 0 <= request <= 10:
            print("request handled in 0")
            return True
        return False


class ConcreteHandler1(Handler):
    start, end = 11, 20

    def check_range(self, request: int) -> bool:
        if request in range(self.start, self.end + 1):
            print('request handlen in 1')
            return True
        return False


if __name__ == "__main__":
    requests = [2, 3, 10, 12]
    h0 = ConcreteHandler0()
    h1 = ConcreteHandler1()
    h0.successor = h1

    for request in requests:
        h0.handle(request)
