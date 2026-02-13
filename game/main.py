import pygame
import sys
import os
from game import tetris, menu
from game.sounds import SoundManager
from game.settings import GameSettings
from game.images import ImageManager

# --------------------
# Inicialización
# --------------------
pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    print("Audio no disponible")

WIDTH, HEIGHT = 330, 660
screen = pygame.display.set_mode((GameSettings.WIDTH, GameSettings.HEIGHT))
pygame.display.set_caption("Menú Principal - Tetris")

font_title = pygame.font.Font(None, 48)
font_text  = pygame.font.Font(None, 22)
font_creditos = pygame.font.Font(None, 22)

#imagesmanager
image_manager = ImageManager()
# Soundmanager
sound_manager = SoundManager()

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
        screen.fill(GameSettings.BLACK)
        draw_text("INSTRUCCIONES", font_title, GameSettings.WHITE, screen, WIDTH//2, 80)
        draw_text("[LEFT]/[RIGHT] : mover pieza", font_text, GameSettings.WHITE, screen, WIDTH//2, 120)
        draw_text("[UP] : rotar pieza", font_text, GameSettings.WHITE, screen, WIDTH//2, 160)
        draw_text("[DOWN] : bajar pieza rápido", font_text, GameSettings.WHITE, screen, WIDTH//2, 200)
        draw_text("P : Pausa", font_text, GameSettings.WHITE, screen, WIDTH//2, 240)
        draw_text("ESC : Volver al menú", font_text, GameSettings.WHITE, screen, WIDTH//2, 280)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.flip()

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
                # detener cualquier música antes de reiniciar
                sound_manager.stop_all_music()
                continue

            if action == "menu_principal":
                sound_manager.stop_all_music()
                sound_manager.play_menu_music()
                return

            if action == "salir":
                sound_manager.stop_all_music()
                pygame.quit()
                sys.exit()

# --------------------
# Menú Principal
# --------------------
def main_menu():
    sound_manager.play_menu_music()

    while True:
        screen.fill(GameSettings.BLACK)
        draw_text("TETRIS", font_title, GameSettings.WHITE, screen, WIDTH//2, 80)

        start_button   = pygame.Rect(65, 150, 200, 60)
        instr_button   = pygame.Rect(65, 250, 200, 60)
        credits_button = pygame.Rect(65, 350, 200, 60)
        exit_button    = pygame.Rect(65, 450, 200, 60)

        pygame.draw.rect(screen, GameSettings.BLUE, start_button)
        pygame.draw.rect(screen, GameSettings.BLUE, instr_button)
        pygame.draw.rect(screen, GameSettings.BLUE, credits_button)
        pygame.draw.rect(screen, GameSettings.BLUE, exit_button)

        draw_text("Iniciar Juego", font_title, GameSettings.WHITE, screen, WIDTH//2, 180)
        draw_text("Instrucciones", font_title, GameSettings.WHITE, screen, WIDTH//2, 280)
        draw_text("Créditos", font_title, GameSettings.WHITE, screen, WIDTH//2, 380)
        draw_text("Salir", font_title, GameSettings.WHITE, screen, WIDTH//2, 480)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    sound_manager.stop_all_music()
                    start_game_loop()

                elif instr_button.collidepoint(event.pos):
                    show_instructions()

                elif credits_button.collidepoint(event.pos):
                    show_credits()

                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

# --------------------
# Créditos
# --------------------
def show_credits():
    # Reproducir música de créditos
    sound_manager.play_creditos_music()

    # Lista de créditos
    creditos = [
        "CREDITOS",
        "Desarrollador:", 
        "LUIS.P",
        "Programación:", 
        "JESUS.P",
        "Asistentes de programacion:",
        "Copilot y LUIS.P",
        "Editor de textos y diseño:",
        "AILYN.Q",
        "asistente de edicion",
        "RAFAEL.C",
        "Efectos Visuales",
        "JESUS.P",
        "asistentes de efectos visuales",
        "LUIS,RAFAEL y AILYN",
        "Tecnico de audio:",
        "JESUS.P",
        "Inspector de bugs:",
        "RAFAEL.C",
        "Agradecimientos especiales a :",
        "Halomante don FERNANDO BAUTE",
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

    # Cargar imágenes con ImageManager
    imagen_final = image_manager.load_credit_image()      # final.png
    imagen_final = pygame.transform.scale(imagen_final, (300, 200))
    imagen_estatica = image_manager.load_static_image()   # final_static.png
    imagen_estatica = pygame.transform.scale(imagen_estatica, (300, 200))

    while running:
        screen.fill(GameSettings.BLACK)

        if not mostrar_final:
            # Dibujar cada línea de créditos subiendo
            for i, linea in enumerate(creditos):
                texto = font_creditos.render(linea, True, GameSettings.WHITE)
                screen.blit(texto, (WIDTH//2 - texto.get_width()//2, desplazamiento + i*50))

            # Dibujar la imagen final.png como si fuera la última "línea"
            if imagen_final:
                screen.blit(imagen_final, (
                    WIDTH//2 - imagen_final.get_width()//2,
                    desplazamiento + len(creditos)*50
                ))

            desplazamiento -= 0.5  # velocidad del scroll

            # Cuando todo salió por arriba (texto + imagen)
            limite_scroll = -(len(creditos)*50 + (imagen_final.get_height() if imagen_final else 0))
            if desplazamiento < limite_scroll:
                mostrar_final = True

        else:
            # Pantalla final estática
            lineas = ["Gracias por jugar",
                      "se despiden",
                      "los tripulantes",
                      "GAME",
                      "te falta odio "]
            for i, linea in enumerate(lineas):
                texto = font_final.render(linea, True, GameSettings.WHITE)
                rect_texto = texto.get_rect(center=(WIDTH//2, HEIGHT//2 - 150 + i*50))
                screen.blit(texto, rect_texto)

            # Imagen final_static.png debajo del bloque de texto
            if imagen_estatica:
                rect_img = imagen_estatica.get_rect(center=(WIDTH//2, HEIGHT//2 + 200))
                screen.blit(imagen_estatica, rect_img)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sound_manager.stop_all_music()
                sound_manager.play_menu_music()
                running = False

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main_menu()