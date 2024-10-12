import os
import random
import pygame
from constants import WINDOW_HEIGHT, WINDOW_WIDTH

pygame.init()

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("space shooter")
running = True

surface = pygame.Surface((100, 200))
surface.fill("seagreen")


player_surface = pygame.image.load(os.path.join("images", "player.png")).convert_alpha()
star_surface = pygame.image.load(os.path.join("images", "star.png")).convert_alpha()
star_positions = [
    (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
    for _ in range(20)
]
while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill("darkgray")

    for position in star_positions:
        display_surface.blit(star_surface, position)

    display_surface.blit(player_surface, (100, 150))

    pygame.display.update()

pygame.quit()
