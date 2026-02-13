# game/images.py
import pygame
from pathlib import Path
from game.settings import GameSettings

class ImageManager:
    def __init__(self, preload=True):
        self.base_dir = Path(GameSettings.IMAGES_DIR)
        self.images = {}  # cache: name -> pygame.Surface | None
        self.default_map = {
            "secret": "secret.png",
            "premio": "premio.png",
            "credit_final": "final.png",
            "credit_static": "final_static.png",
            "screamer": "screamer.png",
            # añade más pares name:filename si los necesitas
        }
        if preload:
            self.load_all_default_images()

    def _root_path(self, *paths):
        return self.base_dir.joinpath(*paths)

    # --------------------
    # Carga y caché
    # --------------------
    def load_image(self, name, filename=None, size=None, convert_alpha=True):
        """
        Carga una imagen y la guarda en caché.
        - name: clave lógica para referenciar la imagen.
        - filename: nombre de archivo dentro de IMAGES_DIR; si None usa default_map.
        - size: tupla (w,h) para escalar opcionalmente.
        - convert_alpha: True para conservar transparencia cuando sea posible.
        Devuelve pygame.Surface o None.
        """
        if name in self.images:
            return self.images[name]

        if filename is None:
            filename = self.default_map.get(name)
            if filename is None:
                print(f"❌ No hay archivo por defecto para la imagen '{name}'")
                self.images[name] = None
                return None

        path = self._root_path(filename)
        if not path.exists():
            print(f"❌ No existe imagen: {path}")
            self.images[name] = None
            return None

        try:
            surf = pygame.image.load(str(path))
            if convert_alpha:
                try:
                    surf = surf.convert_alpha()
                except Exception:
                    surf = surf.convert()
            else:
                surf = surf.convert()
            if size:
                surf = pygame.transform.scale(surf, size)
            self.images[name] = surf
            return surf
        except Exception as e:
            print(f"❌ Error cargando imagen {filename}: {e}")
            self.images[name] = None
            return None

    def load_all_default_images(self, size_map=None):
        """
        Precarga todas las imágenes definidas en default_map.
        - size_map: dict opcional con tamaños por nombre, por ejemplo {'credit_final': (300,200)}
        """
        if size_map is None:
            size_map = {}
        for name, filename in self.default_map.items():
            size = size_map.get(name)
            self.load_image(name, filename, size=size)

    def get(self, name):
        """Devuelve una imagen ya cargada o None."""
        return self.images.get(name)

    # --------------------
    # Métodos específicos para tu juego
    # --------------------
    def load_credit_image(self, size=(300, 200)):
        return self.load_image("credit_final", None, size=size)

    def load_static_image(self, size=(300, 200)):
        return self.load_image("credit_static", None, size=size)

    def load_screamer_image(self, size=None):
        return self.load_image("screamer", None, size=size)

    # --------------------
    # Helpers de dibujo
    # --------------------
    def draw_image(self, surface, name, pos, center=False):
        """
        Dibuja una imagen ya cargada en la superficie dada.
        - surface: pantalla o surface destino.
        - name: clave lógica de la imagen.
        - pos: tupla (x,y) o rect para posicionar.
        - center: si True centra la imagen en pos.
        """
        img = self.get(name)
        if not img:
            return
        if center:
            rect = img.get_rect(center=pos)
            surface.blit(img, rect)
        else:
            surface.blit(img, pos)