import os

import pygame
from settings import TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH
from player import Player


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        position,
        size,
        groups,
    ):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.fill((10, 155, 199))
        self.rect = self.image.get_frect(center=position)
