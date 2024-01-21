"""
Декоратор - структурный паттерн проектирования, который позволяет динамически
добавлять объектам новую функциональность, оборачивая их в полезные «обёртки».
"""
from typing import Any, Protocol


class DataSource(Protocol):
    """Общий интерфейс компонентов"""

    def write_data(self, data: Any) -> None:
        ...

    def read_data(self) -> None:
        ...


class FileDataSource(DataSource):
    """Один из конкретных компонентов, реализует базовую функциональность"""

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def write_data(self, data: Any) -> None:
        print('Запись данных в файл')

    def read_data(self) -> None:
        print('Прочитать данные из файла')


class DataSourceDecorator(DataSource):
    """Родитель всех декораторов"""

    _wrapee: DataSource

    def __init__(self, source: DataSource) -> None:
        self._wrapee = source

    def write_data(self, data: Any) -> None:
        self._wrapee.write_data(data)

    def read_data(self) -> None:
        self._wrapee.read_data()


class EncryptionDecorator(DataSourceDecorator):
    """
    Конкретные декораторы добавляют что-то своё к базовому поведению
    обёрнутого компонента.
    """

    _wrapee: DataSource

    def __init__(self, source: DataSource) -> None:
        self._wrapee = source

    def write_data(self, data: Any) -> None:
        """
        1. Зашифровать поданные данные
        2. Передать зашифрованные данные в метод write_data обёрнутого объекта
            (_wrapee)
        """
        ...

    def read_data(self) -> Any:
        """
        1. Получить данные из метода read_data обёрнутого объекта (_wrapee).
        2. Распаковать их, если они зашифрованны.
        3. Вернуть результат.
        """
        ...


class CompressionDecorator(DataSourceDecorator):
    def write_data(self, data: Any) -> None:
        """
        1. Запаковать поданные данные
        2. Передать запакованные данные в метод write_data обёрнутого объекта
            (_wrapee)
        """
        ...

    def read_data(self) -> None:
        """
        1. Получить данные из метода read_data обёрнутого объекта (_wrapee).
        2. Распаковать их, если они запакованные.
        3. Вернуть результат.
        """
        ...


class SalaryManager:
    source: DataSource

    def __init__(self, source: DataSource) -> None:
        self.source = source

    def load(self) -> None:
        return self.source.read_data()

    def save(self) -> None:
        self.source.write_data(11_000)
 

if __name__ == '__main__':
    source = FileDataSource('somefile.py')
    source.write_data('print("Hello World!")')

    source = CompressionDecorator(source)

    source = EncryptionDecorator(source)

    source.write_data(11_000)

    # Пример 2 ---------------------------------

    source = FileDataSource('salary.data')

    enabled_encryption = True
    enabled_compression = True

    if enabled_encryption:
        source = EncryptionDecorator(source)
    if enabled_compression:
        source = CompressionDecorator(source)

    logger = SalaryManager(source)
    salary = logger.load()
