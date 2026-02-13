import pygame
import sys
import os
from game.sounds import SoundManager
from game.images import ImageManager

sound_manager = SoundManager()
Image_manager = ImageManager()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE  = (0, 100, 255)
clock = pygame.time.Clock()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)



def game_over_menu(screen):
    if not pygame.font.get_init():
        pygame.font.init()

    font = pygame.font.Font(None, 48)

    SCREAMER_TIMEOUT = pygame.USEREVENT + 1

    screamer_img_path = _root_path("images", "screamer.png")

    # Música Game Over
    sound_manager.play_gameover_theme()
    # Sonido Screamer
    screamer_sound = sound_manager.load_screamer_sound()

    WIDTH, HEIGHT = screen.get_size()
    screamer_shown = False
    screamer_active = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound_manager.stop_all_music()
                pygame.quit()
                sys.exit()

            # Cuando la música termina, mostramos el screamer
            if not pygame.mixer.music.get_busy() and not screamer_shown:
                if os.path.exists(screamer_img_path):
                    img = pygame.image.load(screamer_img_path).convert()
                    img = pygame.transform.scale(img, (WIDTH, HEIGHT))
                    screen.blit(img, (0, 0))
                    pygame.display.flip()
                    screamer_active = True

                if screamer_sound:
                    screamer_sound.play()

                # Lanzamos un temporizador de 10 segundos
                pygame.time.set_timer(SCREAMER_TIMEOUT, 10000)
                screamer_shown = True

            elif event.type == SCREAMER_TIMEOUT:
                pygame.time.set_timer(SCREAMER_TIMEOUT, 0)  # detener el timer
                screamer_active = False
                if screamer_sound:
                    screamer_sound.stop()
                sound_manager.stop_all_music()
                pygame.mixer.stop()
                return "menu_principal"

            elif event.type == pygame.MOUSEBUTTONDOWN and not screamer_active:
                if restart_button.collidepoint(event.pos):
                    if screamer_sound:
                        screamer_sound.stop()
                    sound_manager.stop_all_music()
                    pygame.mixer.stop()
                    return "reiniciar"

                if menu_button.collidepoint(event.pos):
                    if screamer_sound:
                        screamer_sound.stop()
                    sound_manager.stop_all_music()
                    pygame.mixer.stop()
                    return "menu_principal"

                if exit_button.collidepoint(event.pos):
                    if screamer_sound:
                        screamer_sound.stop()
                    sound_manager.stop_all_music()
                    pygame.quit()
                    sys.exit()

        # Si no está activo el screamer, dibujamos el menú normal
        if not screamer_active:
            screen.fill(BLACK)
            draw_text("GAME OVER", font, WHITE, screen, WIDTH // 2, 60)

            restart_button = pygame.Rect(30, 120, 260, 50)
            menu_button    = pygame.Rect(30, 190, 260, 50)
            exit_button    = pygame.Rect(30, 260, 260, 50)

            pygame.draw.rect(screen, BLUE, restart_button)
            pygame.draw.rect(screen, BLUE, menu_button)
            pygame.draw.rect(screen, BLUE, exit_button)

            draw_text("Reiniciar", font, WHITE, screen, WIDTH // 2, 145)
            draw_text("Menú Principal", font, WHITE, screen, WIDTH // 2, 215)
            draw_text("Salir", font, WHITE, screen, WIDTH // 2, 285)

        pygame.display.flip()
        clock.tick(60)