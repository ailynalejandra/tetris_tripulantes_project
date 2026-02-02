import pygame
import sys
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE  = (0, 100, 255)
clock = pygame.time.Clock()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def _root_path(*paths):
    base = os.path.dirname(os.path.dirname(__file__))  # sale de /game/ a raíz
    return os.path.join(base, *paths)

def stop_all_music():
    """Detiene música y limpia eventos."""
    pygame.mixer.music.stop()
    try:
        pygame.mixer.music.unload()
    except:
        pass
    pygame.mixer.music.set_endevent()  # limpia evento MUSIC_END

def game_over_menu(screen):
    if not pygame.font.get_init():
        pygame.font.init()

    font = pygame.font.Font(None, 48)

    MUSIC_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(MUSIC_END)

    gameover_theme_path = _root_path("sounds", "gameover_theme.mp3")
    screamer_sound_path = _root_path("sounds", "screamer.mp3")
    screamer_img_path   = _root_path("images", "screamer.png")

    # Música Game Over
    if os.path.exists(gameover_theme_path):
        
        pygame.mixer.music.load(gameover_theme_path)
        pygame.mixer.music.play(0)
        pygame.mixer.music.set_volume(0.3)

    screamer_sound = None
    if os.path.exists(screamer_sound_path):
        screamer_sound = pygame.mixer.Sound(screamer_sound_path)

    WIDTH, HEIGHT = screen.get_size()
    screamer_shown = False

    while True:
        screen.fill(BLACK)
        draw_text("GAME OVER", font, WHITE, screen, WIDTH // 2, 60)

        restart_button = pygame.Rect(100, 120, 200, 50)
        menu_button    = pygame.Rect(100, 190, 200, 50)
        exit_button    = pygame.Rect(100, 260, 200, 50)

        pygame.draw.rect(screen, BLUE, restart_button)
        pygame.draw.rect(screen, BLUE, menu_button)
        pygame.draw.rect(screen, BLUE, exit_button)

        draw_text("Reiniciar", font, WHITE, screen, WIDTH // 2, 145)
        draw_text("Menú Principal", font, WHITE, screen, WIDTH // 2, 215)
        draw_text("Salir", font, WHITE, screen, WIDTH // 2, 285)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_all_music()
                pygame.quit()
                sys.exit()

            elif event.type == MUSIC_END and not screamer_shown:
                if os.path.exists(screamer_img_path):
                    img = pygame.image.load(screamer_img_path).convert()
                    img = pygame.transform.scale(img, (WIDTH, HEIGHT))
                    screen.blit(img, (0, 0))
                    pygame.display.flip()

                if screamer_sound:
                    screamer_sound.play()

                pygame.time.wait(10000)  # 10 segundos
                screamer_shown = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    if screamer_sound:
                        screamer_sound.stop()
                    stop_all_music()   # 🔥 detiene el gameover_theme
                    pygame.mixer.music.stop()
                    pygame.mixer.stop()
                    return "reiniciar"

                if menu_button.collidepoint(event.pos):
                    if screamer_sound:
                        screamer_sound.stop()
                    stop_all_music()
                    pygame.mixer.music.stop()
                    pygame.mixer.stop()
                    return "menu_principal"

                if exit_button.collidepoint(event.pos):
                    if screamer_sound:
                        screamer_sound.stop()
                    stop_all_music()
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)