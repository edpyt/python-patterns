"""
Интерпретатор (Interpreter) - паттерн поведения классов.
Для заданного языка определяет представление его грамматики,
а также интерпретатор предложений этого языка.
"""


class RomanNumeralInterpret:
    def __init__(self) -> None:
        self.grammar = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }

    def interpret(self, text: str) -> int:
        numbers = list(map(self.grammar.get, text))  # строки в значения
        if None in numbers:
            raise ValueError('Ошибочное значение: %s' % text)
        result = 0  # накапливаем результат
        temp = None  # запоминаем последнее значение
        while numbers:
            num = numbers.pop(0)
            if temp is None or temp >= num:
                result += num
            else:
                result += (num - temp * 2)
            temp = num
        return result


if __name__ == '__main__':
    interp = RomanNumeralInterpret()
    print(interp.interpret('MMMCMXCIX'))
