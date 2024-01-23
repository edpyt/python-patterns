"""
Легковес.

Легковес экономит
память, разделяя общее состояние объектов между собой,
вместо хранения одинаковых данных в каждом объекте

Предназначен для обработки большого числа
сравнительно небольших объектов, когда многие из этих объектов являются
дубликатами.
Реализация паттерна предполагает, что каждый уникальный объект представлется
всего один раз и именно этот экземпляр отдается на запрос. В Python легко
реализуется через словарь.
"""


from typing import Any


class TreeType:
    name: str
    color: str
    texture: str

    def __init__(self, name: str, color: str, texture: str) -> None:
        self.name = name
        self.color = color
        self.texture = texture

    def draw(self, canvas: Any, x: float, y: float) -> None:
        """
        1. Создать картину данного типа, цвета и текстуры
        2. Нарисовать картину на холсте в позиции X, Y
        """

        ...


class TreeFactory:
    """
    Фабрика легковесов.

    Решает когда нужно создать новый объект, когда можно обойтись существующим
    """

    tree_types: list[TreeType] = []

    @classmethod
    def get_tree_type(cls, name: str, color: str, texture: str) -> TreeType:
        tree = None

        for tree_type in cls.tree_types:
            if (
                tree_type.name == name and
                tree_type.color == color and
                tree_type.texture == texture
            ):
                tree = tree_type
                break

        if tree is None:
            tree = TreeType(name, color, texture)
            cls.tree_types.append(tree)

        return tree


# Контекстный объект, из которого выделяют легковес TreeType.
# В программе могут быть тысячи объектов Tree, так как накладные расходы на их
# хранение совсем небольшие - в памяти нужно держать всего три целых числа
# (две координаты и ссылка).
class Tree:
    x: float
    y: float
    tree_type: TreeType

    def __init__(self, x: float, y: float, t_type: TreeType) -> None:
        self.x = x
        self.y = y
        self.tree_type = t_type

    def draw(self, canvas: Any) -> None:
        self.tree_type.draw(canvas, self.x, self.y)


# Классы Tree и Forest являются клиентами Легковеса. При желании их можно
# слить в один класс, если вам не нужно расширять класс деревьев далее.
class Forest:
    trees: set[Tree]

    def plant_tree(
        self, x: float, y: float, name: str, color: str, texture: str
    ) -> None:
        tree_type = TreeFactory.get_tree_type(name, color, texture)
        tree = Tree(x, y, tree_type)
        self.trees.add(tree)

    def draw(self, canvas: Any) -> None:
        for tree in self.trees:
            tree.draw(canvas)
