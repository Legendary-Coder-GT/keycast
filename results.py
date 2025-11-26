import pygame
from constants import HUD_HEIGHT, WHITE


def draw_results(screen: pygame.Surface, results: dict):
    font = pygame.font.Font(None, 46)
    small = pygame.font.Font(None, 32)
    lines = [
        f"Results ({results['mode']}):",
        f"WPM: {results['wpm']:.1f}",
        f"Accuracy: {results['acc']:.1f}%",
        f"Keys: {results['correct_keys']}/{results['total_keys']} correct",
    ]
    errors = sorted(results["errors"].items(), key=lambda kv: kv[1], reverse=True)
    top_errors = ", ".join(f"{k}:{v}" for k, v in errors[:5]) if errors else "None"
    lines.append(f"Top errors: {top_errors}")
    lines.append("R = Retry   Enter = Menu   Esc = Quit")

    y = HUD_HEIGHT + 60
    for i, line in enumerate(lines):
        surf = font.render(line, True, WHITE) if i == 0 else small.render(line, True, WHITE)
        screen.blit(surf, (60, y))
        y += surf.get_height() + 12


def draw_menu(screen: pygame.Surface, mode: str):
    screen.fill("black")
    font = pygame.font.Font(None, 48)
    small = pygame.font.Font(None, 32)
    lines = [
        "KeyCast",
        f"Mode: {mode}",
        "Press Enter or R to start",
        "Esc to quit",
    ]
    y = HUD_HEIGHT + 80
    for i, line in enumerate(lines):
        surf = font.render(line, True, WHITE) if i == 0 else small.render(line, True, WHITE)
        screen.blit(surf, (60, y))
        y += surf.get_height() + 14
