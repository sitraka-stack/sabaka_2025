import pygame
import random
import math

def show_win_animation(screen, winner_id):
    clock = pygame.time.Clock()
    # Police moderne, ou fallback
    try:
        font_big = pygame.font.SysFont("segoeuisemibold", 70, bold=True)
        font_glow = pygame.font.SysFont("segoeuisemibold", 70, bold=True)
        font_small = pygame.font.SysFont("segoeui", 34, bold=True)
    except:
        font_big = pygame.font.SysFont("arial", 70, bold=True)
        font_glow = pygame.font.SysFont("arial", 70, bold=True)
        font_small = pygame.font.SysFont("arial", 34, bold=True)

    duration = 5  # secondes
    t0 = pygame.time.get_ticks()

    # Confettis (x, y, couleur, rayon, vitesse)
    confettis = [
        [
            random.randint(0, screen.get_width()),
            random.randint(-400, -10),
            random.choice([
                (255, 0, 0), (255, 200, 0), (0, 180, 255),
                (0, 255, 120), (255, 0, 170), (255, 255, 0),
                (255, 150, 50), (0, 255, 255), (180, 0, 255)
            ]),
            random.randint(5, 11),
            random.randint(4, 9)
        ] for _ in range(130)
    ]

    running = True
    while running:
        screen.fill((250, 247, 255))

        elapsed = (pygame.time.get_ticks() - t0) / 1000
        # Animation pop : le texte grandit légèrement puis revient à la taille normale
        pop_scale = 1.0 + 0.13 * math.exp(-2*elapsed) * math.sin(8 * elapsed)

        # Texte avec effet glow
        winner_text = f" Joueur {winner_id} a gagné ! "
        center = (screen.get_width()//2, 210)
        # Glow
        for glow_radius in [8, 5, 2]:
            glow_surface = font_glow.render(winner_text, True, (140, 102, 255))
            glow_rect = glow_surface.get_rect(center=center)
            glow_surface = pygame.transform.smoothscale(
                glow_surface,
                (int(glow_rect.width * (1 + glow_radius*0.04 * pop_scale)),
                 int(glow_rect.height * (1 + glow_radius*0.04 * pop_scale)))
            )
            screen.blit(glow_surface, glow_surface.get_rect(center=center))
        # Texte principal
        text_surface = font_big.render(winner_text, True, (44, 6, 120))
        text_surface = pygame.transform.smoothscale(
            text_surface,
            (int(text_surface.get_width() * pop_scale), int(text_surface.get_height() * pop_scale))
        )
        screen.blit(text_surface, text_surface.get_rect(center=center))

        # Sous-texte
        subtext = "Bravo !"
        msg = font_small.render(subtext, True, (50, 170, 60))
        msg2 = font_small.render(subtext, True, (255,255,255))
        msg_rect = msg.get_rect(center=(screen.get_width()//2, 285))
        # Ombre du sous-texte
        screen.blit(msg2, msg_rect.move(2,2))
        screen.blit(msg, msg_rect)

        # Confettis
        for c in confettis:
            pygame.draw.circle(screen, c[2], (int(c[0]), int(c[1])), c[3])
            c[1] += c[4]
            if c[1] > screen.get_height():
                c[0] = random.randint(0, screen.get_width())
                c[1] = random.randint(-250, -20)
                c[2] = random.choice([
                    (255, 0, 0), (255, 200, 0), (0, 180, 255),
                    (0, 255, 120), (255, 0, 170), (255, 255, 0),
                    (255, 150, 50), (0, 255, 255), (180, 0, 255)
                ])
                c[3] = random.randint(5, 11)
                c[4] = random.randint(4, 9)

        pygame.display.flip()
        clock.tick(60)

        # Quit ou 3 secondes écoulées
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if pygame.time.get_ticks() - t0 > duration * 1000:
            running = False