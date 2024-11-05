import pygame

from settings import TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def draw(self, target_position):
        self.offset.x = -(target_position[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_position[1] - WINDOW_HEIGHT / 2)

        ground_sprites = [sprite for sprite in self if hasattr(sprite, "ground")]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, "ground")]

        for layer in [ground_sprites, object_sprites]:
            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery):
                self.display_surface.blit(
                    sprite.image, sprite.rect.topleft + self.offset
                )
