"""
Позволяет поэлементно обходить элементы коллекции или агрегированного объекта

В Python встроена поддержка этого паттерна, предоставляются специальные методы
"""


from typing import Any, Sequence


class Bag:
    def __init__(self, items: None | Sequence = None) -> None:
        self.__bag = {}

        if items is not None:
            for item in items:
                self.add(item)

    def add(self, item) -> None:
        self.__bag[item] = self.__bag.get(item, 0) + 1

    def __delitem__(self, item) -> None:
        if self.__bag.get(item) is not None:
            self.__bag[item] -= 1
            if self.__bag[item] <= 0:
                del self.__bag[item]
        else:
            raise KeyError(str(item))

    def __getitem__(self, key: str) -> Any:
        return self.__bag.get(key)


if __name__ == '__main__':
    bag = Bag()
    bag['1']
