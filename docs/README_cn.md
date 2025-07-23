
<p align="center">
  <img
    src="../assets/logo.png"
    alt="FNAF: Signal Lost Logo"
    style="border: 2px solid white; border-radius: 5000px; width: 150px; height:150px; padding:10px;" />
</p>

<h1 align="center">FNAF: Signal Lost</h1>

---

<p align="center">
  欢迎来到 <strong>FNAF: Signal Lost</strong> — 一款刺激的完全可玩的控制台恐怖游戏，灵感来自《Five Nights at Freddy's》系列。  
  操控摄像头，管理电力，生存过夜… 全部在你的终端完成。
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
  <a href="./README_fr.md">Français</a> ·  
  <a href="./README_cn.md">简体中文</a> ·
  <a href="./README_es.md">Español</a> ·
  <a href="./README_ja.md">日本語</a> ·
  <a href="./README_pt-BR.md">Português Brasileiro</a> ·
  <a href="./README_it.md">Italiano</a>
</p>

<br>

## 🧠 主要特性

- 🔦 **能量系统**：受摄像头和手电筒使用限制。
- 🎥 **互动摄像头地图**（方向键导航）。
- 🤖 **玩偶AI**，难度可调节。
- ⏰ **夜间时钟**随时间推进。
- 🎶 使用 `pygame` 的**真实音效**。
- 💀 **自定义的 Game Over 屏幕**。
- 🌙 难度等级：普通、困难、噩梦。

---

```bash
# 克隆仓库
git clone https://github.com/zomboysoul/fnaf_cmd_game.git
cd fnaf_cmd_game

# 运行游戏（请确保安装 Python 3.10+）
python main.py
```

### 🕹️ 控制方式

- `↑ ↓ ← →`: 切换摄像头
- `Enter`: 查看选定房间
- `F`:  使用手电筒
- `Q`: 退出游戏

---

## 📁 项目结构

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
│   └── CAM_0X/ (摄像头 ASCII 模板)
├── sounds/
│   └── *.mp3 (音效)
├── animatronics.py
├── main.py
└── README.md
```

---

## ⚙️ 系统要求

- Python 3.10 或更高版本
- Pygame
- Colorama

使用以下命令安装：

```bash
pip install pygame colorama
```

---

## 📸 截图

![FNAF: Signal Lost Menu](../assets/menu.png)

![FNAF: Signal Lost Map](../assets/map.png)

![FNAF: Signal Lost Camara](../assets/camara.png)

---

## 🧑‍💻 作者

**Agustín Lezcano - ZomboySoul**
🔗 [GitHub](https://github.com/ZomboySoul) | 🇦🇷 阿根廷
