import pygame

# Dimensions de la case et espacements
CASE_SIZE = 68
CASE_SPACING = 10
CIEL_WIDTH = 110
CIEL_HEIGHT = 74

# Calcul de la position de la première case pour tout centrer verticalement
START_X = 300  # centre horizontal
START_Y = 80

# Définition des positions pour une marelle classique

CASES = [
    {"num": 1, "pos": (START_X, START_Y + (CASE_SIZE + CASE_SPACING) * 6)},  # 1
    {"num": 2, "pos": (START_X, START_Y + (CASE_SIZE + CASE_SPACING) * 5)},  # 2
    {"num": 3, "pos": (START_X - CASE_SIZE // 1.5, START_Y + (CASE_SIZE + CASE_SPACING) * 4)},  # 3 gauche
    {"num": 4, "pos": (START_X + CASE_SIZE // 1.5, START_Y + (CASE_SIZE + CASE_SPACING) * 4)},  # 4 droite
    {"num": 5, "pos": (START_X, START_Y + (CASE_SIZE + CASE_SPACING) * 3)},  # 5
    {"num": 6, "pos": (START_X - CASE_SIZE // 1.5, START_Y + (CASE_SIZE + CASE_SPACING) * 2)},  # 6 gauche
    {"num": 7, "pos": (START_X + CASE_SIZE // 1.5, START_Y + (CASE_SIZE + CASE_SPACING) * 2)},  # 7 droite
    {"num": 8, "pos": (START_X, START_Y + (CASE_SIZE + CASE_SPACING) * 1)},  # 8 (simple, centrée)
    {"num": "Ciel", "pos": (START_X, START_Y)},  # Ciel
]
class Board:
    def __init__(self):
        self.cases = CASES
        self.size = CASE_SIZE

    def draw(self, screen):
        for case in self.cases:
            x, y = case["pos"]

            if case["num"] == "Ciel":
                # Case "Ciel" : rectangle arrondi, plus large et plus haut
                shadow_offset = 6
                border_radius = 28
                rect = pygame.Rect(
                    x - CIEL_WIDTH // 2, y - CIEL_HEIGHT // 2, CIEL_WIDTH, CIEL_HEIGHT
                )
                # Ombre
                shadow_rect = rect.move(shadow_offset, shadow_offset)
                pygame.draw.rect(screen, (180, 200, 210), shadow_rect, border_radius=border_radius)
                # Remplissage
                pygame.draw.rect(screen, (230, 235, 255), rect, border_radius=border_radius)
                # Contour
                pygame.draw.rect(screen, (70, 79, 76), rect, width=5, border_radius=border_radius)
                # Texte centré
                font = pygame.font.SysFont(None, 48, bold=True)
                txt = font.render(str(case["num"]), True, (40, 40, 110))
                txtr = txt.get_rect(center=rect.center)
                screen.blit(txt, txtr)
            else:
                # Cases normales : carré arrondi avec ombre
                shadow_offset = 4
                border_radius = 16
                rect = pygame.Rect(
                    x - CASE_SIZE // 2, y - CASE_SIZE // 2, CASE_SIZE, CASE_SIZE
                )
                # Ombre douce
                shadow_rect = rect.move(shadow_offset, shadow_offset)
                pygame.draw.rect(screen, (180, 200, 210), shadow_rect, border_radius=border_radius)
                # Remplissage
                pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=border_radius)
                # Contour
                pygame.draw.rect(screen, (70, 79, 76), rect, width=4, border_radius=border_radius)
                # Texte centré
                font = pygame.font.SysFont(None, 36, bold=True)
                txt = font.render(str(case["num"]), True, (30, 30, 30))
                txtr = txt.get_rect(center=rect.center)
                screen.blit(txt, txtr)

