"""
Компоновщик - структурный паттерн проектирования, который позволяет
сгруппировать множество объектов в древовидную структуру, а затем работать
с ней так, как будто это единичный объект.
"""
from typing import Protocol


class Graphic(Protocol):
    """Общий интерфейс компонента"""

    def move(self, x: float, y: float) -> None:
        ...

    def draw(self) -> None:
        ...


class Dot(Graphic):
    """Простой компонент"""

    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def move(self, x: float, y: float) -> None:
        self.x += x
        self.y += y

    def draw(self) -> None:
        """Нарисовать точку в координате X, Y"""

        print(f'Нарисована точка в координате {self.x}, {self.y}')


# Компоненты могут расширять другие компоненты
class Circle(Dot):
    radius: float

    def __init__(self, x: float, y: float, radius: int) -> None:
        super().__init__(x, y)
        self.radius = radius

    def draw(self) -> None:
        """Нарисовать окружность в координате x, y и радиусом radius"""

        print(
            f'Нарисован круг в координате {self.x} {self.y} с радиусом:'
            f' {self.radius}'
        )


# Контейнер содержит операции добавления/удаления дочерних компонентов.
# Все стандартные операции интерфейса компонентов он делегирует каждому из
# дочерних компонентов
class CompoundGraphic(Graphic):
    def __init__(self) -> None:
        self.children: list[Graphic] = []

    def add(self, child: Graphic) -> None:
        self.children.append(child)

    def remove(self, child: Graphic) -> None:
        if child in self.children:
            self.children.remove(child)

    def move(self, x: float, y: float) -> None:
        for child in self.children:
            child.move(x, y)

    def draw(self) -> None:
        """
        1. Для каждого дочернего компонента:
            - Отрисовать компонент
            - Определить координаты максимальной границы.
        2. Нарисовать пунктирную границу вокруг всей области.
        """
        for children in self.children:
            children.draw()


class ImageEditor:
    all_: CompoundGraphic

    def load(self) -> None:
        self.all_ = CompoundGraphic()

        self.all_.add(Dot(1, 2))
        self.all_.add(Circle(5, 3, 10))

    def group_selected(self, components: list[Graphic]) -> None:
        group = CompoundGraphic()

        for component in components:
            group.add(component)
            self.all_.remove(component)
        self.all_.add(group)

        # Все компоненты будут отрисованы
        self.all_.draw()


if __name__ == '__main__':
    image_editor = ImageEditor()

    image_editor.load()

    components = [Dot(5, 4), Circle(8, 9, 5)]

    image_editor.group_selected(components)
