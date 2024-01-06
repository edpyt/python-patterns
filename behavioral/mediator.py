"""
Паттерн Посредник представляет средства для создания объекта - посредника -
который инкапсулирует взаимодействия между другими объектами.

Это позволяет осуществлять взаимодействия между объектами, которые ничего
не знают друг о друге.

Например, в случае нажатия кнопки соответствующий ей объект должен только
известить посредника, а уж тот уведомит все объекты, которых интересует
нажатие этой кнопки.

Посредник обеспечивает слабую связанность системы, избавляя объекты от
необходимости явно ссылаться друг на друга и позволяя тем самым независимо
изменять взаимодействия между ними.
"""


class ChatRoom:
    """Mediator (чисто дескриптор какой-то)"""

    def display_message(self, user: str, message: str) -> None:
        print(f'User {user}: {message}')


class User:
    def __init__(self, username: str) -> None:
        self.username = username
        self.chat_room = ChatRoom()

    def send_message(self, message: str) -> None:
        self.chat_room.display_message(self.username, message)


if __name__ == '__main__':
    user1 = User('Anya')
    user2 = User('Alex')

    user1.send_message('Hello!')
    user2.send_message('Hi!!!')
