import os

import pygame
from settings import TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH, walk


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state = "up"
        self.frame_index = 0
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
        self.rect = self.image.get_frect(center=position)
        self.direction = pygame.math.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites
        self.hitbox_rectangle = self.rect.inflate(-60, -90)

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
        self.hitbox_rectangle.x += self.direction.x * self.speed * delta_time
        self.collision("horizontal")
        self.hitbox_rectangle.y += self.direction.y * self.speed * delta_time
        self.collision("vertical")
        self.rect.center = self.hitbox_rectangle.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rectangle):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox_rectangle.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rectangle.left = sprite.rect.right
                    self.direction.x = 0
                if direction == "vertical":
                    if self.direction.y > 0:
                        self.hitbox_rectangle.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox_rectangle.top = sprite.rect.bottom

    def animate(self, delta_time):
        # get state
        if self.direction.x != 0:
            self.state = "right" if self.direction.x > 0 else "left"
        if self.direction.y != 0:
            self.state = "down" if self.direction.y > 0 else "up"
        # animate
        self.frame_index += 5 * delta_time
        self.image = self.frames[self.state][
            int(self.frame_index) % len(self.frames[self.state])
        ]

    def update(self, delta_time):
        self.input()
        self.movement(delta_time)
        self.animate(delta_time)

    def load_images(self):
        self.frames = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
        }

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(
                os.path.join("vampire_survivors", "images", "player", state)
            ):
                for file_name in sorted(
                    file_names, key=lambda name: int(name.split(".")[0])
                ):
                    full_path = os.path.join(folder_path, file_name)
                    surface = pygame.image.load(full_path).convert_alpha()
                    self.frames[state].append(surface)
