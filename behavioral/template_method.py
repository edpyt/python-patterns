from dataclasses import dataclass
from typing import Any


@dataclass
class Enemy:
    position: tuple = (0, 0)


@dataclass
class Map:
    center: tuple = (0, 0)


class GameAI:
    """
    Шаблонный метод должен быть задан в базовом классе. Он состоит из вызовов
    методов в определённом порядке. Чаще всего эти методы являются шагами
    некоего алгоритма.
    """

    def turn(self) -> None:
        self.map = Map()

        self.collect_resources()
        self.build_structures()
        self.build_units()
        self.attack()

    # Некоторые из этих методов могут быть реализованы прямо в базовом классе.
    def collect_resources(self):
        for s in self.build_structures():
            s.collect()

    # А некоторые могут быть полностью абстрактными
    def build_structures(self):
        ...

    def build_units(self):
        ...

    # Кстати, шаблонных методов в классе может быть несколько.
    def attack(self):
        enemy = self.closest_enemy()
        if enemy is None:
            self.send_scouts(self.map.center)
        else:
            self.send_warriors(enemy.position)

    def closest_enemy(self) -> Any:
        return Enemy()

    def send_scouts(self, cords: Any) -> None:
        ...

    def send_warriors(self, pos: Any) -> None:
        ...


# Подклассы могут предоставлять свою реализацию шагов алгоритма, не изменяя
# сам шаблонный метод.
class OrcsAI(GameAI):
    def build_structures(self) -> None:
        # if some resources:
        # Строить фермы, затем бараки, а потом цитадель.
        ...

    def build_units(self) -> None:
        # if (there are plenty of resources) then
        #   if (there are no scouts)
        #      Построить раба и добавить в группу
        #      разведчиков.
        # else
        #      Построить пехотинца и добавить в группу45
        #      воинов.
        ...

    def send_scouts(self, cords: Any) -> None:
        # if (scouts.length > 0) then
        #   Отправить разведчиков на позицию
        ...

    def send_warriors(self, pos: Any) -> None:
        # if (warriors.length > 5) then
        #     Отправить воинов на позицию.
        ...


# Подклассы могут не только реализовывать абстрактные шаги, но и
# переопределять шаги, уже реализованные в базовом классе.
class MonstersAI(GameAI):
    def collect_resources(self) -> None:
        ...

    def build_structures(self) -> None:
        ...

    def build_units(self) -> None:
        ...
