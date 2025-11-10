#game.py
import pygame

from board import Board
from timing_bar import TimingBar
from sounds import Sounds
import win_anim
import  random




GOOD_TIMING_COMMENTS = [
    "Timing parfait ! Tu as mangé un chrono ce matin ?",
    "Wouah, c’est du grand art !",
    "On dirait que tu as un métronome intégré !",
    "Incroyable, tu es dans le tempo !",
    "On t’appelle Maestro Timing !",
    "Tu l'as dans le sang"
]
ALMOST_TIMING_COMMENTS = [
    "Pas mal, mais tu peux faire mieux !",
    "C’est presque ça, continue !",
    "Ça passe, mais c’était un peu chaud !",
    "On sent que tu vises la perfection !",
    "Un peu plus vite ou plus lentement la prochaine fois !"
]
FAIL_TIMING_COMMENTS = [
    "Ouch, tu as raté le coche !",
    "Le timing, c’est comme le fromage, ça se travaille !",
    "Aïe, ça pique !",
    "Essaie encore, Rome ne s’est pas faite en un jour !",
    "Si tu visais à côté, c’est réussi !"
]



class Game:
    def __init__(self, screen, players):
        self.screen = screen
        self.board = Board()
        self.players = players
        self.current_player = 0
        self.state = "move_to_token"  # Autres états : jump_timing, pick_token, throw_token, move_to_end, return_to_base
        self.timing_bar = TimingBar((self.screen.get_width() // 2 - 125, 500), (250, 18))
        self.sounds = Sounds()
        self.next_case = None  # La case visée par le saut
        self.last_timing_quality = None
        self.last_timing_comment = ""
        self.winner = None
    def draw_timing_legend(self):
        # Position de la frise à droite de l'écran
        x = self.screen.get_width() - 200
        y = 60
        r = 12  # rayon du cercle couleur
        font = pygame.font.SysFont("segoeuisemibold", 24, bold=True)
        infos = [
            ((40, 200, 60), "Bon timing", "Vert"),
            ((230, 150, 30), "Assez bon", "Orange"),
            ((200, 40, 40), "Switch à l'autre", "Rouge")
        ]
        for i, (color, label, desc) in enumerate(infos):
            pygame.draw.circle(self.screen, color, (x, y + i * 60), r)
            txt = font.render(label, True, (0, 0, 0))
            self.screen.blit(txt, (x + r + 10, y - 12 + i * 60))
            descfont = pygame.font.SysFont("segoeuisemibold", 20)
            self.screen.blit(descfont.render(desc, True, color), (x + r + 10, y + 12 + i * 60))
        # Titre
        font_title = pygame.font.SysFont(None, 26, bold=True)
        self.screen.blit(font_title.render("Action timing :", True, (0, 0, 0)), (x - 8, y - 36))
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            player = self.players[self.current_player]

            # --- Déclencher un saut (on demande le timing) ---
            if self.state in ["move_to_token", "move_to_end", "return_to_base"] and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Détermine la prochaine case selon la phase
                    next_case = None
                    if self.state == "move_to_token" and player.case < player.token.case_num:
                        next_case = player.case + 1
                    elif self.state == "move_to_end" and player.case < 9:
                        next_case = player.case + 1
                        if next_case == player.token.case_num:
                            next_case += 1
                        if next_case > 9:
                            next_case = 9
                    elif self.state == "return_to_base" and player.case > 1:
                        next_case = player.case - 1

                    # Vérifie que la case est valide
                    if next_case is not None and (1 <= next_case <= 9):
                        self.next_case = next_case
                        self.state_before_jump = self.state
                        self.state = "jump_timing"
                        # Difficulté identique pour saut et lancer (timing serré)
                        self.timing_bar.set_difficulty(3)
                        self.timing_bar.ideal_width = int(self.timing_bar.width * 0.1)
                        self.timing_bar.reset()
                    else:
                        # Fin de phase, passer à l’étape suivante
                        if self.state == "move_to_token":
                            self.state = "pick_token"
                        elif self.state == "move_to_end":
                            self.state = "return_to_base"
                        elif self.state == "return_to_base":
                            if player.token.case_num == 9:
                                pygame.mixer.Sound("assets/audio_win.wav").play()
                                win_anim.show_win_animation(self.screen, player.id)
                                self.winner = player.name  # ou player.id, ou ce que tu veux afficher
                            self.state = "move_to_token"
                        # Pas de next_turn ici, le joueur garde son tour après un aller-retour réussi

            # --- Phase de timing du saut ---
            elif self.state == "jump_timing" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.timing_bar.stop()
                    timing_quality = self.timing_bar.get_timing_quality()
                    # Ajout du commentaire
                    if timing_quality == "good":
                        self.last_timing_comment = random.choice(GOOD_TIMING_COMMENTS)
                    elif timing_quality == "almost":
                        self.last_timing_comment = random.choice(ALMOST_TIMING_COMMENTS)
                    else:
                        self.last_timing_comment = random.choice(FAIL_TIMING_COMMENTS)
                    self.last_timing_quality = timing_quality
                    # DEBUG: print(f"Timing quality: {timing_quality}")
                    if timing_quality in ("good", "almost"):
                        player.move_to_case(self.next_case)
                        self.sounds.play_jump()
                        # Retour à la phase précédente ou passage à l’étape suivante
                        if self.state_before_jump == "move_to_token" and player.case == player.token.case_num:
                            self.state = "pick_token"
                        elif self.state_before_jump == "move_to_end" and player.case == 9:
                            self.state = "return_to_base"
                        elif self.state_before_jump == "return_to_base" and player.case == 1:
                            if player.token.case_num == 9:
                                pygame.mixer.Sound("assets/audio_win.wav").play()
                                win_anim.show_win_animation(self.screen, player.id)
                                self.winner = player.name  # ou player.id, ou ce que tu veux afficher
                            self.state = "move_to_token"
                            # Le joueur garde son tour après un aller-retour complet
                        else:
                            self.state = self.state_before_jump
                    else:
                        self.sounds.play_fail()
                        self.next_turn()

            # --- Ramasser le jeton ---
            elif self.state == "pick_token" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.has_token = True
                    self.state = "throw_token"
                    # Difficulté identique pour le lancer
                    self.timing_bar.set_difficulty(3)
                    self.timing_bar.ideal_width = int(self.timing_bar.width * 0.1)
                    self.timing_bar.reset()

            # --- Timing pour lancer le jeton ---
            elif self.state == "throw_token" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.timing_bar.stop()
                    timing_quality = self.timing_bar.get_timing_quality()
                    # Ajout du commentaire
                    if timing_quality == "good":
                        self.last_timing_comment = random.choice(GOOD_TIMING_COMMENTS)
                    elif timing_quality == "almost":
                        self.last_timing_comment = random.choice(ALMOST_TIMING_COMMENTS)
                    else:
                        self.last_timing_comment = random.choice(FAIL_TIMING_COMMENTS)
                    self.last_timing_quality = timing_quality

                    if timing_quality in ("good", "almost"):
                        target_case = player.token.case_num + 1
                        if target_case > 9:
                            target_case = 9
                        player.token.move_to_case(target_case)
                        self.sounds.play_jump()
                        player.has_token = False
                        if player.token.case_num == 9:
                            pygame.mixer.Sound("assets/audio_win.wav").play()
                            win_anim.show_win_animation(self.screen, player.id)
                            self.winner = player.name  # ou player.id, ou ce que tu veux afficher
                        self.state = "move_to_end"
                        player.move_to_case(player.case + 1)
                    else:
                        self.sounds.play_fail()
                        self.next_turn()
        return True

    def next_turn(self):
        self.current_player = (self.current_player + 1) % 2
        self.state = "move_to_token"
        self.timing_bar.set_difficulty(3)  # Ex : 12 = rapide (à tester selon ta classe TimingBar)
        self.timing_bar.ideal_width = int(self.timing_bar.width * 0.1)  # Zone verte étroite (8% de la barre)
        self.timing_bar.reset()

    def update(self):
        if self.state in ["throw_token", "jump_timing"]:
            self.timing_bar.draw(self.screen)
            self.timing_bar.update()

    def draw(self):
        self.screen.fill((200, 230, 255))
        self.board.draw(self.screen)

        # 1. DESSIN DES JETONS (AVANT les pions)
        for player in self.players:
            if hasattr(player, "token") and player.token:
                player.token.draw(self.screen)

        # 2. DESSIN DES PIONS
        for idx, player in enumerate(self.players):
            player.draw(self.screen, active=(idx == self.current_player))

        font = pygame.font.SysFont(None, 28)
        for idx, player in enumerate(self.players):
            display_name = player.name if hasattr(player, "name") and player.name else f"J{idx + 1}"
            txt = font.render(f"{display_name} : case {player.case}, jeton: {player.token.case_num}", True, (0, 0, 0))
            y = 10 + 30 * idx

            # Curseur graphique pour le joueur courant
            if idx == self.current_player:
                color = (60, 30, 120)  # ou player.color
                pygame.draw.polygon(
                    self.screen,
                    color,
                    [
                        (0, y + 12),  # pointe gauche
                        (18, y + 4),  # haut droit
                        (18, y + 20),  # bas droit
                    ]
                )
            self.screen.blit(txt, (25, y))
        if self.state in ["throw_token", "jump_timing"]:
            # Indication au-dessus du timing
            font = pygame.font.SysFont(None, 28, bold=True)
            if self.state == "jump_timing":
                txt = "Timing pour le saut"
            elif self.state == "throw_token":
                txt = "Timing pour le lancer du jeton"
            else:
                txt = ""
            if txt:
                bar_x, bar_y = self.timing_bar.x, self.timing_bar.y
                bar_w = self.timing_bar.width
                text_surf = font.render(txt, True, (60, 30, 120))
                self.screen.blit(text_surf, (bar_x + (bar_w - text_surf.get_width()) // 2, bar_y - 36))

            self.timing_bar.draw(self.screen)
            # Commentaire sous la barre
            if self.last_timing_comment:
                font = pygame.font.SysFont(None, 26, bold=True)
                color = (40, 200, 60) if self.last_timing_quality == "good" else \
                    (230, 150, 30) if self.last_timing_quality == "almost" else \
                        (200, 40, 40)
                text = font.render(self.last_timing_comment, True, color)
                bar_x, bar_y = self.timing_bar.x, self.timing_bar.y
                bar_w, bar_h = self.timing_bar.width, self.timing_bar.height
                self.screen.blit(text, (bar_x + (bar_w - text.get_width()) // 2, bar_y + bar_h + 12))
        self.draw_timing_legend()
        pygame.display.flip()