import time
from typing import Self


class Singleton:
    """Класс одиночки"""

    _instance: Self | None = None

    def __new__(cls, *args, **kwargs) -> Self:
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class Database(Singleton):
    """Класс подключения БД"""

    @classmethod
    def get_instance(cls) -> 'Database | None':
        return cls._instance

    def query(self, sql: str) -> None:
        print('Executing sql query...')
        print(sql)
        time.sleep(.5)
        print('Done!')


if __name__ == '__main__':
    first_database = Database()

    foo: Database = Database()
    assert foo is first_database
    foo.query('SELECT * FROM table1')

    bar: Database = Database.get_instance()
    assert bar is first_database
    foo.query('SELECT * FROM table2')
