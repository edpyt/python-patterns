"""Служит для того, чтобы предоставить удобный унифицированный интерфейс

Паттерны Фасад и Адаптер на первый взгляд кажутся похожими. Разница в том,
что Фасад надстраивает простой интерфейс поверх сложного, а Адаптер
надстраивает унифицированный интерфейс над каким-то другим
(необязательно сложным). 
"""


class CPU:
    def execute(self) -> None:
        print('Start CPU')


class SolidStateDriver:
    def run(self) -> None:
        print('Run SSD')


class Memory:
    def load(self) -> None:
        print('Load Memory')


class ComputerFacade:
    def __init__(self) -> None:
        self._cpu = CPU()
        self._ssd = SolidStateDriver()
        self._memory = Memory()

    def start(self) -> None:
        self._cpu.execute()
        self._memory.load()
        self._ssd.run()


if __name__ == '__main__':
    computer = ComputerFacade()
    computer.start()
