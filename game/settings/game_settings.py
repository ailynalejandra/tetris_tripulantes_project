from typing import Tuple
from pathlib import Path
import os

class GameSettings:
    # Dimensiones del screen
    WIDTH: int = 330
    HEIGHT: int = 660

    # Colores
    BLACK: Tuple[int,int,int] = (0, 0, 0)
    WHITE: Tuple[int,int,int] = (255, 255, 255)
    BLUE: Tuple[int,int,int] = (0, 100, 255)
