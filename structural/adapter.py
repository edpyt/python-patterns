"""Создать класс, который будет унифицировать интерфейс"""


from copy import copy


class Dog:
    def woof(self) -> str:
        return 'woof'


class Human:
    def say(self) -> str:
        return 'Hello!'


class Cat:
    def meow(self) -> str:
        return 'meow'


class Adapter:
    def __init__(self, obj: object, **adapted_methods) -> None:
        self.obj = obj
        self.__dict__.update(**adapted_methods)


if __name__ == '__main__':
    dog = Dog()
    dog_adapter = Adapter(dog, make_noise=dog.woof)

    cat = Cat()
    cat_adapter = Adapter(cat, make_noise=cat.meow)

    human = Human()
    human_adapter = Adapter(human, make_noise=human.say)

    local_items = copy(locals()).items()

    for k, v in local_items:
        if k.endswith('_adapter'):
            print(k, v.make_noise())
