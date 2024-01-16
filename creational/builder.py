"""
Строитель - позволяет создавать сложные объекты пошагово. Строитель даёт
возможность использовать один и тот же код строительства для получения разных
представлений объектов
"""

from dataclasses import dataclass
from typing import Protocol


class Engine(Protocol):
    """Интерфейс Двигатель"""

    horsepower: int


@dataclass
class DefaultEngine(Engine):
    horsepower: int = 150


@dataclass
class SportsEngine(Engine):
    horsepower: int = 800


@dataclass
class TripComputer:
    name: str = ''


@dataclass
class GPS:
    model: str = ''


# Строитель может создавать различные продукты, используя один и тот же процесс
# строительства
@dataclass
class Car:
    # Автомобили могут отличаться комплектацией
    seats: int | None = None
    engine: Engine | None = None
    trip_computer: TripComputer | None = None
    gps: GPS | None = None


class Manual(Protocol):
    """Интерфейс базового класса Справочник"""

    def info(self) -> str:
        ...


@dataclass
class CarManual(Manual):
    seats: int = 0
    engine: Engine | None = None
    trip_computer: TripComputer | None = None
    gps: GPS | None = None

    @property
    def read_seats(self) -> str:
        return f'Сидений: {self.seats}'

    @property
    def read_engine(self) -> str:
        if self.engine:
            return f'Л/с: {self.engine.horsepower}'
        return 'Нет двигателя'

    @property
    def read_trip_computer(self) -> str:
        if self.trip_computer:
            return f'Система навигации: {self.trip_computer.name}'
        return 'Нет системы навигации'

    @property
    def read_gps(self) -> str:
        if self.gps:
            return f'GPS: {self.gps.model}'
        return 'Нет GPS'

    def info(self) -> str:
        return '\n'.join(
            (
                self.read_seats,
                self.read_engine,
                self.read_trip_computer,
                self.read_gps,
            )
        )


class Builder(Protocol):
    """Интерфейс Строитель"""

    def reset(self) -> None:
        ...

    def set_seats(self, seats: int) -> None:
        ...

    def set_engine(self, engine: Engine) -> None:
        ...

    def set_trip_computer(self, trip_computer: TripComputer) -> None:
        ...

    def set_gps(self, gps: GPS) -> None:
        ...


class CarBuilder(Builder):
    _car: Car

    def reset(self) -> None:
        """Поместить новый объект `Car`"""

        self._car = Car()

    def set_seats(self, seats: int) -> None:
        """Установить указанное количество сидений"""

        self._car.seats = seats

    def set_engine(self, engine: Engine) -> None:
        """Установить поданный двигатель"""

        self._car.engine = engine

    def set_trip_computer(
        self, trip_computer: bool, name: str = 'unknown'
    ) -> None:
        """Установить поданную систему навигации"""

        if trip_computer:
            self._car.trip_computer = TripComputer(name)
        else:
            self._car.trip_computer = None

    def set_gps(self, gps: bool, model: str = 'unknown') -> None:
        """Установить или снять GPS"""

        if gps:
            self._car.gps = GPS(model=model)
        else:
            self._car.gps = None

    def get_result(self) -> Car:
        """Вернуть текущий объект автомобиля"""

        return self._car


# В отличие от других порождающих паттернов, где продукты должны быть частью
# одной иерархии классов или следовать общему интерфейсу, строители могут
# создавать совершенно разные продукты, которые не имеют общего продукта
class CarManualBuilder(Builder):
    _manual: CarManual

    def reset(self) -> None:
        """Поместить новый объект `CarManual`"""

        self._manual = CarManual()

    def set_seats(self, seats: int) -> None:
        """Описать сколько мест в машине"""

        self._manual.seats = seats

    def set_engine(self, engine: Engine) -> None:
        """Добавить в руководство описание двигателя"""

        self._manual.engine = engine

    def set_trip_computer(
        self, trip_computer: bool, name: str = 'unknown'
    ) -> None:
        """Добавить в руководство описание системы навигации"""

        if trip_computer:
            self._manual.trip_computer = TripComputer(name=name)
        else:
            self._manual.trip_computer = None

    def set_gps(self, gps: bool, model: str = 'unknown') -> None:
        """Добавить в инструкцию инструкцию GPS"""

        if gps:
            self._manual.gps = GPS(model=model)
        else:
            self._manual.gps = None

    def get_result(self) -> CarManual:
        """Вернуть текущий объект руководства"""

        return self._manual


# Директор знает, в какой последовательности нужно заставлять работать
# строителя, чтобы получить ту или иную версию продукта.
# Директор работает со строителем через общий интерфейс, благодаря чему он не
# знает тип продукта, который изготавливает строитель.
class Director:
    def construct_sports_car(self, builder: Builder) -> None:
        builder.reset()
        builder.set_seats(2)
        builder.set_engine(SportsEngine())
        builder.set_trip_computer(True)
        builder.set_gps(True)


def make_car() -> tuple[Car, CarManual]:
    director: Director = Director()

    builder: CarBuilder = CarBuilder()
    director.construct_sports_car(builder)
    car: Car = builder.get_result()

    builder: CarManualBuilder = CarManualBuilder()
    director.construct_sports_car(builder)
    manual: Manual = builder.get_result()

    return car, manual


if __name__ == '__main__':
    car, car_manual = make_car()

    print(car, car_manual.info(), sep='\n')


"""
Применимость.

Когда нужно избавиться от "телескопического конструктора".

Допустим, у вас есть один конструктор с десятью опциональными параметрами.
Его неудобно вызывать, поэтому вы создали ещё десять конструкторов с меньшим
количеством параметров. Всё, что они делают — это переадресуют вызов к
базовому конструктору, подавая какие-то значения по умолчанию в параметры,
которые пропущены в них самих.
"""
