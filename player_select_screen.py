import pygame
pygame.init()
pygame.mixer.init()

sound_play = pygame.mixer.Sound("assets/sounds/enter.wav")


def show_player_select_screen(screen):
    clock = pygame.time.Clock()
    font_title = pygame.font.SysFont(None, 60, bold=True)
    font_sub = pygame.font.SysFont(None, 36, bold=True)
    font_name = pygame.font.SysFont(None, 28, bold=True)
    font_button = pygame.font.SysFont(None, 32, bold=True)

    # Liste de personnages à adapter à ton jeu
    characters = [
        {"name": "L'Alien", "img": "assets/alien.png", "color": (55, 200, 90)},
        {"name": "Arbest", "img": "assets/player.png", "color": (255, 120, 80)},
        {"name": "Gorillya", "img": "assets/monkey.png", "color": (100, 220, 255)},
        {"name": "La Momie", "img": "assets/mummy.png", "color": (230, 190, 80)}
    ]

    selected = [None, None]
    selecting = 0  # 0 pour joueur 1, 1 pour joueur 2

    running = True
    while running:
        screen.fill((240, 238, 255))
        # Titre
        title_surf = font_title.render("Choisissez vos personnages", True, (72, 30, 140))
        screen.blit(title_surf, (screen.get_width() // 2 - title_surf.get_width() // 2, 50))

        # Sous-titre
        sub_surf = font_sub.render(f"Sélection Joueur {selecting+1} :", True, (0, 128, 128))
        screen.blit(sub_surf, (screen.get_width() // 2 - sub_surf.get_width() // 2, 120))

        # Affichage des personnages
        margin_x = 100
        margin_y = 200
        spacing_x = 150
        for i, char in enumerate(characters):
            x = margin_x + i * spacing_x
            y = margin_y
            pygame.draw.rect(screen, (180, 170, 220), (x-10, y-10, 120, 140), 0, border_radius=20)
            try:
                img = pygame.image.load(char["img"]).convert_alpha()
                img = pygame.transform.smoothscale(img, (80, 80))
                img_rect = img.get_rect(center=(x+50, y+45))
                screen.blit(img, img_rect)
            except Exception:
                pygame.draw.circle(screen, char["color"], (x+50, y+45), 36)
            name_surf = font_name.render(char["name"], True, (50, 50, 60))
            screen.blit(name_surf, (x+50 - name_surf.get_width()//2, y+90))

            # Highlight si sélectionné
            if selected[selecting] == i:
                pygame.draw.rect(screen, (72, 30, 140), (x-10, y-10, 120, 140), 4, border_radius=20)

        # Bouton "Jouer !"
        button_rect = pygame.Rect(screen.get_width()//2 - 70, 400, 140, 50)
        can_play = all(sel is not None for sel in selected) and selected[0] != selected[1]
        pygame.draw.rect(screen, (180, 180, 200) if not can_play else (120, 200, 100), button_rect, border_radius=12)
        txt = "Jouer !" if can_play else "Choisir !"
        txt_surf = font_button.render(txt, True, (100, 100, 100) if not can_play else (0, 50, 0))
        screen.blit(txt_surf, (button_rect.centerx - txt_surf.get_width()//2, button_rect.centery - txt_surf.get_height()//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                # Sélection personnage
                for i in range(len(characters)):
                    x = margin_x + i * spacing_x
                    y = margin_y
                    rect = pygame.Rect(x-10, y-10, 120, 140)
                    if rect.collidepoint(mx, my):
                        selected[selecting] = i
                        if selecting == 0:
                            selecting = 1
                        else:
                            selecting = 0
                # Bouton jouer
                if button_rect.collidepoint(mx, my) and can_play :
                    p1 = characters[selected[0]]
                    p2 = characters[selected[1]]
                    sound_play.play()
                    return {"players": [p1, p2]}  # plus de "mode" ici

        clock.tick(50)