import pygame
import sys
import os
from game import menu
from game import tetris

# --------------------
# Inicialización
# --------------------
pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    print("Audio no disponible")

WIDTH, HEIGHT = 330, 660
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menú Principal - Tetris")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE  = (0, 100, 255)
font_title = pygame.font.Font(None, 48)
font_text  = pygame.font.Font(None, 22)
font_creditos =pygame.font.Font(None, 22)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# --------------------
# Pantalla de Instrucciones
# --------------------
def show_instructions():
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("INSTRUCCIONES", font_title, WHITE, screen, WIDTH//2, 80)
        draw_text("[LEFT]/[RIGHT] : mover pieza", font_text, WHITE, screen, WIDTH//2, 120)
        draw_text("[UP] : rotar pieza", font_text, WHITE, screen, WIDTH//2, 160)
        draw_text("[DOWN] : bajar pieza rápido", font_text, WHITE, screen, WIDTH//2, 200)
        draw_text("P : Pausa", font_text, WHITE, screen, WIDTH//2, 240)
        draw_text("ESC : Volver al menú", font_text, WHITE, screen, WIDTH//2, 280)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.flip()


# --------------------
# Música del menú
# --------------------
def get_root_path(*paths):
    base = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base, *paths)

def play_menu_music():
    menu_music = get_root_path("sounds", "menu_theme.mp3")
    if os.path.exists(menu_music):
        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.unload()
        except:
            pass
        pygame.mixer.music.load(menu_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)

# --------------------
# Loop del juego
# --------------------
def start_game_loop():
    while True:
        result = tetris.run_game(screen)

        if result == "quit":
            pygame.quit()
            sys.exit()

        if result == "gameover":
            action = menu.game_over_menu(screen)

            if action == "reiniciar":
                menu.stop_all_music()
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                try:
                    pygame.mixer.music.unload()
                except:
                    pass
                continue

            if action == "menu_principal":
                menu.stop_all_music()
                play_menu_music()
                return

            if action == "salir":
                menu.stop_all_music()
                pygame.quit()
                sys.exit()

# --------------------
# Menú Principal
# --------------------
def main_menu():
    play_menu_music()

    while True:
        screen.fill(BLACK)
        draw_text("TETRIS", font_title, WHITE, screen, WIDTH//2, 80)

        start_button   = pygame.Rect(65, 150, 200, 60)
        instr_button   = pygame.Rect(65, 250, 200, 60)
        credits_button = pygame.Rect(65, 350, 200, 60)
        exit_button    = pygame.Rect(65, 450, 200, 60)

        pygame.draw.rect(screen, BLUE, start_button)
        pygame.draw.rect(screen, BLUE, instr_button)
        pygame.draw.rect(screen, BLUE, credits_button)
        pygame.draw.rect(screen, BLUE, exit_button)

        draw_text("Iniciar Juego", font_title, WHITE, screen, WIDTH//2, 180)
        draw_text("Instrucciones", font_title, WHITE, screen, WIDTH//2, 280)
        draw_text("Créditos", font_title, WHITE, screen, WIDTH//2, 380)
        draw_text("Salir", font_title, WHITE, screen, WIDTH//2, 480)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    try:
                        pygame.mixer.music.unload()
                    except:
                        pass
                    start_game_loop()

                elif instr_button.collidepoint(event.pos):
                    show_instructions()

                elif credits_button.collidepoint(event.pos):
                    show_credits()

                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()

def show_credits():
    # Apagar música del menú y reproducir la de créditos
    pygame.mixer.music.stop()
    try:
        pygame.mixer.music.unload()
    except:
        pass

    creditos_music = get_root_path("sounds", "creditos_theme.mp3")
    if os.path.exists(creditos_music):
        pygame.mixer.music.load(creditos_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    # Lista de créditos
    creditos = [
        "CREDITOS",
        "Desarrollador:", 
        "LUIS.P",
        "Programación:", 
        "JESUS.P",
        "Asistentes de programacion:",
        "Copilot y LUIS.P",
        "Editor de textos y diseno:",
        "AILYN.Q",
        "Tecnico de audio:",
        "JESUS.P",
        "Inspector de bugs:",
        "RAFAEL.C(GUAIDO)",
        "tecnico en relajacion:",
        "RAFAEL.C(GUAIDO)",
        "Agradecimientos especiales a :",
        "Holomante don FERNANDO BAUTE",
        "que nos instruyo en este",
        "fantastico mundo de la",
        "programacion motivandonos a",
        "mejorar y crecer como futuros",
        "ingenieros desarrollando nuestro",
        "aprendizaje e impulsandonos a",
        "ser cada dia mejores y nos regalo",
        "tardes inolvidables de impostores",
        "y tripulantes con excelentes",
        "referencias solo para basados",
        "en la verdadera cultura",
        "Gracias por jugar!",
        "ERES FUERTE, PERO!",
        "CRISTO LO ES MAS!!!"
    ]

    reloj = pygame.time.Clock()
    desplazamiento = HEIGHT
    running = True
    mostrar_final = False

    # Fuentes
    font_creditos = pygame.font.Font(None, 28)
    font_final    = pygame.font.Font(None, 38)

    # Imagen que sube junto con los créditos
    imagen_final_path = get_root_path("images", "final.png")
    if os.path.exists(imagen_final_path):
        imagen_final = pygame.image.load(imagen_final_path)
        imagen_final = pygame.transform.scale(imagen_final, (300, 200))
    else:
        imagen_final = None

    # Imagen para la pantalla final estática
    imagen_estatica_path = get_root_path("images", "final_static.png")
    if os.path.exists(imagen_estatica_path):
        imagen_estatica = pygame.image.load(imagen_estatica_path)
        imagen_estatica = pygame.transform.scale(imagen_estatica, (300, 200))
    else:
        imagen_estatica = None

    while running:
        screen.fill(BLACK)

        if not mostrar_final:
            # Dibujar cada línea de créditos subiendo
            for i, linea in enumerate(creditos):
                texto = font_creditos.render(linea, True, WHITE)
                screen.blit(texto, (WIDTH//2 - texto.get_width()//2, desplazamiento + i*50))

            # Dibujar la imagen como si fuera la última "línea"
            if imagen_final:
                screen.blit(imagen_final, (WIDTH//2 - imagen_final.get_width()//2,
                                           desplazamiento + len(creditos)*50))

            desplazamiento -= 0.5 #ajustar velocidad de los creditos 

            # Cuando todo salió por arriba (texto + imagen)
            if desplazamiento < -(len(creditos)*50 + (imagen_final.get_height() if imagen_final else 0)):
                mostrar_final = True

        else:
            # Pantalla final estática
            lineas = ["Gracias por jugar",
                      "se despiden",
                      "los tripulantes",
                      "GAME",
                      "te falta odio "]
            for i, linea in enumerate(lineas):
                texto = font_final.render(linea, True, WHITE)
                rect_texto = texto.get_rect(center=(WIDTH//2, HEIGHT//2 - 150 + i*50))
                screen.blit(texto, rect_texto)

            # Imagen debajo del bloque de texto
            if imagen_estatica:
                rect_img = imagen_estatica.get_rect(center=(WIDTH//2, HEIGHT//2 + 200))
                screen.blit(imagen_estatica, rect_img)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                try:
                    pygame.mixer.music.unload()
                except:
                    pass
                play_menu_music()
                running = False

        pygame.display.flip()
        reloj.tick(60)