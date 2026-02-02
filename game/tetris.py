import pygame
import random
import os
import itertools

def run_game(screen):
    # ❗ NO pygame.init() aquí si ya lo haces en main
    # ❗ NO pygame.mixer.init() aquí si ya lo haces en main

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
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # ← raíz del proyecto
    SOUND_DIR = os.path.join(BASE_DIR, "sounds")
    IMAGE_DIR = os.path.join(BASE_DIR, "images")

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
    # Recursos Easter Egg
    # --------------------
    secret_image_path = os.path.join(IMAGE_DIR, "secret.png")
    secret_image = pygame.image.load(secret_image_path) if os.path.exists(secret_image_path) else None
    premio_path = os.path.join(IMAGE_DIR, "premio.png")
    premio_image = pygame.image.load(premio_path) if os.path.exists(premio_path) else None
    musica_secreta = os.path.join(SOUND_DIR, "secret_music.mp3")

    KONAMI_CODE = [
        pygame.K_UP, pygame.K_UP,
        pygame.K_DOWN, pygame.K_DOWN,
        pygame.K_LEFT, pygame.K_RIGHT,
        pygame.K_LEFT, pygame.K_RIGHT,
        pygame.K_b, pygame.K_a
    ]
    input_seq = []

    def poner_musica(ruta):
        if os.path.exists(ruta):
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(ruta)
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
            except Exception as e:
                print("❌ Error al reproducir música:", e)

    def ejecutar_easter_egg():
        """Pantalla independiente para el Easter Egg con dos fases y contador de F que desbloquea imagen."""
        poner_musica(musica_secreta)
        colors_cycle = itertools.cycle([(255,0,0), (0,255,0), (0,0,255), (255,255,0)])
        font_grande = pygame.font.Font(None, 60)
        font_mediana = pygame.font.Font(None, 36)
        font_pequena = pygame.font.Font(None, 28)

        inicio = pygame.time.get_ticks()
        fase = 1  # 1 = intro de 5 segundos, 2 = mensaje especial
        f_counter = 0  # contador de veces que se presiona F
        mostrar_premio = False

        # Si queremos que la imagen especial desaparezca tras unos segundos, podemos usar timer_premio
        timer_premio_inicio = None
        DURACION_PREMIO_MS = 5000  # si quieres que el premio se muestre solo 5s; si quieres que quede fija, ignora timers

        while True:
            screen.fill(NEGRO)

            if fase == 1:
                # Imagen secreta y texto dinámico
                if secret_image:
                    rect = secret_image.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
                    screen.blit(secret_image, rect)

                txt = font_grande.render("¡SECRET MODE!", True, next(colors_cycle))
                screen.blit(txt, (screen.get_width()//2 - txt.get_width()//2, 50))

                hint = font_mediana.render("Presiona ESC para volver", True, BLANCO)
                screen.blit(hint, (screen.get_width()//2 - hint.get_width()//2, screen.get_height()-50))

                # Pasar a fase 2 después de 5 segundos
                if pygame.time.get_ticks() - inicio > 5000:
                    fase = 2

            elif fase == 2:
                # Mensaje especial
                mensaje = [
                    "Bien hecho, lo has logrado.",
                    "Descubriste el misterio secreto dejado por los desarrolladores.",
                    "Te has ganado el premio por la curiosidad.",
                    "Este proyecto nos enorgullece enormemente y que tú estés aquí",
                    "jugándolo y disfrutándolo nos da una gran felicidad.",
                    "Muchas gracias y de parte del grupo Los Tripulantes nos despedimos.",
                    "",
                    "Press F to pay respect"
                ]

                y = 80
                for linea in mensaje:
                    txt = font_mediana.render(linea, True, BLANCO)
                    screen.blit(txt, (screen.get_width()//2 - txt.get_width()//2, y))
                    y += 36

                # Mostrar contador de F en pantalla
                contador_txt = font_pequena.render(f"Respectos: {f_counter}/10", True, (200,200,200))
                screen.blit(contador_txt, (screen.get_width()//2 - contador_txt.get_width()//2, y + 10))

                # Si se presionó F 10 veces, mostrar imagen especial
                if mostrar_premio and premio_image:
                    rect = premio_image.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 40))
                    screen.blit(premio_image, rect)

                    # Si usamos timer para que el premio desaparezca tras X ms:
                    if timer_premio_inicio is None:
                        timer_premio_inicio = pygame.time.get_ticks()
                    else:
                        if pygame.time.get_ticks() - timer_premio_inicio > DURACION_PREMIO_MS:
                            # Ocultar premio después de la duración (si prefieres que quede fija, comenta estas líneas)
                            mostrar_premio = False
                            timer_premio_inicio = None

            pygame.display.flip()

            # Eventos
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    poner_musica(tetris_theme)
                    return "quit"
                if ev.type == pygame.KEYDOWN:
                    # En cualquier fase ESC vuelve al juego
                    if ev.key == pygame.K_ESCAPE:
                        poner_musica(tetris_theme)
                        return "resume"

                    if fase == 1:
                        # permitir saltar la intro con ESC (ya manejado) o con F si quieres
                        continue

                    if fase == 2:
                        if ev.key == pygame.K_f:
                            f_counter += 1
                            print(f"Respect paid ({f_counter}/10)")
                            # efecto visual breve: si quieres reproducir un sonido, puedes hacerlo aquí
                            if f_counter >= 10:
                                mostrar_premio = True
                                timer_premio_inicio = None  # reiniciar timer para mostrar premio
                                print("🎉 Imagen especial desbloqueada")
                            else:
                                print("No se pudo cargar premio.png")
                        # permitir otras teclas en fase 2 (por ejemplo volver con ESC ya manejado)

    # --------------------
    # Fuente
    # --------------------
    font = pygame.font.Font(None, 36)

    # --------------------
    # Funciones de juego
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
                # Registrar tecla para Konami
                input_seq.append(event.key)
                # mantener input_seq con tamaño máximo razonable
                if len(input_seq) > len(KONAMI_CODE):
                    input_seq.pop(0)
                if input_seq[-len(KONAMI_CODE):] == KONAMI_CODE:
                    # Ejecutar Easter Egg
                    res = ejecutar_easter_egg()
                    if res == "quit":
                        return "quit"
                    # al volver, la música ya fue restaurada por ejecutar_easter_egg
                    input_seq.clear()  # limpiar secuencia tras usar el easter egg

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

                    # Puntaje por líneas
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

    return "gameover"