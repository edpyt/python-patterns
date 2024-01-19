"""
Создать класс, который будет унифицировать интерфейс

Это структурный паттерн проектирования, который позволяет объектам с
несовместимыми интерфейсами работать вместе.
"""


from math import sqrt


class RoundHole:
    """Круглая дыра"""

    def __init__(self, radius: int) -> None:
        self.radius = radius

    def get_radius(self) -> float:
        """Вернуть радиус отверстия"""

        return self.radius

    def fits(self, peg: 'RoundPeg') -> bool:
        return self.get_radius() >= peg.get_radius()


class RoundPeg:
    """Круглое колышко"""

    def __init__(self, radius: int) -> None:
        self.radius = radius

    def get_radius(self) -> float:
        """Вернуть радиус круглого колышка."""

        return self.radius


class SquarePeg:
    """Квадратное колышко"""

    def __init__(self, width: int) -> None:
        self.width = width

    def get_width(self) -> int:
        """Вернуть ширину квадратного колышка"""

        return self.width


class SquarePegAdapter(RoundPeg):
    """
    Адаптер позволяет использовать квадратные колышки и круглые отверстия
    вместе.
    """

    _peg: SquarePeg

    def __init__(self, peg: SquarePeg) -> None:
        self._peg = peg

    def get_radius(self) -> float:
        return self._peg.get_width() * sqrt(2) / 2


if __name__ == '__main__':
    hole = RoundHole(5)
    rpeg = RoundPeg(5)
    assert hole.fits(rpeg)

    small_speg = SquarePeg(5)
    large_speg = SquarePeg(10)

    try:
        hole.fits(small_speg)
    except AttributeError:
        print('All good')

    small_sqpeg_adapter = SquarePegAdapter(small_speg)
    large_sqpeg_adapter = SquarePegAdapter(large_speg)
    hole.fits(small_sqpeg_adapter)
    hole.fits(large_sqpeg_adapter)
