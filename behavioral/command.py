"""
Инкапсулирует запрос в объекте, позволяя тем самым параметризовать клиенты
для разных запросов, ставить запросы в очередь или протоколировать
их, а также поддерживать отмену операций.
"""


class MoveFileCommand:
    def __init__(self, src, dest) -> None:
        self.src = src
        self.dest = dest

    def execute(self) -> None:
        self.rename(self.src, self.dest)

    def undo(self) -> None:
        self.rename(self.dest, self.src)

    def rename(self, src, dest) -> None:
        print(f'rename {src} to {dest}')


if __name__ == '__main__':
    x = MoveFileCommand('1', '2')
    x.execute()
    x.undo()
