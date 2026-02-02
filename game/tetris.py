import pygame
import random
import os

def run_game(screen):
    # ❗ NO pygame.init() aquí si ya lo haces en main
    # ❗ NO pygame.mixer.init() aquí si ya lo haces en main
    # (si no lo haces en main, puedes activarlos, pero recomiendo hacerlo en main)

    # --------------------
    # Configuración tablero
    # --------------------
    tam_bloque = 30
    columnas = 11
    filas = 20

    MARGEN_SUPERIOR = 60

    pygame.display.set_caption("Tetris")

    # --------------------
    # Colores
    # --------------------
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    ROJO = (255, 0, 0)
    GRIS = (128, 128, 128)

    COLORES = [
        (0, 255, 255),   # I
        (0, 0, 255),     # J
        (255, 165, 0),   # L
        (255, 255, 0),   # O
        (0, 255, 0),     # S
        (128, 0, 128),   # T
        (255, 0, 0)      # Z
    ]

    PIEZAS = [
        [[1, 1, 1, 1]],            # I
        [[1, 1], [1, 1]],          # O
        [[0, 1, 0], [1, 1, 1]],    # T
        [[1, 0, 0], [1, 1, 1]],    # J
        [[0, 0, 1], [1, 1, 1]],    # L
        [[1, 1, 0], [0, 1, 1]],    # S
        [[0, 1, 1], [1, 1, 0]]     # Z
    ]
    


    # --------------------
    # RUTAS (carpeta raíz)
    # --------------------
    # tetris.py está en /game, por eso subimos un nivel
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # ← raíz del proyecto
    SOUND_DIR = os.path.join(BASE_DIR, "sounds")

    # Debug útil:
    # print("BASE_DIR:", BASE_DIR)
    # print("SOUND_DIR:", SOUND_DIR)

    # --------------------
    # Audio
    # --------------------
    

    def load_sound(filename):
        path = os.path.join(SOUND_DIR, filename)
        if not os.path.exists(path):
            print("❌ No existe sound:", path)
            return None
        try:
            return pygame.mixer.Sound(path)
        except Exception as e:
            print("❌ Error cargando sound:", filename, e)
            return None

    # Música de fondo
    
    tetris_theme = os.path.join(SOUND_DIR, "tetris_theme.mp3")
    if os.path.exists(tetris_theme):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(tetris_theme)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
            print("🎵 Música Tetris OK")
        except Exception as e:
            print("❌ Error cargando música:", e)
    else:
        print("❌ No existe música:", tetris_theme)

    # Efectos
    rotate_sound   = load_sound("rotate.flac")
    move_sound     = load_sound("move.mp3")
    soft_drop      = load_sound("soft_drop.wav")
    line_clear     = load_sound("line_clear.mp3")
    gameover_sound = load_sound("gameover.wav")
    final_theme    = load_sound("gameover_theme.mp3")

    for s in [rotate_sound, move_sound, soft_drop, line_clear, gameover_sound, final_theme]:
        if s:
            s.set_volume(0.5)

    # --------------------
    # Fuente
    # --------------------
    font = pygame.font.Font(None, 36)

    # --------------------
    # Funciones
    # --------------------
    def crear_nueva_pieza():
        forma = random.choice(PIEZAS)
        color = random.choice(COLORES)
        return {
            "forma": forma,
            "color": color,
            "x": columnas // 2 - len(forma[0]) // 2,
            "y": 0
        }

    def colision(tablero, pieza):
        for i, fila in enumerate(pieza["forma"]):
            for j, bloque in enumerate(fila):
                if bloque:
                    x = pieza["x"] + j
                    y = pieza["y"] + i

                    if x < 0 or x >= columnas or y >= filas:
                        return True

                    if y >= 0 and tablero[y][x] != 0:
                        return True
        return False

    def unir_pieza(tablero, pieza):
        for i, fila in enumerate(pieza["forma"]):
            for j, bloque in enumerate(fila):
                if bloque:
                    tablero[pieza["y"] + i][pieza["x"] + j] = pieza["color"]

    # ✅ corregido: elimina SOLO filas completas
    def borrar_lineas(tablero):
        nuevas = []
        lineas_borradas = 0

        for fila in tablero:
            if all(v != 0 for v in fila):
                lineas_borradas += 1
            else:
                nuevas.append(fila)

        while len(nuevas) < len(tablero):
            nuevas.insert(0, [0] * columnas)

        return nuevas, lineas_borradas

    def rotar_pieza(pieza):
        pieza["forma"] = [list(row) for row in zip(*pieza["forma"][::-1])]
        return pieza

    # --------------------
    # Variables
    # --------------------
    tablero = [[0] * columnas for _ in range(filas)]
    pieza_actual = crear_nueva_pieza()

    reloj = pygame.time.Clock()
    tiempo_caida = 500
    ultimo_movimiento = pygame.time.get_ticks()

    game_over = False
    puntaje = 0
    pausa = False

    

    # --------------------
    # Bucle principal
    # --------------------
    while not game_over:
        screen.fill(NEGRO)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "quit"

            if event.type == pygame.KEYDOWN:
                # Pausa
                if event.key == pygame.K_p:
                    pausa = not pausa

                if pausa:
                    continue

                # Movimiento
                if event.key == pygame.K_LEFT:
                    pieza_actual["x"] -= 1
                    if colision(tablero, pieza_actual):
                        pieza_actual["x"] += 1
                    elif move_sound:
                        move_sound.play()

                elif event.key == pygame.K_RIGHT:
                    pieza_actual["x"] += 1
                    if colision(tablero, pieza_actual):
                        pieza_actual["x"] -= 1
                    elif move_sound:
                        move_sound.play()

                elif event.key == pygame.K_DOWN:
                    pieza_actual["y"] += 1
                    if colision(tablero, pieza_actual):
                        pieza_actual["y"] -= 1
                    elif soft_drop:
                        soft_drop.play()

                elif event.key == pygame.K_UP:
                    pieza_actual = rotar_pieza(pieza_actual)
                    if colision(tablero, pieza_actual):
                        # desrotar 3 veces
                        for _ in range(3):
                            pieza_actual = rotar_pieza(pieza_actual)
                    elif rotate_sound:
                        rotate_sound.play()

        # Caída automática
        if not pausa:
            if pygame.time.get_ticks() - ultimo_movimiento > tiempo_caida:
                pieza_actual["y"] += 1

                if colision(tablero, pieza_actual):
                    pieza_actual["y"] -= 1
                    unir_pieza(tablero, pieza_actual)

                    tablero, lineas = borrar_lineas(tablero)

                    # ✅ Puntaje SOLO por líneas
                    if lineas > 0:
                        if line_clear:
                            line_clear.play()

                        if lineas == 1:
                            puntaje += 100
                        elif lineas == 2:
                            puntaje += 300
                        elif lineas == 3:
                            puntaje += 500
                        elif lineas == 4:
                            puntaje += 800

                    pieza_actual = crear_nueva_pieza()

                    if colision(tablero, pieza_actual):
                        game_over = True
                        if gameover_sound:
                            gameover_sound.play()

                ultimo_movimiento = pygame.time.get_ticks()

        # Dibujar tablero
        for y, fila in enumerate(tablero):
            for x, color in enumerate(fila):
                if color != 0:
                    pygame.draw.rect(
                        screen, color,
                        (x * tam_bloque, y * tam_bloque + MARGEN_SUPERIOR, tam_bloque, tam_bloque)
                    )
                    pygame.draw.rect(
                        screen, GRIS,
                        (x * tam_bloque, y * tam_bloque + MARGEN_SUPERIOR, tam_bloque, tam_bloque), 1
                    )

        # Dibujar pieza actual
        for i, fila in enumerate(pieza_actual["forma"]):
            for j, bloque in enumerate(fila):
                if bloque:
                    pygame.draw.rect(
                        screen, pieza_actual["color"],
                        ((pieza_actual["x"] + j) * tam_bloque,
                         (pieza_actual["y"] + i) * tam_bloque + MARGEN_SUPERIOR,
                         tam_bloque, tam_bloque)
                    )
                    pygame.draw.rect(
                        screen, GRIS,
                        ((pieza_actual["x"] + j) * tam_bloque,
                         (pieza_actual["y"] + i) * tam_bloque + MARGEN_SUPERIOR,
                         tam_bloque, tam_bloque), 1
                    )

        # Puntaje en pantalla
        score_text = font.render(f"Puntaje: {puntaje}", True, BLANCO)
        screen.blit(score_text, (10, 10))

        # Pausa en pantalla
        if pausa:
            pause_text = font.render("PAUSA - Pulsa P", True, ROJO)
            screen.blit(pause_text, (10, 35))

        pygame.display.flip()
        reloj.tick(60)

    # Final del juego
    pygame.mixer.music.stop()
    if final_theme:
        final_theme.play()

    # Konami code: define la secuencia y la función de comprobación
konami_code = [
    pygame.K_UP, pygame.K_UP,
    pygame.K_DOWN, pygame.K_DOWN,
    pygame.K_LEFT, pygame.K_RIGHT,
    pygame.K_LEFT, pygame.K_RIGHT,
    pygame.K_b, pygame.K_a
]
input_sequence = []

def check_konami(event, screen):
    """
    Llamar desde el bucle de eventos: check_konami(event, screen)
    Cuando se detecta la secuencia completa llama a activar_easter_egg(screen).
    """
    if event.type == pygame.KEYDOWN:
        input_sequence.append(event.key)
        if len(input_sequence) > len(konami_code):
            input_sequence.pop(0)
        if input_sequence == konami_code:
            input_sequence.clear()
            activar_easter_egg(screen)

import pygame
import itertools

pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Konami Code Easter Egg")

# --- Recursos ---
font = pygame.font.SysFont("Arial", 40, bold=True)
colors_cycle = itertools.cycle([(255,0,0), (0,255,0), (0,0,255), (255,255,0)])
image = pygame.image.load("images/secret.png")
image_rect = image.get_rect(center=(WIDTH//2, HEIGHT//2))
pygame.mixer.music.load("sounds/secret_music.mp3")

# --- Estado ---
easter_active = False
clock = pygame.time.Clock()

# --- Función del Easter Egg ---
def activar_easter_egg(screen):
    global easter_active
    easter_active = True
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()

def desactivar_easter_egg():
    global easter_active
    easter_active = False
    pygame.mixer.music.stop()

# --- Konami Code ---
konami_code = [
    pygame.K_UP, pygame.K_UP,
    pygame.K_DOWN, pygame.K_DOWN,
    pygame.K_LEFT, pygame.K_RIGHT,
    pygame.K_LEFT, pygame.K_RIGHT,
    pygame.K_b, pygame.K_a
]
input_sequence = []

def check_konami(event, screen):
    global input_sequence
    if event.type == pygame.KEYDOWN:
        input_sequence.append(event.key)
        if len(input_sequence) > len(konami_code):
            input_sequence.pop(0)
        if input_sequence == konami_code:
            input_sequence.clear()
            activar_easter_egg(screen)

# --- Bucle principal ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        check_konami(event,screen)

        # Tecla ESC para desactivar
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            desactivar_easter_egg()

    screen.fill((0,0,0))

    if easter_active:
        # Imagen centrada
        screen.blit(image, image_rect)

        # Texto dinámico
        color = next(colors_cycle)
        text = font.render("¡Easter Egg Activado!", True, color)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + 150))
        screen.blit(text, text_rect)
 

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
    
    