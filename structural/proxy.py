"""
Заместитель.

Паттерн, который позволяет подставлять вместо реальных объектов
специальные объекты-заменители. Эти объекты
перехватывают вызовы к оригинальному объекту, позволяя
сделать что-то до или после передачи вызова оригиналу

Является суррогатом другого объекта и контролирует доступ к нему
"""
from abc import ABC
from typing import Any


class ThirdPartyYouTubeLib(ABC):
    """Интерфейс удалённого сервиса"""

    def list_videos(self) -> list:
        raise NotImplementedError

    def get_video_info(self, id_: str) -> Any:
        raise NotImplementedError

    def download_video(self, id_: str) -> None:
        raise NotImplementedError


class ThirdPartyYouTubeClass(ThirdPartyYouTubeLib):
    def list_videos(self) -> list:
        return ['video1', 'video2', 'video3']

    def get_video_info(self, id_: str) -> str:
        return f'video[{id_}]: Good video'

    def download_video(self, id_: str) -> None:
        print(f'[DOWNLOAD]{id_}')


class CachedYouTubeClass(ThirdPartyYouTubeLib):
    """
    Конкретная реализация сервиса.

    Методы этого класса запрашивают у YouTube различную информацию. Скорость
    запроса зависит не только от качества интернет-канала пользователя, но и
    от состояния самого YouTube. Значит, чем больше будет вызов к сервису, тем
    менее отзывчивей станет программа.
    """

    def __init__(self, service: ThirdPartyYouTubeClass) -> None:
        self._service = service
        self._list_cache: list = []
        self._video_cache: None = None
        self.need_reset: bool = False

    def list_videos(self) -> list:
        if self._list_cache is None or self.need_reset:
            self._list_cache = self._service.list_videos()
        return self._list_cache

    def get_video_info(self, id_: str) -> Any:
        if self._video_cache is None or self.need_reset:
            self._video_cache = self._service.get_video_info(id_)
        return self._video_cache

    def download_video(self, id_: str) -> None:
        if self._video_cache is None or self.need_reset:
            self._video_cache = self._service.get_video_info(id_)
        return self._video_cache


class YouTubeManager:
    _service: ThirdPartyYouTubeLib

    def __init__(self, service: ThirdPartyYouTubeLib) -> None:
        self._service = service

    def render_video_page(self, id_: str) -> None:
        info = self._service.get_video_info(id_)
        print(info)

    def render_list_panel(self) -> None:
        li = self._service.list_videos()
        print(li)
    
    def react_on_user_input(self) -> None:
        self.render_video_page('1321')
        self.render_list_panel()


if __name__ == '__main__':
    youtube_service = ThirdPartyYouTubeClass()
    youtube_proxy = CachedYouTubeClass(youtube_service)
    manager = YouTubeManager(youtube_proxy)
    manager.react_on_user_input()
