"""Компоновать объекты"""


class Graphic:
    def render(self) -> None:
        raise NotImplementedError


class CompositeGraphic(Graphic):
    def __init__(self) -> None:
        self.graphics = []

    def render(self) -> None:
        for graphic in self.graphics:
            graphic.render()

    def add(self, graphic: Graphic) -> None:
        self.graphics.append(graphic)


class Ellipse(Graphic):
    def __init__(self, name: str) -> None:
        self._name = name

    def render(self) -> None:
        print(f'Ellipse with name: {self._name}')


if __name__ == '__main__':
    ellipse1 = Ellipse('1')
    ellipse2 = Ellipse('2')
    ellipse3 = Ellipse('3')
    ellipse4 = Ellipse('4')

    graphic1 = CompositeGraphic()
    graphic2 = CompositeGraphic()

    graphic1.add(ellipse1)
    graphic1.add(ellipse2)
    graphic1.add(ellipse3)
    graphic2.add(ellipse4)

    graphic = CompositeGraphic()

    graphic.add(graphic1)
    graphic.add(graphic2)

    graphic.render()
