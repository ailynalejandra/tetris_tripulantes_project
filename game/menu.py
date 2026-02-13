import pygame
import sys
import random
import math
from pathlib import Path
from game.sounds import SoundManager
from game.images import ImageManager
from game.settings import GameSettings

sound_manager = SoundManager()
image_manager = ImageManager(preload=False)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE  = (0, 100, 255)
GRAY  = (200, 200, 200)
clock = pygame.time.Clock()

# Parámetros de efectos
FLASH_DURATION_MS = 30        # flash blanco antes del blackout
BLACKOUT_DURATION_MS = 50    # pantalla negra justo antes del golpe
SCREAMER_VISIBLE_MS = 39000   # tiempo total que la imagen puede estar visible (igual que antes)
SHAKE_INTENSITY = 5          # píxeles máximos de shake
FLICKER_NEXT_MIN = 400       # ms mínimo hasta el siguiente flicker
FLICKER_NEXT_MAX = 1600        # ms máximo hasta el siguiente flicker
FLICKER_DUR_MIN = 60          # ms mínimo que dura un flicker (imagen apagada)
FLICKER_DUR_MAX = 180         # ms máximo que dura un flicker

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def _image_path(filename):
    return Path(GameSettings.IMAGES_DIR).joinpath(filename)

def _try_load_and_scale(path, size):
    try:
        print(f"🔎 Intentando cargar imagen: {path.resolve()}")
    except Exception:
        print(f"🔎 Intentando cargar imagen: {path}")
    if not path.exists():
        print(f"❌ No existe: {path}")
        return None
    try:
        surf = pygame.image.load(str(path))
        try:
            surf = surf.convert_alpha()
        except Exception:
            surf = surf.convert()
        surf = pygame.transform.scale(surf, size)
        print("✅ Imagen cargada y escalada")
        return surf
    except Exception as e:
        print(f"❌ Error cargando imagen {path}: {e}")
        return None

def _blit_with_shake(screen, surf, center, intensity):
    dx = random.randint(-intensity, intensity)
    dy = random.randint(-intensity, intensity)
    rect = surf.get_rect(center=center)
    rect.move_ip(dx, dy)
    screen.blit(surf, rect)

def game_over_menu(screen):
    if not pygame.font.get_init():
        pygame.font.init()

    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 28)
    SCREAMER_TIMEOUT = pygame.USEREVENT + 1
    MUSIC_END_EVENT = pygame.USEREVENT + 2

    WIDTH, HEIGHT = screen.get_size()

    # No cargar en preload; lo haremos justo antes de mostrar
    screamer_surface = None
    base_surface = None

    pygame.mixer.music.set_endevent(MUSIC_END_EVENT)
    sound_manager.play_gameover_theme()

    screamer_shown = False
    screamer_active = False

    # Estados para pre-flash/blackout
    preflash_state = None  # None | "flash" | "blackout" | "done"
    preflash_start = 0

    # Flicker timers
    next_flicker_at = 0
    flicker_end_at = 0
    flicker_off = False

    # Botones
    restart_button = pygame.Rect(30, 120, 260, 50)
    menu_button    = pygame.Rect(30, 190, 260, 50)
    exit_button    = pygame.Rect(30, 260, 260, 50)

    skip_text = "Presiona F para saltarte la cancion"

    while True:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound_manager.stop_all_music()
                pygame.quit()
                sys.exit()

            # Trigger: fin de la música (evento) o tecla F para saltar
            if (event.type == MUSIC_END_EVENT or (event.type == pygame.KEYDOWN and event.key == pygame.K_f)) and not screamer_shown:
                # iniciar secuencia pre-flash -> blackout -> mostrar screamer
                preflash_state = "flash"
                preflash_start = now
                screamer_shown = True
                # precargar la imagen justo ahora (escalada al tamaño actual)
                screamer_path = _image_path("screamer.png")
                base_surface = _try_load_and_scale(screamer_path, (WIDTH, HEIGHT))
                # preparar timers de flicker
                next_flicker_at = now + random.randint(FLICKER_NEXT_MIN, FLICKER_NEXT_MAX)
                flicker_end_at = 0
                flicker_off = False
                # no reproducir aún el screamer; lo haremos tras blackout para sincronizar con el golpe
                continue

            # Temporizador que finaliza la visualización del screamer
            if event.type == SCREAMER_TIMEOUT:
                pygame.time.set_timer(SCREAMER_TIMEOUT, 0)
                screamer_active = False
                # detener sonidos y volver al menú
                sound_manager.stop_all_music()
                pygame.mixer.stop()
                return "menu_principal"

            elif event.type == pygame.MOUSEBUTTONDOWN and not screamer_active:
                if restart_button.collidepoint(event.pos):
                    sound_manager.stop_all_music()
                    pygame.mixer.stop()
                    return "reiniciar"
                if menu_button.collidepoint(event.pos):
                    sound_manager.stop_all_music()
                    pygame.mixer.stop()
                    return "menu_principal"
                if exit_button.collidepoint(event.pos):
                    sound_manager.stop_all_music()
                    pygame.quit()
                    sys.exit()

        # Estado pre-flash / blackout / mostrar
        if preflash_state == "flash":
            # mostrar flash blanco breve
            if now - preflash_start <= FLASH_DURATION_MS:
                screen.fill(WHITE)
                pygame.display.flip()
            else:
                # pasar a blackout
                preflash_state = "blackout"
                preflash_start = now
            # no procesar más hasta que termine la secuencia
            continue

        if preflash_state == "blackout":
            if now - preflash_start <= BLACKOUT_DURATION_MS:
                screen.fill(BLACK)
                pygame.display.flip()
            else:
                # terminar preflash y activar screamer
                preflash_state = "done"
                screamer_active = True
                # reproducir el screamer justo al terminar el blackout
                try:
                    sound_manager.play_screamer()
                except Exception:
                    try:
                        s = sound_manager.load_screamer_sound()
                        if s:
                            s.play()
                    except Exception as e:
                        print("❌ No se pudo reproducir el screamer:", e)
                # lanzar timer para ocultar la imagen después del tiempo definido
                pygame.time.set_timer(SCREAMER_TIMEOUT, SCREAMER_VISIBLE_MS)
                # inicializar flicker timers basados en now (ya hecho al iniciar, pero asegurar)
                next_flicker_at = now + random.randint(FLICKER_NEXT_MIN, FLICKER_NEXT_MAX)
                flicker_end_at = 0
                flicker_off = False
            continue

        # Si el screamer está activo, aplicar flicker y shake al dibujarlo
        if screamer_active:
            # actualizar flicker: si llegó el momento, apagar la imagen por un breve periodo
            if now >= next_flicker_at:
                flicker_off = True
                flicker_end_at = now + random.randint(FLICKER_DUR_MIN, FLICKER_DUR_MAX)
                next_flicker_at = now + random.randint(FLICKER_NEXT_MIN, FLICKER_NEXT_MAX)
            if flicker_off and now >= flicker_end_at:
                flicker_off = False

            # dibujar: si flicker_off True, mostramos pantalla negra (o flash intermitente)
            if flicker_off:
                screen.fill(BLACK)
                # ocasionalmente hacer un micro-flash rojo para más tensión
                if random.random() < 0.08:
                    overlay = pygame.Surface((WIDTH, HEIGHT))
                    overlay.fill((150, 0, 0))
                    overlay.set_alpha(120)
                    screen.blit(overlay, (0, 0))
                pygame.display.flip()
            else:
                # dibujar la imagen con shake
                if base_surface:
                    _blit_with_shake(screen, base_surface, (WIDTH//2, HEIGHT//2), SHAKE_INTENSITY)
                    pygame.display.flip()
                else:
                    # fallback visual si no hay imagen
                    screen.fill(BLACK)
                    draw_text("SCREAMER NO DISPONIBLE", font, (255, 0, 0), screen, WIDTH//2, HEIGHT//2)
                    pygame.display.flip()
            # seguir al siguiente frame
            clock.tick(60)
            continue

        # Menú normal si no está activo el screamer
        screen.fill(BLACK)
        draw_text("GAME OVER", font, WHITE, screen, WIDTH // 2, 60)

        pygame.draw.rect(screen, BLUE, restart_button)
        pygame.draw.rect(screen, BLUE, menu_button)
        pygame.draw.rect(screen, BLUE, exit_button)

        draw_text("Reiniciar", font, WHITE, screen, WIDTH // 2, 145)
        draw_text("Menú Principal", font, WHITE, screen, WIDTH // 2, 215)
        draw_text("Salir", font, WHITE, screen, WIDTH // 2, 285)

        if pygame.mixer.music.get_busy() and not screamer_shown:
            draw_text(skip_text, small_font, GRAY, screen, WIDTH // 2, HEIGHT - 40)

        pygame.display.flip()
        clock.tick(60)