import os

import pygame
from settings import TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH
from player import Player
from math import atan2, degrees


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

    def get_direction(self):
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())
        player_position = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = (mouse_position - player_position).normalize()
        # print(self.player_direction)

    def rotate_gun(self):
        angle = (
            degrees(
                atan2(
                    self.player_direction.x,
                    self.player_direction.y,
                )
            )
            - 90
        )
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(
                self.gun_surface,
                angle,
                1,
            )
        else:
            self.image = pygame.transform.rotozoom(
                self.gun_surface,
                abs(angle),
                1,
            )
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = (
            self.player.rect.center + self.player_direction * self.distance
        )
