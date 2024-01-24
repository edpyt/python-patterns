"""
Комманда - поведенческий паттерн проектирования, который превращает запросы в
объекты, позволяя передавать их как аргументы при вызове методов, ставить
запросы в очередь, логировать их, а также поддерживать отмену операций
"""
from abc import ABC, abstractmethod


class Command(ABC):
    """
    Абстрактная комманда задаёт общий интерфейс для конкретных классов команд
    и содержит базовое поведение отмены операции
    """

    def __init__(self, app: 'Application', editor: 'Editor') -> None:
        self._app: 'Application' = app
        self._editor: 'Editor' = editor
        self._backup: str

    def save_backup(self) -> None:
        """Метод сохранения состояния редактора"""

        self._backup = self._editor.text
    
    def undo(self) -> None:
        """Метод восстановления состоянии редактора"""

        self._editor.text = self._backup

    @abstractmethod
    def execute(self) -> bool:
        """
        Главный метод команды остаётся абстрактным, чтобы каждая конкретная
        команда определила его по-своему. Метод должен возвратить True или
        False в зависимости о того, изменила ли команда состояние редактора, а
        значит, нужно ли её сохранить в истории.
        """
        ...


# Конкретные команды
class CopyCommand(Command):
    def execute(self) -> bool:
        self._app.clipboard = self._editor.get_selection()

        # Команда копирования не изменяет состояние редактора
        return False


class CutCommand(Command):
    # Команды, меняющие состояние редактора, сохраняют состояние редактора
    # и сигнализирует измения возвращая True
    def execute(self) -> bool:

        self.save_backup()
        self._app.clipboard = self._editor.get_selection()
        self._editor.delete_selection()
        return True


class PasteCommand(Command):
    def execute(self) -> bool:
        self.save_backup()
        self._editor.replace_selection(self._app.clipboard)
        return True


class UndoCommand(Command):
    def execute(self) -> bool:
        self._app.undo()
        return False


class CommandHistory:
    def __init__(self) -> None:
        self._history: list[Command] = []
    
    def push(self, c: Command) -> None:
        self._history.append(c)
    
    def pop(self) -> Command:
        return self._history.pop()


class Editor:
    """
    Класс редактора. Он отыгравает роль получателя - команды делегируют ему
    свои действия
    """

    def __init__(self) -> None:
        self.text: str = ''

    def get_selection(self) -> str:
        """Вернуть выбранный текст"""

        return self.text
    
    def delete_selection(self) -> None:
        """Удалить выбранный текст"""

        self.text = self.text[:-1]
        return self.text
    
    def replace_selection(self) -> None:
        """Вставить текст из буфера обмена в текущей позиции"""

        return self.text


class Application:
    """
    Класс приложения.

    Настраивает объекты для совместной работы. Он выступает в роли отправителя
    - создаёт команды, чтобы выполнять какие-то действия.
    """

    def __init__(self) -> None:
        self.clipboard: str
        self.editors: list[Editor]
        self.active_editor: Editor
        self.history: CommandHistory

    # Код привязывающий команды к элементам интерфейса, может выглядить примерно так.
    def create_ui(self) -> None:
        copy = lambda: self.execute_command(CopyCommand(self, self.active_editor))
        cut = lambda: self.execute_command(CutCommand(self, self.active_editor))
        paste = lambda: self.execute_command(PasteCommand(self, self.active_editor))
    
    def execute_command(self, c: Command) -> None:
        """Метод запуска команды, проверяет надо ли добавить команду в историю"""

        if c.execute():
            self.history.push(c)
    
    # Берём последнюю команду из истории и отменяем её последние действия.
    # Мы не знаем конкретный тип команды, но это и не важно, так как команда
    # знает, как отменить своё действие
    def undo(self) -> None:
        command = self.history.pop()
        if command is not None:
            command.undo()
