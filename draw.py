import pygame
from constants import WHITE, GREEN, HUD_HEIGHT


def draw_hud(surface: pygame.Surface, wpm: float, acc: float, timer: float, progress: float):
    font = pygame.font.Font(None, 32)
    width, _ = surface.get_size()

    # Background bar
    bg_rect = pygame.Rect(0, 0, width, HUD_HEIGHT)
    pygame.draw.rect(surface, (20, 20, 20), bg_rect)

    text = f"WPM: {wpm:.1f}    ACC: {acc:.1f}%    TIME: {timer:0.1f}s"
    text_surf = font.render(text, True, WHITE)
    surface.blit(text_surf, (20, 20))

    # Progress bar
    bar_margin = 20
    bar_height = 12
    bar_width = width - bar_margin * 2
    bar_rect = pygame.Rect(bar_margin, HUD_HEIGHT - 25, bar_width, bar_height)
    pygame.draw.rect(surface, (60, 60, 60), bar_rect)
    clamped = max(0.0, min(1.0, progress))
    fill_rect = pygame.Rect(bar_margin, HUD_HEIGHT - 25, int(bar_width * clamped), bar_height)
    pygame.draw.rect(surface, GREEN, fill_rect)
