"""Подменить реализацию класса"""


class TextTag:
    def __init__(self, text: str) -> None:
        self.text = text

    def render(self) -> str:
        return self.text


class BoldWrapper(TextTag):
    def __init__(self, wrapper: TextTag) -> None:
        self._wrapper = wrapper

    def render(self) -> str:
        return f'<b>{self._wrapper.render()}</b>'


class ItalicWrapper(TextTag):
    def __init__(self, wrapper: TextTag) -> None:
        self._wrapper = wrapper

    def render(self) -> str:
        return f'<i>{self._wrapper.render()}</i>'


if __name__ == '__main__':
    text = TextTag('hello!')
    italic_text = ItalicWrapper(text)
    bold_italic_text = BoldWrapper(ItalicWrapper(text))

    print(italic_text.render())
    print(bold_italic_text.render())