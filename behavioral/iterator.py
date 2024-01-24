"""
Позволяет поэлементно обходить элементы коллекции или агрегированного объекта,
не раскрывая их внутреннего представления.

В Python встроена поддержка этого паттерна, предоставляются специальные методы
"""


from typing import Protocol


class SocialNetwork(Protocol):
    """
    Общий интерфейс коллекций должен определить фабричный метод для
    производства итератора.

    Можно определить сразу несколько методов, чтобы дать пользователям
    различные варианты обхода одной и той же колекции.
    """
    
    def create_friends_iterator(self, profile_id: str) -> 'ProfileIterator':
        ...

    def create_coworkers_iterator(self, profile_id: str) -> 'ProfileIterator':
        ...


class Facebook(SocialNetwork):
    """Конкретная коллекция знает, объект каких итераторов нужно создавать"""

    def create_friends_iterator(self, profile_id: str) -> 'ProfileIterator':
        return FacebookIterator(self, profile_id, 'friends')

    def create_coworkers_iterator(self, profile_id: str) -> 'ProfileIterator':
        return FacebookIterator(self, profile_id, 'coworkers')
    
    def social_graph_request(self, profile_id: str, type_iter: str) -> list['Profile']:
        return [Profile('3123', 'eds@mail.com'), Profile('12321', 'gjj@mail.com')]


class ProfileIterator(Protocol):
    """Общий интерфейс итераторов"""

    def get_next(self) -> 'Profile':
        ...
    
    def has_more(self) -> bool:
        ...


class FacebookIterator(ProfileIterator):
    """Конкретный итератор"""

    def __init__(self, facebook: Facebook, profile_id: str, type_iter: str) -> None:
        self._facebook: Facebook = facebook
        self._profile_id = profile_id
        self._type_iter = type_iter

        self._current_position: int = 0
        self._cache: list['Profile'] | None = None

    def lazy_init(self) -> None:
        if self._cache is None:
            self._cache = self._facebook.social_graph_request(self._profile_id, self._type_iter)

    # Конкретный итератор реализует методы базового интерфейса по-своему.
    def get_next(self) -> 'Profile':
        if self.has_more():
            res = self._cache[self._current_position]
            self._current_position += 1
            return res

    def has_more(self) -> bool:
        self.lazy_init()
        return self._current_position < len(self._cache)


class SocialSpammer:
    def send(self, iterator: ProfileIterator, message: str) -> None:
        while iterator.has_more():
            profile = iterator.get_next()
            print('Send email to', profile.email, 'with message', message)


class Application:
    """Класс приложения конфигурирует классы, как захочет"""
    
    spammer: SocialSpammer
    network: SocialNetwork

    def __init__(self, working_with: str) -> None:
        self.working_with = working_with.lower()
        self.config()
    
    def config(self) -> None:
        if self.working_with == 'facebook':
            self.network = Facebook()
        self.spammer = SocialSpammer()
    
    def send_spam_to_friends(self, profile: 'Profile') -> None:
        iterator = self.network.create_friends_iterator(profile.get_id())
        self.spammer.send(iterator, 'Very important message')
    
    def send_spam_to_coworkers(self, profile: 'Profile') -> None:
        iterator = self.network.create_coworkers_iterator(profile.get_id())
        self.spammer.send(iterator, 'Very important message')


class Profile:
    def __init__(self, id_: str, email: str) -> None:
        self.id = id_
        self.email = email

    def get_id(self) -> str:
        return self.id


if __name__ == '__main__':
    profile = Profile('21321321', 'ahah@mail.com')
    app = Application('facebook')
    app.send_spam_to_coworkers(profile)
