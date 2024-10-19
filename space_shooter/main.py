import os
import random
import pygame
from constants import WINDOW_HEIGHT, WINDOW_WIDTH

pygame.init()

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("space shooter")
running = True
clock = pygame.time.Clock()

surface = pygame.Surface((100, 200))
surface.fill("seagreen")


player_surface = pygame.image.load(os.path.join("images", "player.png")).convert_alpha()
player_frect = player_surface.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
player_direction = pygame.math.Vector2(1, 1)
player_speed = 200

star_surface = pygame.image.load(os.path.join("images", "star.png")).convert_alpha()
star_positions = [
    (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
    for _ in range(20)
]

meteor_surface = pygame.image.load(os.path.join("images", "meteor.png")).convert_alpha()
meteor_frect = meteor_surface.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surface = pygame.image.load(os.path.join("images", "laser.png")).convert_alpha()
laser_frect = laser_surface.get_frect(bottomleft=(20, WINDOW_HEIGHT - 20))

while running:
    delta_time = clock.tick(60) / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill("darkgray")

    for position in star_positions:
        display_surface.blit(star_surface, position)

    display_surface.blit(meteor_surface, meteor_frect)

    display_surface.blit(laser_surface, laser_frect)

    player_frect.center += player_direction * player_speed * delta_time
    if player_frect.bottom >= WINDOW_HEIGHT or player_frect.top <= 0:
        player_direction.y *= -1
    if player_frect.right >= WINDOW_WIDTH or player_frect.left <= 0:
        player_direction.x *= -1
    # if player_frect.right > WINDOW_WIDTH or player_frect.left < 0:
    #     player_direction *= -1

    display_surface.blit(player_surface, player_frect)

    pygame.display.update()

pygame.quit()
