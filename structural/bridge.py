"""
Мост - паттерны, который разделяет один или несколько классов на две отдельные
иерархии — абстракцию и реализацию, позволяя изменять их независимо друг от
друга
"""


from typing import Protocol


class Device(Protocol):
    @property
    def is_enabled(self) -> None:
        ...

    def enable(self) -> None:
        ...

    def disable(self) -> None:
        ...

    def get_volume(self) -> None:
        ...

    def set_volume(self, percent: int | float) -> None:
        ...

    def get_channel(self) -> None:
        ...

    def set_channel(self, channel: int) -> None:
        ...


class Remote:
    _device: "Device"

    def __init__(self, device: "Device") -> None:
        self._device = device

    def toggle_power(self) -> None:
        if self._device.is_enabled:
            self._device.disable()
        else:
            self._device.enable()

    def volume_down(self) -> None:
        self._device.set_volume(self._device.get_volume() - 10)

    def volume_up(self) -> None:
        self._device.set_volume(self._device.get_volume() + 10)

    def channel_down(self) -> None:
        self._device.set_channel(self._device.get_channel() - 1)

    def channel_up(self) -> None:
        self._device.set_channel(self._device.get_channel() + 1)


class AdvancedRemote(Remote):
    def mute(self) -> None:
        self._device.set_volume(0)


class TV(Device):
    ...


class Radio(Device):
    ...


if __name__ == '__main__':
    tv = TV()
    remote = Remote(tv)
    remote.toggle_power()

    radio = Radio()
    remote = AdvancedRemote(radio)
    remote.mute()
