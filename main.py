import pygame
import player_select_screen
import end_screen
from splash_screen import show_splash_screen
from player import Player
from board import Board
from game import Game
from token import Token




def run_game(screen, player_choices):
    # Prépare les joueurs et le plateau
    p1 = player_choices["players"][0]
    p2 = player_choices["players"][1]

    board = Board()
    players = []

    player1 = Player(1, p1["img"], "assets/token1.png", board, name=p1["name"], color=p1["color"])
    player1.token = Token("assets/token1.png", 1, board)
    players.append(player1)

    player2 = Player(2, p2["img"], "assets/token2.png", board, name=p2["name"], color=p2["color"])
    player2.token = Token("assets/token2.png", 1, board)
    players.append(player2)

    pygame.display.set_caption("Sabaka Maro - Marelle")
    game = Game(screen, players)
    clock = pygame.time.Clock()
    running = True

    winner = None

    while running:
        running = game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)
        # --- Détecter la victoire : Game doit définir game.winner quand il y a un gagnant
        if getattr(game, "winner", None) is not None:
            winner = game.winner
            running = False

    # Affiche l'écran de fin de partie, retourne "replay" ou "quit"
    action = end_screen.show_end_screen(screen, winner_name=winner)
    return action

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((750, 600))
    # === Musique de fond continue ===
    pygame.mixer.music.load("assets/sounds/background1.mp3")  # Chemin de ta musique
    pygame.mixer.music.set_volume(0.065)  # Ajuste le volume si besoin
    pygame.mixer.music.play(-1)  # -1 = boucle infinie

    show_splash_screen(screen)
    player_choices = player_select_screen.show_player_select_screen(screen)
    if player_choices is None:
        pygame.quit()
        exit()

    while True:
        action = run_game(screen, player_choices)
        if action == "replay":
            continue
        elif action == "quit":
            break
    pygame.quit()

if __name__ == "__main__":
    main()