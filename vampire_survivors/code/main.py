import os

import pygame
from player import Player
from settings import TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH
from sprites import CollisionSprite, GroundSprite, GunSprite, BulletSprite
from pytmx.util_pygame import load_pygame
from groups import AllSprites, BulletGroup
from ui import AutoShootButtonUI


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("vampire_survivors")
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()
        self.load_images()

        # Button
        self.auto_shoot_button_ui = AutoShootButtonUI(self.display_surface)
        self.previous_mouse_state = False

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = BulletGroup()

        self.tilemap_setup()

        self.can_shoot = True
        self.shoot_timer = 0
        self.gun_cooldown = 400
        # player

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
            self.gun_timer()
            self.input()
            self.all_sprites.update(delta_time)
            self.auto_shoot_button_ui.update()

            # draw
            self.display_surface.fill((0, 0, 0))
            self.all_sprites.draw(self.player.rect.center)
            self.auto_shoot_button_ui.draw()
            pygame.display.update()

    def tilemap_setup(self):
        tilemap = load_pygame(
            os.path.join("vampire_survivors", "data", "maps", "world.tmx")
        )

        for ground_x, ground_y, ground_image in tilemap.get_layer_by_name(
            "Ground"
        ).tiles():
            GroundSprite(
                (ground_x * TILE_SIZE, ground_y * TILE_SIZE),
                ground_image,
                self.all_sprites,
            )

        for tile in tilemap.get_layer_by_name("Objects"):
            CollisionSprite(
                (tile.x, tile.y), tile.image, (self.all_sprites, self.collision_sprites)
            )

        for collision_object in tilemap.get_layer_by_name("Collisions"):
            CollisionSprite(
                (collision_object.x, collision_object.y),
                pygame.Surface((collision_object.width, collision_object.height)),
                self.collision_sprites,
            )

        for marker in tilemap.get_layer_by_name("Entities"):
            if marker.name == "Player":
                self.player = Player(
                    (marker.x, marker.y),
                    self.all_sprites,
                    self.collision_sprites,
                )
                self.gun = GunSprite(self.player, self.all_sprites)

            # CollisionSprite(
            #     (marker.x, marker.y),
            #     pygame.Surface((marker.width, marker.height)),
            #     self.collision_sprites,
            # )

    def input(self):
        mouse_position = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        current_mouse_state = pygame.mouse.get_pressed()[0]

        if current_mouse_state and not self.previous_mouse_state:
            self.auto_shoot_button_ui.toggle_button(mouse_position)

        self.previous_mouse_state = current_mouse_state

        if mouse_click[0]:
            self.auto_shoot_button_ui.toggle_button(mouse_position=mouse_position)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_shoot:
            bullet_position = self.gun.rect.center + self.gun.player_direction * 50
            BulletSprite(
                self.bullet_surface,
                bullet_position,
                self.gun.player_direction,
                (self.all_sprites, self.bullet_sprites),
            )
            self.can_shoot = False
            self.shoot_timer = pygame.time.get_ticks()
            print("shoot")

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_timer >= self.gun_cooldown:
                self.can_shoot = True

    def load_images(self):
        self.bullet_surface = pygame.image.load(
            os.path.join("vampire_survivors", "images", "gun", "bullet.png")
        ).convert_alpha()
        self.bullet_surface = pygame.transform.scale(self.bullet_surface, (30, 30))


if __name__ == "__main__":
    game = Game()
    game.run()


pygame.quit()
