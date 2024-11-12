import pygame


class AutoShootButtonUI:
    def __init__(self, surface):
        self.display_surface = surface
        self.button_rect = pygame.Rect(50, 50, 100, 50)
        self.button_active = False
        self.button_color = {True: (0, 255, 0), False: (255, 0, 0)}

        # cooldown
        self.can_toggle = True
        self.toggle_timer = 0
        self.toggle_cooldown = 500

        # font
        self.font = pygame.font.Font(None, 30)

    def draw(self):
        pygame.draw.rect(
            self.display_surface,
            self.button_color[self.button_active],
            self.button_rect,
        )
        pygame.draw.rect(self.display_surface, (0, 0, 0), self.button_rect, 2)

        # Render text based on button state
        text = "ON" if self.button_active else "OFF"
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_frect(center=self.button_rect.center)
        self.display_surface.blit(text_surface, text_rect)

    def toggle_button(self, mouse_position):
        if self.button_rect.collidepoint(mouse_position) and self.can_toggle:
            self.button_active = not self.button_active
            self.can_toggle = False
            self.toggle_timer = pygame.time.get_ticks()

    def update(self):
        if not self.can_toggle:
            current_time = pygame.time.get_ticks()
            if current_time - self.toggle_timer >= self.toggle_cooldown:
                self.can_toggle = True
