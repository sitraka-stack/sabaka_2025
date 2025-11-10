import pygame

class Sounds:
    def __init__(self):
        self.jump_sound = pygame.mixer.Sound("assets/sounds/jump_sound.wav")
        self.fail_sound = pygame.mixer.Sound("assets/sounds/fail.wav")

    def play_jump(self):
        self.jump_sound.play()

    def play_fail(self):
        self.fail_sound.play()