import os

import pygame
from settings import TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.original_surface = pygame.image.load(
            os.path.join(
                "vampire_survivors",
                "images",
                "player",
                "down",
                "0.png",
            )
        ).convert_alpha()
        self.image = self.original_surface
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 800

    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )

    def movement(self, delta_time):
        self.rect.center += self.direction * self.speed * delta_time

    def update(self, delta_time):
        self.input()
        self.movement(delta_time)
