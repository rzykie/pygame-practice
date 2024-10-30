import os

import pygame
from settings import TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, collision_sprites):
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
        self.collision_sprites = collision_sprites

        # mask
        self.player_mask = pygame.mask.from_surface(self.image)

    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )

    def movement(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time
        self.collision("horizontal")
        self.rect.y += self.direction.y * self.speed * delta_time
        self.collision("vertical")

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                    self.direction.x = 0
                if direction == "vertical":
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                #     self.direction.y = 0

    def update(self, delta_time):
        self.input()
        self.movement(delta_time)
