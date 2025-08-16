
<p align="center">
  <img
    src="../assets/logo.png"
    alt="FNAF: Signal Lost Logo"
    style="border: 2px solid white; border-radius: 5000px; width: 150px; height:150px; padding:10px;" />
</p>

<h1 align="center">FNAF: Signal Lost</h1>

---

<p align="center">
  Bem-vindo ao <strong>FNAF: Signal Lost</strong> — uma experiência de horror emocionante, totalmente jogável no console, inspirada no universo Five Nights at Freddy's.  
  Navegue pelas câmeras, gerencie a energia e sobreviva à noite… tudo pelo seu terminal.
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
  <a href="https://github.com/ZomboySoul/fnaf_signal_lost/issues/new?assignees=&labels=bug&projects=&template=bug_report.yml" target="_blank" rel="noopener noreferrer">
  Reportar um bug
  </a>
</p>

<p align="center">
  <a href="./README_fr.md">Français</a> ·  
  <a href="./README_cn.md">简体中文</a> ·
  <a href="./README_es.md">Español</a> ·
  <a href="./README_ja.md">日本語</a> ·
  <a href="./README_pt-BR.md">Português Brasileiro</a> ·
  <a href="./README_it.md">Italiano</a>
</p>

<br>

## 🧠 Principais Recursos

- 🔦 **Sistema de energia**: limitado pelo uso da câmera e lanterna.
- 🎥 **Mapa de câmeras interativo** (navegação com setas).
- 🤖 **IA dos animatrônicos** com dificuldade ajustável.
- ⏰ **Relógio noturno** que avança com o tempo.
- 🎶 **Efeitos sonoros realistas** usando `pygame`.
- 💀 **Tela de Game Over personalizada**.
- 🌙 Níveis de dificuldade: Normal, Difícil, Pesadelo.

---

## 🎮 Como jogar

```bash
# Clonar o repositório
git clone https://github.com/zomboysoul/fnaf_cmd_game.git
cd fnaf_cmd_game

# Execute o jogo (certifique-se de ter o Python 3.10+)
python main.py
```

### 🕹️ Controles

- `↑ ↓ ← →`: Navegar entre câmeras
- `Enter`: Ver sala selecionada
- `F`: Usar lanterna
- `Q`: Salir del juego

---

## 📁 Estrutura do Projeto

```bash
├── core/
.
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
│   └── CAM_0X/ (modelos ASCII das câmeras)
├── sounds/
│   └── *.mp3 (efeitos sonoros)
├── animatronics.py
├── main.py
└── README.md
```

---

## ⚙️ Requisitos

- Python 3.10 ou superior
- Pygame
- Colorama

Instale com:

```bash
pip install pygame colorama
```

---

## 📸 captura de tela

![FNAF: Signal Lost Menu](../assets/menu.png)

![FNAF: Signal Lost Map](../assets/map.png)

![FNAF: Signal Lost Camara](../assets/camara.png)

---

## 🧑‍💻 autor

📄[Ver a documentação do projeto](https://zomboysoul.github.io/fnaf_signal_lost/)
**Agustín Lezcano - ZomboySoul**
🔗 [GitHub](https://github.com/ZomboySoul) | 🇦🇷 Argentina
