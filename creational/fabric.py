"""
Фабричный метод - паттерн проектирования, благодаря которому реализация
строится на основе какой-либо функции/метода.

Это очень полезно при повторяющемся коде.

Например, есть грузовая компания. Изначально код был спроектирован только
для грузовых машин, но потом пришли с идеей добавить судна к логике кода.

На добавление новой логики может уйти очень много времени.
А если нужно будет добавить ещё транспорт?

Благодаря фабричному методу мы можем строить реализацию не опираясь на то,
как работает метод в наследуемом классе, главное, чтобы он был.
"""


from abc import abstractmethod
from typing import Any


class Button:
    def render(self, a: Any, b: Any) -> None:
        ...

    def on_click(self, f: Any) -> None:
        ...


class WindowsButton(Button):
    def render(self, a: Any, b: Any) -> str:
        return 'Windows Button'

    def on_click(self, f: Any) -> None:
        print('Windows Button clicked!!')


class HTMLButton(Button):
    def render(self, a: Any, b: Any) -> str:
        return "<button>I'm the button</button>"

    def on_click(self, f: Any) -> None:
        print('HTML Button clicked!')


class Dialog:
    """Базовый класс фабрики. """

    def render(self) -> None:
        """Фабричный метод"""
        ok_button: Button = self.create_button()
        ok_button.on_click(close_dialog)
        ok_button.render()

    @abstractmethod
    def create_button(self) -> Button:
        """Абстрактный метод создания кнопки"""
        ...


# Конкретные фабрики переопределяют фабричный метод и возвращают из него
# собственные реализации
class WindowsDialog(Dialog):
    def create_button(self) -> Button:
        return WindowsButton()


class WebDialog(Dialog):
    def create_button(self) -> Button:
        return HTMLButton()


class Application:
    dialog: Dialog

    # Приложение создаёт определённую фабрику в зависимости от
    # конфигурации или окружения.
    def initialize(self) -> None:
        config = 'config'

        if config == 'Windows':
            self.dialog = WindowsDialog()
        elif config == 'Web':
            self.dialog = WebDialog()
        else:
            raise Exception('Error! Unknown operating system.')

    def main(self) -> None:
        self.initialize()
        self.dialog.render()