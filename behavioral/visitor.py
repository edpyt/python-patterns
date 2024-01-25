from typing import Protocol


class Shape(Protocol):
    def move(self, x: float, y: float) -> None:
        ...

    def draw(self) -> None:
        ...

    def accept(self, v: 'Visitor') -> None:
        ...


# Метод принятия посетителя должен быть реализован в каждом элементе, а не
# только в базовом классе. Это поможет программе определить, какой метод
# посетителя нужно вызвать, если вы не знаете тип элемента.
class Dot(Shape):
    def move(self, x: float, y: float) -> None:
        return super().move(x, y)

    def draw(self) -> None:
        return super().draw()

    def accept(self, v: 'Visitor') -> None:
        v.visit_dot(self)


class Circle(Shape):
    def move(self, x: float, y: float) -> None:
        return super().move(x, y)

    def draw(self) -> None:
        return super().draw()

    def accept(self, v: 'Visitor') -> None:
        v.visit_circle(self)


class Rectangle(Shape):
    def move(self, x: float, y: float) -> None:
        return super().move(x, y)

    def draw(self) -> None:
        return super().draw()

    def accept(self, v: 'Visitor') -> None:
        v.visit_rectangle(self)


class CompoundShape(Shape):
    def move(self, x: float, y: float) -> None:
        return super().move(x, y)

    def draw(self) -> None:
        return super().draw()

    def accept(self, v: 'Visitor') -> None:
        v.visit_compound_shape(self)


# Интерфейс посетителей должен содержать методы посещения каждого элемента.
# Важно, чтобы иерархия элементов менялась редко, так как при добавлении нового
# элемента придётся менять всех существующих посетителей.
class Visitor(Protocol):
    def visit_dot(self, d: Dot) -> None:
        ...

    def visit_circle(self, c: Circle) -> None:
        ...

    def visit_rectangle(self, r: Rectangle) -> None:
        ...

    def visit_compound_shape(self, cs: CompoundShape) -> None:
        ...


# Конкретный посетитель реализует одну операцию для всей иерархии элементов.
# Новая операция = новый посетитель. Посетитель выгодно применять, когда новые
# элементы добавляются очень редко, а новые операции — часто
class XMLExportVisitor(Visitor):
    def visit_dot(self, d: Dot) -> None:
        """Экспорт id и координат центра точки."""

        return super().visit_dot(d)

    def visit_circle(self, c: Circle) -> None:
        """Экспорт id, кординат центра и радиуса окружности"""

        return super().visit_circle(c)

    def visit_rectangle(self, r: Rectangle) -> None:
        """
        Экспорт id, кординат левого-верхнего угла, ширины и высоты
        прямоугольника.
        """

        return super().visit_rectangle(r)

    def visit_compound_shape(self, cs: CompoundShape) -> None:
        """
        Экспорт id составной фигуры, а также списка id подфигур, из которых
        она состоит.
        """

        return super().visit_compound_shape(cs)


# Приложение может применять посетителя к любому набору объектов элементов,
# даже не уточняя их типы. Нужный метод посетителя будет выбран благодаря
# проходу через метод accept.
class Application:
    def __init__(self, shapes: list[Shape]) -> None:
        self.all_shapes: list[Shape] = shapes

    def export(self) -> None:
        export_visitor = XMLExportVisitor()

        for shape in self.all_shapes:
            shape.accept(export_visitor)


if __name__ == '__main__':
    shapes = [
        Circle(),
        Dot(),
        Rectangle(),
    ]
    app = Application(shapes)
