"""
Стратегия - поведенческий паттерн проектирования, который определяет семейство
схожих алгоритмов и помещает каждый из них в собственный класс, после чего
алгоритмы можно взаимозаменять прямо во время исполнения программы.

В этом примере контекст использует Стратегию для выполнения той или иной
арифметической операции.
"""
from typing import Protocol


class Strategy(Protocol):
    """Общий интерфейс всех стратегий"""

    def execute(self, a: int, b: int) -> None:
        ...


# Каждая конкретная стратегия реализует общий интерфейс своим способом.
class ConcreteStrategyAdd(Strategy):
    def execute(self, a: int, b: int) -> int:
        return a + b


class ConcreteStrategySubtract(Strategy):
    def execute(self, a: int, b: int) -> int:
        return a - b


class ConcreteStrategyMultiply(Strategy):
    def execute(self, a: int, b: int) -> int:
        return a * b


# Контекст всегда работает со стратегиями через общий интерфейс. Он не знает,
# какая именно стратегия ему подана.
class Context:
    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def execute_strategy(self, a: int, b: int) -> None:
        return self._strategy.execute(a, b)


# Конкретная стратегия выбирается на более высоком уровне, например,
# конфигуратором всего приложения. Готовый объект-стратегия подаётся в
# клиентский объект, а затем может быть заменён другой стратегией в любой
# момент на лету.
class ExampleApplication:
    def __init__(self) -> None:
        self._context = Context(ConcreteStrategyAdd())

    def main(self, action: str) -> None:
        # 1. Создать объект контекста.
        # 2. Получить первое число (n1).
        # 3. Получить второе число (n2).
        # 4. Получить желаемую операцию.
        # 5. Затем, выбрать стратегию:

        if action == '1':
            self._context.set_strategy(ConcreteStrategyAdd())
        elif action == '2':
            self._context.set_strategy(ConcreteStrategySubtract())
        elif action == '3':
            self._context.set_strategy(ConcreteStrategyMultiply())

        n1, n2 = map(int, input('Введите два числа через пробел\n').split())
        result = self._context.execute_strategy(n1, n2)

        print(result)


if __name__ == '__main__':
    app = ExampleApplication()
    text_helper = (
        'Введите операцию над двумя цифрами\n'
        '1 - добавление\n'
        '2 - разность\n'
        '3 - умножение\n'
    )
    strategy_title = input(text_helper).lower()
    app.main(strategy_title)
