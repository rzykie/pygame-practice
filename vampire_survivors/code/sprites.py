import os

import pygame
from settings import TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH
from player import Player


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        position,
        surface,
        groups,
    ):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft=position)


class GroundSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        position,
        surface,
        groups,
    ):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft=position)
        self.ground = True


class GunSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        player,
        groups,
    ):
        self.player = player
        self.distance = 140
        self.player_direction = pygame.Vector2(0, 1)

        # sprite setup
        super().__init__(groups)
        self.gun_surface = pygame.image.load(
            os.path.join(
                "vampire_survivors",
                "images",
                "gun",
                "gun.png",
            )
        ).convert_alpha()
        self.image = self.gun_surface
        self.rect = self.image.get_frect(
            center=self.player.rect.center + self.player_direction * self.distance
        )

    def update(self, _):
        self.rect.center = (
            self.player.rect.center + self.player_direction * self.distance
        )
