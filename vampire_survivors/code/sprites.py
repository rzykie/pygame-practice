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
        self.rect = self.image.get_frect(center=position)


class GroundSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        position,
        surface,
        groups,
    ):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center=position)
