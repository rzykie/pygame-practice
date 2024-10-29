import os
import random
import pygame
from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from random import uniform
from typing import List


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

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 200

        # mask
        # Not actually needed for other sprites
        self.player_mask = pygame.mask.from_surface(self.image)
        # player_mask = pygame.mask.from_surface(self.image)
        # mask_surf = player_mask.to_surface()
        # mask_surf.set_colorkey((0, 0, 0))
        # self.image = mask_surf

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
            Laser((all_sprites, laser_sprites), laser_surface, self.rect.midtop)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

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
        self.original_surface = surface
        self.image = self.original_surface
        self.rect = self.image.get_frect(center=position)
        self.rotation_speed = random.randint(80, 120)
        self.rotation = 0

        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.meteor_speed = random.randint(400, 500)

        self.meteor_mask = pygame.mask.from_surface(self.image)

    def update(self, delta_time):
        self.rect.center += self.direction * self.meteor_speed * delta_time
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

        # meteor rotation
        self.rotation += self.rotation_speed * delta_time
        self.image = pygame.transform.rotozoom(self.original_surface, self.rotation, 1)
        self.rect = self.image.get_frect(center=self.rect.center)


class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(
        self,
        groups,
        position,
        frames,
    ):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=position)

    def update(self, delta_time):
        self.frame_index += 25 * delta_time
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()


def collisions():
    global running

    collision_sprites = pygame.sprite.spritecollide(
        player, meteor_sprites, True, pygame.sprite.collide_mask
    )
    if collision_sprites:
        running = False

    for laser in laser_sprites:
        collided_laser = pygame.sprite.spritecollide(
            laser, meteor_sprites, True, pygame.sprite.collide_mask
        )
        if collided_laser:
            laser.kill()
            AnimatedExplosion(all_sprites, laser.rect.midtop, explosion_frames)
            explosion_sound.play()


def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surface = font.render(str(current_time), True, "black")
    text_rect = text_surface.get_frect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    padded_text_rect = text_rect.inflate(20, 12)
    display_surface.blit(text_surface, text_rect)
    pygame.draw.rect(
        display_surface, "red", padded_text_rect.move(0, -8), 5, 10, 5, 5, 5, 5
    )


# General setup
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("space shooter")
running = True
clock = pygame.time.Clock()

# import section
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
star_surface = pygame.image.load(os.path.join("images", "star.png")).convert_alpha()
font = pygame.font.Font(os.path.join("fonts", "Oxanium-Bold.ttf"), 40)
explosion_frames = [
    pygame.image.load((os.path.join("images", "explosion", f"{i}.png"))).convert_alpha()
    for i in range(21)
]

laser_sound = pygame.mixer.Sound(os.path.join("audio", "laser.wav"))
laser_sound.set_volume(0.3)
explosion_sound = pygame.mixer.Sound(os.path.join("audio", "explosion.wav"))
# damage_sound = pygame.mixer.Sound(os.path.join("audio", "damage.ogg"))
game_music = pygame.mixer.Sound(os.path.join("audio", "game_music.wav"))
game_music.play(loops=-1)
game_music.set_volume(0.1)

for i in range(20):
    Star(all_sprites, star_surface)
laser_surface = pygame.image.load(os.path.join("images", "laser.png")).convert_alpha()
meteor_surface = pygame.image.load(os.path.join("images", "meteor.png")).convert_alpha()
player = Player(all_sprites)

# custom event -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

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
    collisions()
    display_surface.fill("#6415B8")

    all_sprites.draw(display_surface)
    display_score()

    # draw test
    # pygame.draw.line(display_surface, "black", (0, 0), player.rect.center, 5)
    # pygame.draw.rect(display_surface, "red", player.rect, 5, 5)

    pygame.display.update()

pygame.quit()
