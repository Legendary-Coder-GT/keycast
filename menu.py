import os
from pathlib import Path
import pygame
from constants import HUD_HEIGHT, WHITE, GREEN


class Menu:
    def __init__(self, texts_dir: str = "data/texts"):
        self.options = [("Timed", "timed"), ("Fixed Text", "fixed"), ("Drill", "drill")]
        self.selected_idx = 0
        self.stage = "mode"  # mode or file
        self.texts_dir = Path(texts_dir)
        self.text_files = sorted([p for p in self.texts_dir.glob("*.txt") if p.is_file()])
        self.text_idx = 0

    def handle_event(self, event: pygame.event.Event):
        if event.type != pygame.KEYDOWN:
            return None

        if self.stage == "mode":
            idx_from_num = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2}
            if event.key in idx_from_num:
                self.selected_idx = idx_from_num[event.key]
                return self._select_current()
            if event.key == pygame.K_UP:
                self.selected_idx = (self.selected_idx - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_idx = (self.selected_idx + 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return self._select_current()
        elif self.stage == "file":
            if event.key == pygame.K_ESCAPE:
                self.stage = "mode"
                return None
            if not self.text_files:
                return None
            if event.key == pygame.K_UP:
                self.text_idx = (self.text_idx - 1) % len(self.text_files)
            elif event.key == pygame.K_DOWN:
                self.text_idx = (self.text_idx + 1) % len(self.text_files)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return {
                    "mode": "fixed",
                    "text_path": str(self.text_files[self.text_idx]),
                }
        return None

    def _select_current(self):
        label, mode = self.options[self.selected_idx]
        if mode == "fixed":
            if self.text_files:
                self.stage = "file"
                return None
            # fall through to default text if none found
        return {
            "mode": mode,
            "text_path": str(self.text_files[self.text_idx]) if self.text_files else "data/texts/sample1.txt",
        }


def draw_menu(screen: pygame.Surface, menu: Menu):
    screen.fill("black")
    font = pygame.font.Font(None, 48)
    small = pygame.font.Font(None, 32)

    y = HUD_HEIGHT + 60
    title = font.render("KeyCast", True, WHITE)
    screen.blit(title, (60, y))
    y += title.get_height() + 20

    for i, (label, _) in enumerate(menu.options):
        color = GREEN if i == menu.selected_idx and menu.stage == "mode" else WHITE
        text = f"{i+1}. {label}"
        surf = small.render(text, True, color)
        screen.blit(surf, (80, y))
        y += surf.get_height() + 10

    if menu.stage == "file":
        y += 10
        header = small.render("Choose text file (Enter to select, Esc to go back):", True, WHITE)
        screen.blit(header, (80, y))
        y += header.get_height() + 8
        if not menu.text_files:
            screen.blit(small.render("No text files found.", True, WHITE), (100, y))
        else:
            for idx, path in enumerate(menu.text_files):
                color = GREEN if idx == menu.text_idx else WHITE
                screen.blit(small.render(path.name, True, color), (100, y))
                y += small.get_height() + 6
    else:
        y += 14
        hint_lines = [
            "Use 1/2/3 or arrows + Enter",
            "Esc quits",
        ]
        for line in hint_lines:
            screen.blit(small.render(line, True, WHITE), (80, y))
            y += small.get_height() + 6
