"""
Снимок - это поведенческий паттерн проектирования, который позволяет сохранять
и восстанавливать прошлые состояния объектов, не раскрывая подробностей их
реализации.
"""

from copy import copy


class Snapshot:
    def __init__(self, editor: 'Editor') -> None:
        self._saved_state = copy(editor.__dict__)
        self._editor: 'Editor' = editor

    def restore(self) -> None:
        self._editor.__dict__.update(self._saved_state)


class Editor:
    def __init__(self, text, cur_x, cur_y, selection_width) -> None:
        self._text = text
        self._cur_x = cur_x
        self._cur_y = cur_y
        self._selection_width = selection_width

    def create_snapshot(self) -> Snapshot:
        return Snapshot(self)


class Command:
    _backup: Snapshot | None = None

    def __init__(self, editor: Editor) -> None:
        self.editor: Editor = editor

    def make_backup(self) -> None:
        self._backup = self.editor.create_snapshot()

    def undo(self) -> None:
        if self._backup:
            self._backup.restore()
