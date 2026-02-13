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
        }
        if preload:
            try:
                self.load_all_default_images()
            except Exception as e:
                print(f"❌ Error en preload de imágenes: {e}")

    def _root_path(self, *paths):
        return self.base_dir.joinpath(*paths)

    # --------------------
    # Utilidades internas
    # --------------------
    def _find_file_case_insensitive(self, filename):
        """
        Busca un archivo en self.base_dir de forma insensible a mayúsculas.
        Devuelve Path si lo encuentra, o None.
        """
        try:
            target_lower = filename.lower()
            if not self.base_dir.exists():
                return None
            for p in self.base_dir.iterdir():
                if p.is_file() and p.name.lower() == target_lower:
                    return p
        except Exception:
            return None
        return None

    def _try_alternative_extensions(self, stem):
        """
        Prueba extensiones comunes si no existe el archivo con la extensión original.
        Devuelve Path si encuentra alguno, o None.
        """
        exts = [".png", ".jpg", ".jpeg", ".webp", ".bmp"]
        for ext in exts:
            candidate = self.base_dir.joinpath(stem + ext)
            if candidate.exists():
                return candidate
            # case-insensitive search
            found = self._find_file_case_insensitive(stem + ext)
            if found:
                return found
        return None

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

        # Ruta esperada
        path = self._root_path(filename)
        print(f"🔎 Intentando cargar imagen: {path}")

        # Si no existe, intentar búsqueda insensible a mayúsculas
        if not path.exists():
            alt = self._find_file_case_insensitive(filename)
            if alt:
                print(f"ℹ️  Encontrado (case-insensitive): {alt}")
                path = alt
            else:
                # intentar con extensiones alternativas usando el stem
                stem = Path(filename).stem
                alt2 = self._try_alternative_extensions(stem)
                if alt2:
                    print(f"ℹ️  Encontrado con extensión alternativa: {alt2}")
                    path = alt2

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
            try:
                self.load_image(name, filename, size=size)
            except Exception as e:
                print(f"❌ Error precargando {name}: {e}")
                self.images[name] = None

    def get(self, name):
        """Devuelve una imagen ya cargada o None."""
        return self.images.get(name)

    # --------------------
    # Métodos específicos para tu juego
    # --------------------
    def load_credit_image(self, size=(200, 200)):
        return self.load_image("credit_final", None, size=size)

    def load_static_image(self, size=(150, 150)):
        return self.load_image("credit_static", None, size=size)

    def load_screamer_image(self, size=(300, 200)):
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