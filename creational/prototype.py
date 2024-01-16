"""
Прототип - паттерн, который позволяет копировать объекты, не вдаваясь
в подробности их реализации
"""
from abc import ABCMeta, abstractmethod


class Shape(metaclass=ABCMeta):
    """Базовый прототип"""

    X: int
    Y: int
    color: str

    def __init__(self, source: 'Shape') -> None:
        """Инициализация прототипа"""

        self.X = source.X
        self.Y = source.Y
        self.color = source.color

    @abstractmethod
    def clone(self) -> 'Shape':
        ...


# Конкретный прототип. Метод клонирования создаёт новый объект текущего класса
# передавая в его конструктор ссылку на собственный объект. Благодаря этому
# операция клонирования получается атомарной — пока не выполнится конструктор,
# нового объекта ещё не существует.
#
# Но как только конструктор завершит работу, мы получим польностью готовый
# объект-клон, а не пустой объект, который нужно ещё заполнить.
class Rectangle(Shape):
    width: int
    height: int

    def __init__(self, source: 'Rectangle') -> None:
        # Вызов родительского конструктора нужен, чтобы скопировать
        # потенциальные приватные поля, объявленные в родительском классе.
        super().__init__(source)

        self.width = source.width
        self.height = source.height

    def clone(self) -> 'Shape':
        return Rectangle(self)


class Circle(Shape):
    radius: int

    def __init__(self, source: 'Circle') -> None:
        super().__init__(source)

        self.radius = source.radius

    def clone(self) -> 'Circle':
        return Circle(self)


def business_logic(shapes: list[Shape]) -> None:
    # Плюс Прототипа в том, что вы можете клонировать набор объектов, не зная
    # их конкретные классы.
    shapes_copy: list[Shape] = []

    # Например, мы не знаем какие конкретно объекты находятся внутри массива
    # `shapes`, так как он объявлен с типом Shape. Но благодаря полиморфизму,
    # мы можем клонировать все объекты "вслепую". Будет выполнен метод clone
    # того класса, которым является этот объект.
    for s in shapes:
        # Переменная shapes_copy будет содержать точные копии элементов списка
        # `shapes`
        shapes_copy.append(s.clone())


if __name__ == '__main__':
    shapes = []

    circle: Circle = Circle()
    circle.X = 10
    circle.Y = 10
    circle.radius = 20
    shapes.append(circle)

    # another_circle будет содержать точную копию circle
    another_circle: Circle = circle.clone()
    shapes.append(another_circle)

    rectange: Rectangle = Rectangle()
    rectange.width = 10
    rectange.height = 20
    shapes.append(rectange)

    business_logic(shapes)
