import pygame

class TimingBar:
    def __init__(self, pos, size):
        self.x, self.y = pos
        self.width, self.height = size
        self.value = 0
        self.direction = 1
        self.active = True
        self.difficulty = 1  # vitesse de la barre

        # Définition de la zone idéale (20% du centre)
        self.ideal_width = int(self.width * 0.1)
        self.ideal_start = self.x + (self.width - self.ideal_width) // 2
        self.ideal_end = self.ideal_start + self.ideal_width

    def set_difficulty(self, level):
        # Plus le niveau est haut, plus la barre va vite
        self.difficulty = 5 + 4 * level

    def update(self):
        if self.active:
            self.value += self.direction * self.difficulty
            if self.value >= self.width:
                self.value = self.width
                self.direction *= -1
            elif self.value <= 0:
                self.value = 0
                self.direction *= -1

    def draw(self, screen):
        # Fond de barre
        pygame.draw.rect(screen, (60, 63, 60), (self.x, self.y, self.width, self.height))
        # Zone idéale (vert)
        ideal_rect = pygame.Rect(self.ideal_start, self.y, self.ideal_width, self.height)
        surface_ideal = pygame.Surface((self.ideal_width, self.height), pygame.SRCALPHA)
        surface_ideal.fill((0, 255, 0, 80))
        screen.blit(surface_ideal, (self.ideal_start, self.y))
        pygame.draw.rect(screen, (0, 180, 0), ideal_rect, 2)
        # Curseur coloré
        pygame.draw.rect(screen, self.get_cursor_color(), (self.x, self.y, self.value, self.height))
        pygame.draw.line(screen, (0, 0, 0), (self.x + self.value, self.y), (self.x + self.value, self.y + self.height), 2)

    def get_cursor_color(self):
        cursor_pos = self.x + self.value
        if self.ideal_start <= cursor_pos <= self.ideal_end:
            return (0, 220, 0)
        elif (self.ideal_start - 20) <= cursor_pos <= (self.ideal_end + 20):
            return (255, 170, 0)
        else:
            return (255, 50, 50)

    def stop(self):
        self.active = False
        return self.value

    def reset(self):
        self.value = 0
        self.direction = 1
        self.active = True

    def get_timing_quality(self):
        cursor_pos = self.x + self.value
        if self.ideal_start <= cursor_pos <= self.ideal_end:
            return "good"
        elif (self.ideal_start - 20) <= cursor_pos <= (self.ideal_end + 20):
            return "almost"
        else:
            return "fail"