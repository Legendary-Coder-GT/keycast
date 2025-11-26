import pygame
from constants import *

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers) # type: ignore[attr-defined]
        else:
            super().__init__()
        
        self.rect = pygame.Rect(20, 30, 3, 40)
        self.color = WHITE
        self.blink_rate = BLINK_RATE
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self, dt):
        if self.blink_rate <= 0:
            if self.color == WHITE:
                self.color = BLACK
            else:
                self.color = WHITE
            self.blink_rate = BLINK_RATE
        self.blink_rate -= dt

    def move_to(self, x: int, y: int, height: int):
        self.rect.topleft = (x, y)
        self.rect.height = height
