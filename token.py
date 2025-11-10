#token.py
import pygame

class Token:
    def __init__(self, image_path, case_num, board):
        self.case_num = case_num  # numéro de la case sur laquelle repose le jeton
        self.board = board
        img = pygame.image.load(image_path)
        # Jeton bien centré, taille adaptée à la case
        self.image = pygame.transform.smoothscale(img, (30, 30))
        self.set_position()

    def set_position(self):
        # Centre le jeton dans la case
        x, y = self.board.cases[self.case_num - 1]["pos"]
        self.x = x - self.image.get_width() // 2
        self.y = y - self.image.get_height() // 2

    def move_to_case(self, case_num):
        self.case_num = case_num
        self.set_position()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))