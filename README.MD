📖 Lore del juego

En un mundo digital donde las piezas del Tetris no son simples bloques, sino fragmentos de un antiguo poder cósmico, existe un equilibrio que mantiene la realidad estable. Cada línea completada fortalece el Muro del Orden, la barrera que protege a la humanidad de fuerzas oscuras.  

Pero ese equilibrio está amenazado…  

👑 El Halomante
El Halomante es un hechicero olvidado, maestro de los halos de energía que rodean el universo. En su ambición, intentó controlar el flujo de las piezas cósmicas, pero fue desterrado al Vacío del Caos. Ahora ha regresado, corrompiendo los tetrominos y enviándolos en formas cada vez más veloces y caóticas para romper el Muro del Orden.  

Su objetivo: colapsar la realidad en un torbellino eterno de piezas descontroladas.  

🧩 El jugador
Tú eres el Arquitecto del Orden, el último guardián capaz de manipular los fragmentos cósmicos. Cada línea que completas es un golpe contra el Halomante, debilitando su poder. Pero cuidado: si las piezas alcanzan la cima del tablero, el Halomante habrá ganado y el mundo caerá bajo su dominio.
🎮 Tetris

Un juego clásico de Tetris desarrollado en Python con Pygame.  
Este proyecto busca ser modular, claro y fácil de mantener, con separación de recursos, lógica y configuración.

---

📂 Estructura del proyecto

`
tetris-main/
├── assets/                  # Recursos del juego
│   ├── images/              # Imágenes, sprites, fondos
│   └── sounds/              # Música y efectos de sonido
├── game/                    # Código fuente del juego
│   ├── settings/            # Configuración del juego
│   │   └── game_settings.py # Constantes y parámetros
│   ├── images.py            # Manejo de recursos gráficos
│   ├── sounds.py            # Manejo de sonidos
│   ├── menu.py              # Lógica del menú
│   ├── tetris.py            # Lógica principal del Tetris
│   └── main.py              # Loop principal
├── run.py                   # Punto de entrada para ejecutar el juego
├── versión.py               # Archivo con la versión del proyecto
├── bumpver                  # Configuración de versionado automático
├── .gitignore               # Exclusiones para Git
└── venv/                    # Entorno virtual de Python
`

---

🚀 Instalación y ejecución

1. Clona el repositorio:
   `bash
   git clone https://github.com/tuusuario/tetris-main.git
   cd tetris-main
   `

2. Crea y activa un entorno virtual (opcional pero recomendado):
   `bash
   python -m venv venv
   source venv/bin/activate   # En Linux/Mac
   venv\Scripts\activate      # En Windows
   `

3. Instala las dependencias:
   `bash
   pip install -r requirements.txt
   `

4. Ejecuta el juego:
   `bash
   python run.py
   `

---

🎯 Objetivo del juego

- Coloca las piezas (tetrominos) que caen en el tablero.  
- Completa líneas horizontales para ganar puntos.  
- Evita que las piezas lleguen hasta la parte superior.  

---

🕹️ Controles

- ⬅️ Flecha izquierda: mover pieza a la izquierda  
- ➡️ Flecha derecha: mover pieza a la derecha  
- ⬇️ Flecha abajo: acelerar caída  
- ⬆️ Flecha arriba: rotar pieza  
- p letra "p"   : pausar el juego
- Esc: salir del juego  

---

📦 Dependencias

- Python 3.10+  
- Pygame  
- bumpver  

---

📝 Licencia

Este proyecto está bajo la licencia MIT.  
¡Siéntete libre de usarlo, modificarlo y compartirlo!  

---

✨ Créditos

Desarrollado por "LOS TRIPULANTES GAME" un grupo de desarrolladores que bajo la tutela del halomante logramos realizar este gran juego,muy divertido y con toques humoristicos no te lo pierdas y disfruta gran aventurero..........ahhhh si, puede haber uno que otro secreto escondidos por ahi, si eres curioso intenta conseguir todos los secretos:3 mucha suerte se despiden "LOS TRIPULANTES GAME"    
`

