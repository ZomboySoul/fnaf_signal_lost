
<p align="center">
  <img
    src="assets/logo.png"
    alt="FNAF: Signal Lost Logo"
    style="border: 2px solid white; border-radius: 5000px; width: 150px; height:150px; padding:10px;" />
</p>

<h1 align="center">FNAF: Signal Lost</h1>

---

<p align="center">
  Welcome to <strong>FNAF: Signal Lost</strong> — a thrilling, fully-playable console horror experience inspired by the Five Nights at Freddy's universe.  
  Navigate cameras, manage power, and survive the night… all from your terminal.
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
  <a href="https://github.com/ZomboySoul/fnaf_signal_lost/issues/new?assignees=&labels=bug&projects=&template=bug_report.yml" target="_blank" rel="noopener noreferrer">Report Bug</a>
</p>
<p align="center">
  <a href="documents/README_fr.md">Français</a> ·  
  <a href="documents/README_cn.md">简体中文</a> ·
  <a href="documents/README_es.md">Español</a> ·
  <a href="documents/README_ja.md">日本語</a> ·
  <a href="documents/README_pt-BR.md">Português Brasileiro</a> ·
  <a href="documents/README_it.md">Italiano</a>
</p>

<br>

## 🧠 Key Features

- 🔦 **Energy system**: limited by camera and flashlight usage.
- 🎥 **Interactive camera map** (arrow key navigation).
- 🤖 **Animatronic AI** with adjustable difficulty.
- ⏰ **Night clock** that advances over time.
- 🎶 **Realistic sound effects** using `pygame`.
- 💀 **Custom Game Over screen**.
- 🌙 Difficulty levels: Normal, Hard, Nightmare.

---

## 🎮 How to Play

```bash
# Clone the repository
git clone https://github.com/zomboysoul/fnaf_cmd_game.git
cd fnaf_cmd_game

# Run the game (make sure you have Python 3.10+)
python main.py
```

### 🕹️ Controls

- `↑ ↓ ← →`: Move between cameras
- `Enter`: View selected room
- `F`: Use flashlight
- `Q`: Quit the game

---

## 📁 Project Structure

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
│   └── CAM_0X/ (camera ASCII art templates)
├── sounds/
│   └── *.mp3 (sound effects)
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

## 📸 Screenshots

![FNAF: Signal Lost Menu](assets/menu.png)

![FNAF: Signal Lost Map](assets/map.png)

![FNAF: Signal Lost Camara](assets/camara.png)

---

## 🧑‍💻 Author

📄[View project documentation](https://zomboysoul.github.io/fnaf_signal_lost/)

**Agustín Lezcano - ZomboySoul**
🔗 [GitHub](https://github.com/ZomboySoul) | 🇦🇷 Argentina
