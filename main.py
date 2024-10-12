import pygame
from constants import WINDOW_HEIGHT, WINDOW_WIDTH

pygame.init()

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("space shooter")
running = True

surface = pygame.Surface((100, 200))
surface.fill("seagreen")

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill("darkseagreen1")
    display_surface.blit(surface, (100, 150))
    pygame.display.update()

pygame.quit()
