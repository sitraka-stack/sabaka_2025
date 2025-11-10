#end_screen.py
import pygame
import sys
pygame.init()
pygame.mixer.init()

sound_replay = pygame.mixer.Sound("assets/sounds/enter.wav")  # mets le chemin correct de ton son
def show_end_screen(screen, winner_name=None):
    clock = pygame.time.Clock()
    font_title = pygame.font.SysFont(None, 54, bold=True)
    font_button = pygame.font.SysFont(None, 36, bold=True)
    font_info = pygame.font.SysFont(None, 28)
    running = True

    # Boutons
    button_w, button_h = 180, 60
    replay_rect = pygame.Rect(screen.get_width()//2 - button_w - 20, 330, button_w, button_h)
    quit_rect = pygame.Rect(screen.get_width()//2 + 20, 330, button_w, button_h)

    # Message de victoire
    if winner_name:
        title = f"{winner_name} a gagné !"
    else:
        title = "Fin de la partie !"

    while running:
        screen.fill((210, 230, 255))

        # Titre
        title_surf = font_title.render(title, True, (50, 30, 130))
        screen.blit(title_surf, (screen.get_width()//2 - title_surf.get_width()//2, 120))

        # Bouton Rejouer
        pygame.draw.rect(screen, (100, 210, 120), replay_rect, border_radius=15)
        replay_surf = font_button.render("Rejouer", True, (30, 60, 20))
        screen.blit(replay_surf, (replay_rect.centerx - replay_surf.get_width()//2, replay_rect.centery - replay_surf.get_height()//2))

        # Bouton Quitter
        pygame.draw.rect(screen, (212, 120, 120), quit_rect, border_radius=15)
        quit_surf = font_button.render("Quitter", True, (60, 20, 20))
        screen.blit(quit_surf, (quit_rect.centerx - quit_surf.get_width()//2, quit_rect.centery - quit_surf.get_height()//2))

        # Message d'info
        info_surf = font_info.render("Merci d'avoir joué !", True, (70,70,70))
        screen.blit(info_surf, (screen.get_width()//2 - info_surf.get_width()//2, 250))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if replay_rect.collidepoint(mx, my):
                    sound_replay.play()
                    pygame.time.wait(200)  # petit délai pour entendre le son
                    return "replay"
                elif quit_rect.collidepoint(mx, my):
                    return "quit"
        clock.tick(30)