"""
Цепочка обязанностей, поведенческий паттерн, который позволяет передавать запросы
последовательно по цепочке обработчиков. Каждый последующий обработчик решает,
может ли он обработать запрос сам и стоит ли передавать запрос дальше по цепи
"""
from abc import ABC
from typing import Protocol


class ComponentWithContextualHelp(Protocol):
    def show_help(self) -> None:
        ...


class Component(ABC, ComponentWithContextualHelp):
    def __init__(self, tooltip_text: str) -> None:
        self.tooltip_text: str | None = tooltip_text
        # Контейнер, содержащий компонент, служит в качестве следующего
        # звена цепочки
        self._container: 'Container | None' = None

    # Базовое поведение компонента заключается в том, чтобы показать
    # всплывающую подсказку, если для неё задан текст.
    # В обратном случае - перенаправить запрос своему контейнеру, если тот существует
    def show_help(self) -> None:
        if self.tooltip_text is not None:
            print('Показать подсказку')
        else:
            self._container.show_help()


# Контейнеры могут включать в себя как простые компоненты, так и другие
# контейнеры. Здесь формируются связи цепочки. Класс контейнера унаследует
# метод show_help от своего родителя - базового компонента.
class Container(Component):
    def __init__(self, tooltip_text: str) -> None:
        self._children: list[Component] = []
        super().__init__(tooltip_text)

    def add(self, child: Component) -> None:
        self._children.append(child)
        child._container = self


# Большинство примитивных компонентов устроит базовое поведение показа помощи
# через подсказку, которое они унаследуют из класса Component
class Button(Component):
    ...


# Но сложные компоненты могут переопределять метод показа помощи по-своему.
# Но и в этом случае они всегда могут вернуться к базовой реализации, вызвав
# метод родителя.
class Panel(Container):
    def __init__(self, x, y, width, height) -> None:
        self.modal_help_text: str | None = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        super().__init__('')
       
    def show_help(self) -> None:
        if self.modal_help_text is None:
            print('Показать модальное окно')
        else:
            super().show_help()


# То же, что и выше
class Dialog(Container):
    def __init__(self, tooltip_text: str) -> None:
        self.wiki_page_url: str | None = None
        super().__init__(tooltip_text)
    
    def show_help(self) -> None:
        if self.wiki_page_url is not None:
            print('Открыть страницу Wiki в браузере.')
        else:
            super().show_help()


if __name__ == '__main__':
    dialog = Dialog('Budget Reports')
    dialog.wiki_page_url = 'https://wiki.com'
    panel = Panel(0, 0, 400, 800)
    panel.modal_help_text = 'This panel does...'
    ok = Button(tooltip_text='OK')
    ok.tooltip_text = 'This is an OK button'
    cancel = Button('Cancel')

    panel.add(ok)
    panel.add(cancel)
    dialog.add(panel)
