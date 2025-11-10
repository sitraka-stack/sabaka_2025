import pygame


class Player:
    def __init__(self, id, img, token_img, board, name=None, color=None):
        self.id = id
        self.img = img
        self.token_img = token_img
        self.board = board
        self.name = name
        self.color = color
        self.case = 1  # Départ sur la case 1
        self.has_token = False
        self.token = None  # À associer dans main.py après création du Token

    def draw(self, screen, active=False):
        # Position du pion selon la case courante du plateau
        if 1 <= self.case <= len(self.board.cases):
            x, y = self.board.cases[self.case - 1]["pos"]
        else:
            # Par défaut, place hors plateau ou sur la première case
            x, y = self.board.cases[0]["pos"]

        # Dessine l'image du pion redimensionnée
        try:
            image = pygame.image.load(self.img).convert_alpha()
            image = pygame.transform.smoothscale(image, (48, 48))  # Petite taille
            rect = image.get_rect(center=(x, y))
            screen.blit(image, rect)
        except Exception:
            pygame.draw.circle(screen, self.color or (100, 100, 255), (x, y), 24)

        # Affiche le nom du joueur au-dessus
        if self.name:
            font = pygame.font.SysFont(None, 20, bold=True)
            name_surf = font.render(self.name, True, (0, 0, 0))
            screen.blit(name_surf, (x - name_surf.get_width() // 2, y - 38))

    def move_to_case(self, case_num):
        self.case = case_num