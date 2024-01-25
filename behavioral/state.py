"""
Поведенческий паттерн проектирования, который позволяет объектам менять
поведение в зависимости от своего состояния. Извне создаётся впечатление,
что изменился класс объекта
"""
from abc import ABC


class State(ABC):
    """Общий интерфейс всех состояний"""

    # Контекст передаёт себя в конструктор состояния, чтобы состояние могло
    # обращаться к его данным и методам в будущем, если потребуется.
    def __init__(self, player: "AudioPlayer") -> None:
        self._player = player

    def click_lock(self) -> None:
        raise NotImplementedError

    def click_play(self) -> None:
        raise NotImplementedError

    def click_next(self) -> None:
        raise NotImplementedError

    def click_previous(self) -> None:
        raise NotImplementedError


# Конкретные состояния реализуют методы абстрактного состояния по-своему.
class LockedState(State):
    # При разблокировке проигрывателя с заблокированными клавишами он может
    # принять одно из двух состояний.
    def click_lock(self) -> None:
        if self._player.is_playing:
            self._player.change_state(PlayingState(self._player))
        else:
            self._player.change_state(ReadyState(self._player))


# Конкретные состояния сами могут переводить контекст в другое состояние.
class ReadyState(State):
    def click_lock(self) -> None:
        self._player.change_state(LockedState(self._player))

    def click_play(self) -> None:
        self._player.start_playback()
        self._player.change_state(PlayingState(self._player))

    def click_next(self) -> None:
        self._player.next_song()

    def click_previous(self) -> None:
        self._player.previous_song()


class PlayingState(State):
    def click_lock(self) -> None:
        self._player.change_state(LockedState(self._player))

    def click_play(self) -> None:
        self._player.stop_playback()
        self._player.change_state(ReadyState(self._player))

    def click_next(self, event: str) -> None:
        if event == "double click":
            self._player.next_song()
        else:
            self._player.fast_forward(5)

    def click_previous(self, event: str) -> None:
        if event == "double click":
            self._player.previous()
        else:
            self._player.rewind(5)


# Проигрыватель выступает в роли контекста.
class AudioPlayer:
    def __init__(self) -> None:
        self.state = ReadyState(self)

    def change_state(self, state: State) -> None:
        self.state = state

    def click_lock(self) -> None:
        self.state.click_lock()

    def click_play(self) -> None:
        self.state.click_play()

    def click_next(self) -> None:
        self.state.click_next()

    def click_previous(self) -> None:
        self.state.click_previous()

    def start_playback(self) -> None:
        ...

    def stop_playback(self) -> None:
        ...

    def next_song(self) -> None:
        ...

    def previous_song(self) -> None:
        ...

    def fast_forward(self, seconds: int) -> None:
        ...

    def rewind(self, seconds: int) -> None:
        ...
