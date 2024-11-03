import os
import random

import pygame
from player import Player
from settings import TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH
from sprites import *
from pytmx.util_pygame import load_pygame


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("vampire_survivors")
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.tilemap_setup()
        # player
        self.player = Player((500, 300), self.all_sprites, self.collision_sprites)

        # for _ in range(6):
        #     posx, posy = random.randint(0, WINDOW_WIDTH), random.randint(
        #         0, WINDOW_HEIGHT
        #     )
        #     width, height = random.randint(60, 100), random.randint(50, 100)
        #     CollisionSprite(
        #         (posx, posy),
        #         (width, height),
        #         (self.all_sprites, self.collision_sprites),
        #     )

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(delta_time)

            # draw
            self.display_surface.fill((0, 0, 0))
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()

    def tilemap_setup(self):
        tilemap = load_pygame(
            os.path.join("vampire_survivors", "data", "maps", "world.tmx")
        )
        for tile in tilemap.get_layer_by_name("Objects"):
            CollisionSprite(
                (tile.x, tile.y), tile.image, (self.all_sprites, self.collision_sprites)
            )
            # print(tile.x)
            # print(tile.y)
            # print(tile.image)


if __name__ == "__main__":
    game = Game()
    game.run()


pygame.quit()
