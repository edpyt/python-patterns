from abc import abstractmethod
from typing import Protocol


class Button(Protocol):
    @abstractmethod
    def paint(self) -> None:
        raise NotImplementedError


class WinButton(Button):
    def paint(self) -> None:
        """Отрисовать кнопку в стиле Windows"""


class MacButton(Button):
    def paint(self) -> None:
        """Отрисовать кнопку в стиле macOS"""


class Checkbox(Protocol):
    @abstractmethod
    def paint(self) -> None:
        raise NotImplementedError


class WinCheckbox(Checkbox):
    def paint(self) -> None:
        """Отрисовать чекбокс в стиле Windows"""


class MacCheckbox(Checkbox):
    def paint(self) -> None:
        """Отрисовать чекбокс в стиле macOS"""


class GUIFactory(Protocol):
    """Абстрактная фабрика знает обо всех абстрактных типах продуктов"""

    @abstractmethod
    def create_button(self) -> Button:
        raise NotImplementedError

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        raise NotImplementedError


class WinFactory(GUIFactory):
    def create_button(self) -> Button:
        return WinButton()

    def create_checkbox(self) -> Checkbox:
        return WinCheckbox()


# Несмотря на то, что фабрики оперируют конкретными классами,
# их методы возвращают абстрактные типы продуктов.
# Благодаря этому фабрики можно взаимозаменять, не изменяя
# клиентский код
class MacFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()


class Application:
    _factory: GUIFactory
    _button: Button

    def __init__(self, factory: GUIFactory) -> None:
        self._factory = factory

    def create_ui(self) -> None:
        self._button = self._factory.create_button()

    def paint(self) -> None:
        self._button.paint()


class ApplicationConfigurator:
    def main(self) -> None:
        self.config = input()

        match self.config:
            case 'Windows':
                factory = WinFactory()
            case 'Mac':
                factory = MacFactory()
            case _:
                raise Exception('Error! Unknown operating system.')

        self.app: Application = Application(factory)
