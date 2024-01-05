"""Вместо абстракций создать отдельные классы с реализацией"""


class Drawing1:
    def draw_circle(self, x, y, radius) -> None:
        print(f'Drawing circle at {x} {y} with radius {radius}')


class Drawing2:
    def draw_circle(self, x, y, radius) -> None:
        print(f'Drawing circle at {x} {y} with radius {radius}')


class CircleShape:
    def __init__(
            self,
            x: int,
            y: int,
            radius: int,
            drawing_api: Drawing1 | Drawing2
    ) -> None:
        self._x = x
        self._y = y
        self._radius = radius
        self._drawing_api = drawing_api

    def draw(self) -> None:
        self._drawing_api.draw_circle(self._x, self._y, self._radius)


if __name__ == '__main__':
    circle_shape_1 = CircleShape(1, 2, 3, Drawing1())
    circle_shape_2 = CircleShape(1, 2, 3, Drawing2())

    for circle in [circle_shape_1, circle_shape_2]:
        circle.draw()
