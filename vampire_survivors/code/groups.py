import pygame

from settings import TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        # self.half_w, self.half_h = self.display_surface.get_size() // 2

    def draw(self, target_position):
        self.offset.x = -(target_position[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_position[1] - WINDOW_HEIGHT / 2)
        for sprite in self:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
