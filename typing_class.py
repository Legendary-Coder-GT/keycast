import time
import pygame
from dataclasses import dataclass

from cursor import Cursor
from text_stream import TextStream
from constants import ALLOW_BACKSPACE


@dataclass
class Keystroke:
    timestamp: float
    char: str
    expected: str | None
    correct: bool


class TypingController:
    def __init__(self, text_stream: TextStream, cursor: Cursor):
        self.text_stream = text_stream
        self.cursor = cursor
        self.keystrokes: list[Keystroke] = []
        self.typed_count = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_BACKSPACE and ALLOW_BACKSPACE:
            self._undo_last()
            return

        if not event.unicode:
            return

        expected = self.text_stream.peek()
        char = event.unicode
        correct = expected is not None and char == expected

        self.keystrokes.append(Keystroke(time.time(), char, expected, correct))

        if expected is None:
            self.typed_count += 1
            self._move_cursor()
            return

        if correct:
            self.text_stream.advance(clear_error=True)
        else:
            self.text_stream.mark_error()
            self.text_stream.advance(clear_error=False)

        self.typed_count += 1
        self._move_cursor()

    def _undo_last(self):
        if not self.keystrokes:
            return

        self.keystrokes.pop()
        self._recompute_state()
        self._move_cursor()

    def _recompute_state(self):
        self.text_stream.retreat(0)
        self.text_stream.error_indices = set()
        self.typed_count = 0

        for ks in self.keystrokes:
            expected = self.text_stream.peek()
            if expected is None:
                self.typed_count += 1
                continue

            if ks.correct:
                self.text_stream.advance(clear_error=True)
            else:
                self.text_stream.mark_error()
                self.text_stream.advance(clear_error=False)

            self.typed_count += 1

    def _move_cursor(self):
        caret_x, caret_y, caret_height = self.text_stream.caret_for_index(self.typed_count)
        self.cursor.move_to(caret_x, caret_y, caret_height)
