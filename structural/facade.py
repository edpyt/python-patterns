"""
Предоставляет простой интерфейс к сложной системе классов, библиотеке или
фреймворку.

Паттерны Фасад и Адаптер на первый взгляд кажутся похожими. Разница в том,
что Фасад надстраивает простой интерфейс поверх сложного, а Адаптер
надстраивает унифицированный интерфейс над каким-то другим
(необязательно сложным). 
"""


class File:
    filename: str

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def save(self) -> None:
        ...


class VideoFile(File):
    ...


class OggCompressionCode:
    ...


class MPEG4CompressionCode:
    ...


class CodecFactory:
    def extract(self) -> None:
        ...


class BitrateReader:
    @classmethod
    def read(cls, filename: str, source_codec) -> None:
        ...

    @classmethod
    def convert(cls, buffer: str, destination_codec) -> None:
        ...


class AudioMixer:
    def fix(self, *args) -> None:
        ...


# Вместо этого мы создаём Фасад - простой интерфейс для работы со сложным
# фреймворком. Фасад не имеет всей функциональности фреймворка, но зато
# скрывает его сложность от клиентов.
class VideoConverter:
    def convert(self, filename: str, format: str) -> File:
        file = VideoFile(filename)
        source_codec = CodecFactory.extract(file)
        if format == 'mp4':
            destination_codec = MPEG4CompressionCode()
        else:
            destination_codec = OggCompressionCode()
        buffer = BitrateReader.read(filename, source_codec)
        result = BitrateReader.convert(buffer, destination_codec)
        result = AudioMixer().fix(result)
        return File(result)


if __name__ == '__main__':
    converter = VideoConverter()
    mp4 = converter.convert('funny-cats.ogg', 'mp4')
    mp4.save()
