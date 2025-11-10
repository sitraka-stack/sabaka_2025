import pygame
import sys



def show_splash_screen(screen):
    # --- Charger l'image de background ---
    try:
        bg_img = pygame.image.load("assets/background.jpg").convert()
        # Redimensionne pour remplir l'écran (optionnel)
        bg_img = pygame.transform.scale(bg_img, (screen.get_width(), screen.get_height()))
    except Exception as e:
        print("⚠️ Impossible de charger le background :", e)
        bg_img = None
    #---------Logo
    try:
        logo_img = pygame.image.load("assets/banner.png").convert_alpha()
        logo_img = pygame.transform.smoothscale(logo_img, (240, 240))  # adapte la taille si besoin
    except Exception as e:
        print("⚠️ Impossible de charger le logo :", e)
        logo_img = None
    # Police stylée ou fallback
    try:
        font_title = pygame.font.SysFont("segoeuisemibold", 72, bold=True)
        font_sub = pygame.font.SysFont("segoeui", 34, bold=True)
    except:
        font_title = pygame.font.SysFont("arial", 72, bold=True)
        font_sub = pygame.font.SysFont("arial", 34, bold=True)

    clock = pygame.time.Clock()
    running = True
    pulse = 0

    # Charge un son court (wav, ogg, mp3 selon pygame version)
    # Place un fichier "enter.wav" dans ton dossier assets !
    enter_sound = None

    try:
        enter_sound = pygame.mixer.Sound("assets/sounds/enter.wav")
    except Exception:
        print("⚠️ Impossible de charger le son 'enter.wav'")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if enter_sound:
                    enter_sound.play()
                pygame.time.wait(400)  # petit délai pour entendre le son
                running = False
        # --- Affiche le fond d'écran ---
        if bg_img:
            screen.blit(bg_img, (0, 0))
        else:
            screen.fill((192, 210, 255))

        # --- AFFICHE LE LOGO ---
        if logo_img:
            logo_rect = logo_img.get_rect(center=(screen.get_width() // 2, 100))
            screen.blit(logo_img, logo_rect)



        # Titre avec effet glow
        title = "Marelle Party"
        for glow in [8, 4, 2]:
            glow_surf = font_title.render(title, True, (120, 100, 210))
            glow_surf = pygame.transform.smoothscale(
                glow_surf,
                (int(glow_surf.get_width() * (1 + glow * 0.01)), int(glow_surf.get_height() * (1 + glow * 0.01)))
            )
            glow_rect = glow_surf.get_rect(center=(screen.get_width()//2, 190))
            screen.blit(glow_surf, glow_rect)
        text = font_title.render(title, True, (54, 10, 120))
        screen.blit(text, text.get_rect(center=(screen.get_width()//2, 190)))

        # Sous-titre avec effet “pulse”
        pulse = 0.5 * pygame.time.get_ticks() // 500 % 2 - 0.5
        sub = "Appuie sur [Entrée] pour jouer"
        color = (100, 130, 200) if abs(pulse) < 0.25 else (54, 0, 120)
        sub_surf = font_sub.render(sub, True, color)
        scale = 1.04 + 0.04 * abs(pulse)
        sub_surf = pygame.transform.smoothscale(sub_surf, (int(sub_surf.get_width() * scale), int(sub_surf.get_height() * scale)))
        sub_rect = sub_surf.get_rect(center=(screen.get_width()//2, 290))
        screen.blit(sub_surf, sub_rect)

        # Footer
        font_footer = pygame.font.SysFont("arial", 20)
        footer = font_footer.render("© 2025 Sabaka Group", True, (100, 100, 110))
        screen.blit(footer, (10, screen.get_height() - 28))

        pygame.display.flip()
        clock.tick(60)