
<p align="center">
  <img
    src="../assets/logo.png"
    alt="FNAF: Signal Lost Logo"
    style="border: 2px solid white; border-radius: 5000px; width: 150px; height:150px; padding:10px;" />
</p>

<h1 align="center">FNAF: Signal Lost</h1>

---

<p align="center">
  Bienvenido a <strong>FNAF: Signal Lost</strong> — una emocionante experiencia de horror totalmente jugable en consola, inspirada en el universo de Five Nights at Freddy's.  
  Navega cámaras, administra la energía y sobrevive la noche… todo desde tu terminal.
</p>

<p align="center">
  <img alt="Platform" src="https://img.shields.io/badge/platform-python-00ffff?logo=python&logoColor=000000" />
  <img alt="Status" src="https://img.shields.io/badge/status-in%20development-ff00ff" />
  <img alt="Interface" src="https://img.shields.io/badge/interface-command%20line-ff007f?logo=windows-terminal&logoColor=white" />
  <img alt="Genre" src="https://img.shields.io/badge/genre-horror-ff1a1a" />
  <img alt="Style" src="https://img.shields.io/badge/style-text--based-6666ff" />
  <img alt="Language" src="https://img.shields.io/badge/lang-es-cc00ff" />
  <img alt="License" src="https://img.shields.io/github/license/ZomboySoul/fnaf_signal_lost" />
</p>


<br>

<p align="center">
  <a href="https://github.com/ZomboySoul/fnaf_signal_lost/issues/new?assignees=&labels=bug&projects=&template=bug_report.yml" target="_blank" rel="noopener noreferrer">Reportar Bug</a>
</p>
<p align="center">
  <a href="docs/README_fr.md">Français</a> ·  
  <a href="docs/README_cn.md">简体中文</a> ·
  <a href="docs/README_es.md">Español</a> ·
  <a href="docs/README_ja.md">日本語</a> ·
  <a href="docs/README_pt-BR.md">Português Brasileiro</a> ·
  <a href="docs/README_it.md">Italiano</a>
</p>

<br>

## 🧠 Características clave

- 🔦 **Sistema de energía**: limitado por el uso de cámaras y linterna.
- 🎥 **Mapa de cámaras interactivo** (navegación con teclas de flecha).
- 🤖 **IA de los animatrónicos** con dificultad ajustable.
- ⏰ **Reloj nocturno** que avanza con el tiempo.
- 🎶 **Efectos de sonido realistas** usando `pygame`.
- 💀 **Pantalla de Game Over personalizada**.
- 🌙 Niveles de dificultad: Normal, Difícil, Pesadilla.

---

## 🎮 Cómo jugar

```bash
# Clona el repositorio
git clone https://github.com/zomboysoul/fnaf_cmd_game.git
cd fnaf_cmd_game

# Ejecuta el juego (asegúrate de tener Python 3.10+)
python main.py
```

### 🕹️ Controles

- `↑ ↓ ← →`: Moverse entre cámaras
- `Enter`: Ver habitación seleccionada
- `F`:  Usar linterna
- `Q`: Salir del Juego

---

## 📁 Estructura del Proyecto

```bash
.
├── core/
│   ├── config.py
│   ├── energy.py
│   ├── game_engine.py
│   ├── movement.py
│   └── timers.py
├── ui/
│   └── screens.py
├── utils/
│   └── utils.py
├── rooms/
│   └── CAM_0X/ (plantillas ASCII de cámaras)
├── sounds/
│   └── *.mp3 (efectos de sonido)
├── animatronics.py
├── main.py
└── README.md
```

---

## ⚙️ Requirements

- Python 3.10 or later
- Pygame
- Colorama

Install them with:

```bash
pip install pygame colorama
```

---

## 📸 Capturas de pantalla

![FNAF: Signal Lost Menu](../assets/menu.png)

![FNAF: Signal Lost Map](../assets/map.png)

![FNAF: Signal Lost Camara](../assets/camara.png)

---

## 🧑‍💻 Autor

**Agustín Lezcano - ZomboySoul**
🔗 [GitHub](https://github.com/ZomboySoul) | 🇦🇷 Argentina
