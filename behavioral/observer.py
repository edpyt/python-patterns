"""
Это поведенческий паттерн проектирования, который создаёт механизм подписки,
позволяющий одним объектам следить и реагировать на события, происходящие в
других объектах.
"""

from collections import defaultdict
from typing import Any, Protocol


class File:
    def __init__(self, path: str) -> None:
        self.name = f'Filee path: {path}'

    def write(self) -> None:
        ...


class EventManager:
    """
    Базовый класс-издатель. Содержит код управления подписчиками и их
    оповещения
    """

    def __init__(self) -> None:
        self._listeners = defaultdict([])

    def subscribe(self, event_type: Any, listener: Any) -> None:
        self._listeners[event_type].append(listener)

    def unsubscribe(self, event_type: Any, listener: Any) -> None:
        self._listeners[event_type].remove(listener)

    def notify(self, event_type: Any, data: Any) -> None:
        for listener in self._listeners[event_type]:
            listener.update(data)


class EventListener(Protocol):
    """
    Общий интерфейс подписчиков

    Во многих языках, поддерживающих функциональные типы, можно обойтись без
    этого интерфейса и конкретных классов, заменив объекты подписчиков
    функциями.
    """

    def update(self, filename: str) -> None:
        ...


#  Набор конкретных подписчиков. Они реализуют добавочную функциональность,
#  реагируя на извещения от издателя.
class LoggingListener(EventListener):
    def __init__(self, log_filename: str, message: str) -> None:
        self._log = File(log_filename)
        self._message = message

    def update(self, filename: str) -> None:
        self._log.write(f'{filename} {self._message}')


class EmailAlertsListener(EventListener):
    def __init__(self, email: str, message: str) -> None:
        self.email = email
        self.message = message

    def update(self, filename: str) -> None:
        ...


class Editor:
    """
    Конкретный класс-издатель, содержащий интересную для других компонентов бизнес-логику.

    Мы могли бы сделать его прямым потомком EventManager, но в реальной жизни
    это не всегда возможно (например, если у класса уже есть родитель).

    Поэтому здесь мы подключаем механизм подписки при помощи композиции.
    """


    def __init__(self) -> None:
        self.events = EventManager()
        self._file = None

    # Методы бизнес-логики, которые оповещают подписчиков об их изменениях.
    def open_file(self, path: str) -> None:
        self._file = File(path)
        self.events.notify('open', self._file.name)

    def save_file(self) -> None:
        self._file.write()
        self.events.notify('save', self._file.name)


if __name__ == '__main__':
    # Приложение может сконфигурировать издателей и подписчиков как угодно, в
    # зависимости от целей и окружения.

    editor = Editor()

    logger = LoggingListener('/path/to/log.txt', 'som on ope file')
    editor.events.subscribe('open', logger)

    email_alerts = EmailAlertsListener('admin@example.com', 'soemopne has changed file')
    editor.events.subscribe('save', email_alerts)
