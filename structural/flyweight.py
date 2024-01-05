"""
Приспособленец предназначен для обработки большого числа
сравнительно небольших объектов, когда многие из этих объектов являются
дубликатами.
Реализация паттерна предполагает, что каждый уникальный объект представлется
всего один раз и именно этот экземпляр отдается на запрос. В Python легко
реализуется через словарь.
"""

import weakref


class Card:
    _pool = weakref.WeakValueDictionary()

    def __new__(cls, value: str, suit: str) -> 'Card':
        key = value + suit
        obj = cls._pool.get(key)
        if obj is None:
            obj = object.__new__(Card)
            cls._pool[key] = obj
            obj.value, obj.suit = value, suit
        return obj


if __name__ == '__main__':
    card1 = Card('9', 'h')
    card2 = Card('9', 'h')

    print(card1 == card2)
    print(card1 is card2)
