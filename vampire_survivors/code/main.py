import os

import pygame
from settings import TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH


class Game:
    def __init__(self):
        super().__init__()
        self.startup = pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.title_name = "vampire_survivors"
        self.running = True
        self.clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.original_surface = pygame.image.load(
            os.path.join("images", "player.png")
        ).convert_alpha()
        self.image = self.original_surface
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 800


game = Game()

while game.running:
    delta_time = game.clock.tick(60) / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
    game.display_surface.fill("#6415B8")

    pygame.display.update()


pygame.quit()
