import os
import random
import pygame
from constants import WINDOW_HEIGHT, WINDOW_WIDTH


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(
            os.path.join("images", "player.png")
        ).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 300

    def update(self, delta_time):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )
        self.rect.center += self.direction * self.speed * delta_time

        recent_key = pygame.key.get_just_pressed()

        if recent_key[pygame.K_SPACE]:
            print("fire laser")


pygame.init()

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("space shooter")
running = True
clock = pygame.time.Clock()

surface = pygame.Surface((100, 200))
surface.fill("seagreen")

all_sprites = pygame.sprite.Group()
player = Player(all_sprites)

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
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #     print(1)
        # if event.type == pygame.MOUSEMOTION:
        #     player_frect.center = event.pos

    all_sprites.update(delta_time)

    display_surface.fill("darkgray")

    for position in star_positions:
        display_surface.blit(star_surface, position)

    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()
