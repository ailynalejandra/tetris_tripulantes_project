# game/sounds.py
import pygame
from pathlib import Path
from game.settings import GameSettings

class SoundManager:
    def __init__(self, preload=True):
        self.base_dir = Path(GameSettings.SOUNDS_DIR)
        self.sounds = {}          # cache de efectos: name -> pygame.mixer.Sound | None
        self._music_volume = 0.4

        # Mapa por defecto: nombre lógico -> archivo en la carpeta de sonidos
        self.default_map = {
            "rotate": "rotate.flac",
            "move": "move.mp3",
            "soft_drop": "soft_drop.wav",
            "line_clear": "line_clear.mp3",
            "gameover": "gameover.wav",
            "final_theme": "gameover_theme.mp3",
            "screamer": "screamer.mp3",
            # añade aquí más efectos si los tienes
        }

        if preload:
            self.load_all_default_sounds()

    def _root_path(self, *paths):
        return self.base_dir.joinpath(*paths)

    # --------------------
    # Carga y caché
    # --------------------
    def load_sound(self, name, filename=None, volume=0.5):
        """
        Carga un efecto y lo guarda en caché.
        - name: clave lógica para referenciar el sonido.
        - filename: si no se pasa, se busca en default_map.
        """
        if name in self.sounds:
            return self.sounds[name]

        if filename is None:
            filename = self.default_map.get(name)
            if filename is None:
                print(f"❌ No hay archivo por defecto para el sonido '{name}'")
                self.sounds[name] = None
                return None

        sound_path = self._root_path(filename)
        if not sound_path.exists():
            print(f"❌ No existe sonido: {sound_path}")
            self.sounds[name] = None
            return None

        try:
            sound = pygame.mixer.Sound(str(sound_path))
            sound.set_volume(volume)
            self.sounds[name] = sound
            return sound
        except Exception as e:
            print(f"❌ Error cargando sonido {filename}: {e}")
            self.sounds[name] = None
            return None

    def load_all_default_sounds(self, volume=0.5):
        """Carga todos los sonidos definidos en default_map a la caché."""
        for name, filename in self.default_map.items():
            # Para música larga (mp3) no es necesario cargar como Sound; la dejamos para play_music
            if filename.lower().endswith((".mp3", ".ogg")) and name.endswith("_theme"):
                # opcional: no cargar como Sound, se reproducen con play_music
                self.sounds[name] = None
                continue
            self.load_sound(name, filename, volume=volume)

    # --------------------
    # Reproducción
    # --------------------
    def play_sound(self, name):
        """Reproduce un efecto ya cargado (o lo carga si no está)."""
        sound = self.sounds.get(name)
        if sound is None:
            # intentar cargar desde default_map si existe
            sound = self.load_sound(name)
        if sound:
            sound.play()

    def stop_all_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.set_endevent()

    def play_music(self, filename, loop=-1, volume=None):
        """Reproduce música (archivo en SOUNDS_DIR)."""
        if volume is None:
            volume = self._music_volume
        music_path = self._root_path(filename)
        if music_path.exists():
            try:
                self.stop_all_music()
                pygame.mixer.music.load(str(music_path))
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loop)
            except Exception as e:
                print(f"❌ Error cargando música {music_path}: {e}")
        else:
            print(f"❌ No existe música: {music_path}")

    # Métodos convenientes que usabas
    def play_menu_music(self, volume=0.4):
        self.play_music("menu_theme.mp3", loop=-1, volume=volume)

    def play_creditos_music(self, volume=0.5):
        self.play_music("creditos_theme.mp3", loop=-1, volume=volume)

    def play_gameover_theme(self, volume=0.1):
        self.play_music("gameover_theme.mp3", loop=0, volume=volume)

    # Helper específico que pediste
    def load_screamer_sound(self, volume=0.7):
        return self.load_sound("screamer", "screamer.mp3", volume=volume)
    

    