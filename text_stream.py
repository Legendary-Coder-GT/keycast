import pygame
from constants import *

class TextStream(pygame.sprite.Sprite):
    def __init__(self, filepath: str | None = None, content: str | None = None):
        if hasattr(self, "containers"):
            super().__init__(self.containers) # type: ignore[attr-defined]
        else:
            super().__init__()
        self.filepath = filepath or 'data/texts/sample1.txt'
        self.ind = 0
        if content is not None:
            self.content = content
        else:
            with open(self.filepath, 'r') as file:
                self.content = file.read()
        self.error_indices: set[int] = set()
        self.font = pygame.font.Font(None, 40)
        self.line_height = self.font.get_linesize()
        self.origin = (20, HUD_HEIGHT + 20)
        self.max_line_width = SCREEN_WIDTH - 40
        self._layout = self._compute_layout()
    
    def draw(self, screen):
        for idx, char, x, y, _ in self._layout:
            if char == "\n":
                continue

            if idx in self.error_indices:
                color = RED
            elif idx < self.ind:
                color = GREEN
            else:
                color = WHITE

            text_surface = self.font.render(char, True, color)
            screen.blit(text_surface, (x, y))

    def update(self, dt):
        pass

    def peek(self):
        if self.ind >= len(self.content):
            return None
        return self.content[self.ind]

    def advance(self, clear_error: bool = True):
        if clear_error and self.ind in self.error_indices:
            self.error_indices.discard(self.ind)
        self.ind = min(self.ind + 1, len(self.content))

    def retreat(self, target_index: int | None = None):
        if target_index is None:
            target_index = self.ind - 1
        self.ind = max(0, min(target_index, len(self.content)))

    def mark_error(self):
        if self.ind < len(self.content):
            self.error_indices.add(self.ind)

    def clear_error(self, index: int):
        self.error_indices.discard(index)

    def caret_for_index(self, typed_index: int):
        if not self._layout:
            start_x, start_y = self.origin
            return start_x, start_y, self.line_height

        clamped_index = max(0, min(typed_index, len(self._layout)))
        start_x, start_y = self.origin

        if clamped_index == 0:
            return start_x, start_y, self.line_height

        prev_idx, prev_char, prev_x, prev_y, prev_width = self._layout[clamped_index - 1]

        if prev_char == "\n":
            return start_x, prev_y + self.line_height, self.line_height

        return prev_x + prev_width, prev_y, self.line_height

    def _compute_layout(self):
        positions = []
        start_x, start_y = self.origin
        x, y = start_x, start_y
        max_width = self.max_line_width

        for idx, char in enumerate(self.content):
            if char == "\n":
                positions.append((idx, char, x, y, 0))
                x = start_x
                y += self.line_height
                continue

            char_width, _ = self.font.size(char)
            if x + char_width > start_x + max_width:
                x = start_x
                y += self.line_height

            positions.append((idx, char, x, y, char_width))
            x += char_width

        return positions


    
