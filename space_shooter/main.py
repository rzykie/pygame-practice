import os
import random
import pygame
from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from random import uniform
from typing import List


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(
            os.path.join("images", "player.png")
        ).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 200

    def update(self, delta_time):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )
        self.rect.center += self.direction * self.speed * delta_time

        recent_key = pygame.key.get_just_pressed()

        if recent_key[pygame.K_SPACE] and self.can_shoot:
            Laser(all_sprites, laser_surface, self.rect.midtop)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True


class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surface):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(
            center=(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
        )


class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, surface, position):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(midbottom=position)

    def update(self, delta_time):
        self.rect.centery -= 400 * delta_time
        if self.rect.bottom < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups: List[tuple], surface, position):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center=position)

        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.meteor_speed = random.randint(400, 500)

    def update(self, delta_time):
        self.rect.center += self.direction * self.meteor_speed * delta_time
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()


# General setup
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("space shooter")
running = True
clock = pygame.time.Clock()

# import section
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
star_surface = pygame.image.load(os.path.join("images", "star.png")).convert_alpha()
for i in range(20):
    Star(all_sprites, star_surface)
laser_surface = pygame.image.load(os.path.join("images", "laser.png")).convert_alpha()
meteor_surface = pygame.image.load(os.path.join("images", "meteor.png")).convert_alpha()
player = Player(all_sprites)


# custom event -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 50)
while running:
    delta_time = clock.tick(60) / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            meteor_position_1, meteor_position_2 = random.randint(
                0, WINDOW_WIDTH
            ), random.randint(-200, -100)
            Meteor(
                (all_sprites, meteor_sprites),
                meteor_surface,
                (meteor_position_1, meteor_position_2),
            )

    all_sprites.update(delta_time)

    meteor_collided = pygame.sprite.spritecollide(player, meteor_sprites, True)
    if meteor_collided:
        print("collided")

    display_surface.fill("darkgray")

    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()
