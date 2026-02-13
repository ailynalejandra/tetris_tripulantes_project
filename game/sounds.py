# game/sounds.py
import pygame
from pathlib import Path
from game.settings import GameSettings

class SoundManager:
    def __init__(self, preload=True):
        self.base_dir = Path(GameSettings.SOUNDS_DIR)
        self.sounds = {}          # cache de efectos cortos: name -> pygame.mixer.Sound | None
        self._music_volume = 0.4

        # Mapa por defecto: nombre lógico -> archivo en la carpeta de sonidos
        self.default_map = {
            "rotate": "rotate.flac",
            "move": "move.flac",
            "soft_drop": "soft_drop.wav",
            "line_clear": "line_clear.flac",
            "gameover": "gameover.wav",          # efecto corto
            "final_theme": "gameover_theme.mp3", # música larga
            "screamer": "screamer.mp3",          # música larga (38s)
            # añade aquí más efectos si los tienes
        }

        if preload:
            self.load_all_default_sounds()

    def _root_path(self, *paths):
        return self.base_dir.joinpath(*paths)

    # --------------------
    # Carga y caché
    # --------------------
    def load_sound(self, name, filename=None, volume=0.8):
        """
        Carga un efecto corto y lo guarda en caché.
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
            # Para música larga (mp3/ogg) no se cargan como Sound; se reproducen con play_music
            if filename.lower().endswith((".mp3",".ogg")) and not name.endswith("over"):
                self.sounds[name] = None
                continue
            self.load_sound(name, filename, volume=volume)

    # --------------------
    # Reproducción
    # --------------------
    def play_sound(self, name):
        """Reproduce un efecto corto ya cargado (o lo carga si no está)."""
        sound = self.sounds.get(name)
        if sound is None:
            sound = self.load_sound(name)
        if sound:
            sound.play()

    def stop_all_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.set_endevent()

    def play_music(self, filename, loop=-1, volume=None):
        """Reproduce música larga (archivo en SOUNDS_DIR)."""
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

    # --------------------
    # Métodos específicos
    # --------------------
    def play_menu_music(self, volume=0.5):
        self.play_music("menu_theme.mp3", loop=-1, volume=volume)

    def play_creditos_music(self, volume=0.5):
        self.play_music("creditos_theme.mp3", loop=-1, volume=volume)

    def play_gameover_theme(self, volume=0.1):
        """Reproduce la música de Game Over (una sola vez)."""
        self.play_music("gameover_theme.mp3", loop=0, volume=volume)

    def play_screamer(self, volume=0.8):
        """Reproduce el screamer como música larga (38s)."""
        self.play_music("screamer.mp3", loop=0, volume=volume)
    

    