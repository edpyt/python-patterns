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
from typing import Protocol


class Mediator(Protocol):
    """Общий интерфейс посредника"""

    def notify(self, sender: 'Component', event: str) -> None:
        ...


class AuthenticationDialog(Mediator):
    """
    Конкретный посредник. Все связи между конкретными компонентами переехали в
    код посредника. Он получает извещения от своих компонентов и знает как на
    них реагировать
    """

    def __init__(self) -> None:
        self._title: str = ''

        self._login_or_register_checkbox: 'Checkbox'

        self._login_username: str
        self._login_password: str

        self._registration_username: str
        self._registration_password: str
        self._registration_email: str

        self._ok_btn: 'Button'
        self._cancel_btn: 'Button'
    
    def notify(self, sender: 'Component', event: str) -> None:
        # Когда что-то случается с компонентом, он шлёт посреднику оповещение.
        # После получения извещения посредник может либо сделать что-то
        # самостоятельно, либо перенаправить запрос другому компоненту.

        if sender is self._login_or_register_checkbox and event == 'check':
            if self._login_or_register_checkbox.checked:
                title = 'Log In'
                # 1. Показать компоненты формы входа.
                # 2. Скрыть компоненты формы регистрации.
            else:
                title = 'Register'
                # 1. Показать компоненты формы регистрации.
                # 2. Скрыть компоненты формы регистрации.
        
        if sender is self._ok_btn and event == 'click':
            if self._login_or_register_checkbox.checked:
                # Попробовать найти пользователя с данными из формы логина
                found = True
                if not found:
                    # Показать ошибку над формой логина

                    raise 'Error'
            else:
                # 1. Создать пользовательский аккаунт с данными из формы регистрации.
                # 2. Авторизировать этого пользователя
                ...

# Классы компонентов общаются с посредниками через их общий интерфейс.
# Благодаря этому одни и те же компоненты можно использовать в разных посредниках.
class Component:
    def __init__(self, dialog: Mediator) -> None:
        self.dialog: Mediator = dialog

    def click(self) -> None:
        self.dialog.notify(self, 'click')
    
    def keypress(self) -> None:
        self.dialog.notify(self, 'keypress')


# Конкретные компоненты не связаны между собой напрямую. У них есть только один
# канал общения — через отправку уведомлений посреднику.
class Button(Component):
    ...


class Textbox(Component):
    ...


class Checkbox(Component):
    def check(self) -> None:
        self.dialog.notify(self, 'check')
