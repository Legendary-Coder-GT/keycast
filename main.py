import pygame
import sys
from constants import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # updatable.update(dt)
        screen.fill("black")
        '''
        for thing in drawable:
            thing.draw(screen)
        dt = clock.tick(60) / 1000  # Delta time in seconds.
        pygame.display.flip()
        '''


if __name__ == "__main__":
    main()