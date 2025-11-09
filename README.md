# KeyCast — A Minimal Typing Trainer (Pygame)

A lightweight typing app that measures **WPM**, **accuracy**, and **error patterns** in real time. Runs locally, no internet required, stores your practice sessions as simple JSON files.

---

## Features

- **Two modes**:  
  - **Timed** (default 60 seconds)  
  - **Fixed Text** (type a selected passage to completion)
- **Live HUD**: WPM, accuracy, elapsed/remaining time, progress bar
- **Clear feedback**: correct characters (green), mistakes (red), visible caret
- **Results screen**: summary with top mistake keys
- **Session history**: each run saved to `data/sessions/` as JSON
- **Drill mode (optional)**: practice biased toward your most error-prone keys

---

## Getting Started

### Prerequisites
- **Python 3.10+**
- **Pygame** (installed below)
- Basic familiarity with running Python scripts

### Install (local development)
```bash
# 1) Clone
git clone https://github.com/<you>/keycast.git
cd keycast

# 2) (Recommended) Create & activate a virtual environment
python -m venv .venv
# macOS/Linux:
. .venv/bin/activate
# Windows (PowerShell):
# .\\.venv\\Scripts\\Activate.ps1

# 3) Install dependencies
python -m pip install --upgrade pip
python -m pip install pygame
```

> If you prefer a global, isolated install for CLI-like use, you can use `pipx install .` after you add packaging metadata. For simple use, running via `python` is sufficient.

### Run
```bash
# From the project root:
python run.py
```
If you prefer module form:
```bash
python -m src.keycast.app  # if you expose a __main__, otherwise use run.py
```

---

## Controls & Navigation

- **Menu**
  - **↑ / ↓** or **1 / 2 / 3**: Navigate/select mode  
  - **Enter**: Confirm selection  
  - **Esc**: Quit
- **Typing Scene**
  - **Type letters/numbers/punctuation**: Input characters
  - **Esc**: Return to Menu
  - (Optional) **Backspace**: Disabled by default in MVP (forces deliberate typing)
- **Results Screen**
  - **R**: Retry same text/mode
  - **Enter**: Return to Menu
  - **Esc**: Quit

> Backspace behavior is configurable (see **Settings**). In the default training mode, errors do **not** move the cursor; they are recorded and highlighted.

---

## Modes

### 1) Timed Mode
- Default duration: **60 seconds**
- Goal: maximize net output while maintaining accuracy
- Ends when the timer reaches 0; results screen appears automatically

### 2) Fixed-Text Mode
- Select one passage from `data/texts/` (plain `.txt` files)
- Goal: finish the passage with the best accuracy and time
- Ends when the last character is typed

### 3) Drill Mode (optional)
- Builds a practice string biased toward your **most frequent error keys** from recent sessions
- Useful for focused training (e.g., semicolons, numbers, frequent bigrams)

---

## Heads-Up Display (HUD)

- **WPM**: calculated as `(typed_chars / 5) / (elapsed_seconds / 60)` (gross WPM)
- **Accuracy**: `correct_keystrokes / total_keystrokes`
- **Timer**: counts up (fixed text) or down (timed mode)
- **Progress bar**: fraction of text completed in fixed-text mode

**Color coding**
- Correctly typed characters → **green**
- Mistyped characters at current position → **red**
- Caret → blinking block or bar

---

## Data & Privacy

- **Local only**: no network requests; nothing is uploaded
- **Session files**: written to `data/sessions/` as JSON
- **One file per run**; includes:
  ```json
  {
    "timestamp": "2025-11-09T11:35:00",
    "mode": "timed",
    "duration_sec": 60,
    "text_id": "sample_01",
    "gross_wpm": 58.4,
    "accuracy": 0.92,
    "total_keys": 275,
    "correct_keys": 253,
    "error_keys": {"s": 12, ";": 6, "e": 4}
  }
  ```
- You can delete any or all session files at any time. The app will continue to run normally.

---

## Settings

Create an **optional** settings file at `settings.ini` in the project root:

```ini
[app]
width = 900
height = 600
fps = 60

[training]
mode_default = timed      ; timed | fixed | drill
timed_duration = 60       ; seconds
backspace_enabled = false ; true to allow corrections

[colors]
fg_ok = 0,200,0
fg_err = 200,0,0
fg_text = 220,220,220
bg = 20,20,24
```

**Text sources**
- Place custom practice texts in `data/texts/` as `.txt`
- The app can list available files by name; select from the Menu

---

## Project Layout (for reference)

```
keycast/
├─ run.py                   # simple launcher (App().run())
├─ src/
│  └─ keycast/
│     ├─ __init__.py
│     ├─ app.py            # Pygame init, main loop, scene switching
│     ├─ scenes/
│     │  ├─ menu.py        # Mode select
│     │  ├─ typing.py      # Core typing scene
│     │  └─ results.py     # Summary screen
│     ├─ engine/
│     │  ├─ text_stream.py # supplies text & cursor
│     │  ├─ scoring.py     # WPM/accuracy/per-key errors
│     │  └─ persistence.py # save/load session JSON
│     └─ ui/
│        ├─ draw.py        # text layout, HUD, progress bar
│        └─ colors.py
├─ data/
│  ├─ texts/               # your .txt passages
│  └─ sessions/            # saved JSON runs (auto-created)
└─ README.md
```

---

## Safety & Comfort

- **Volume**: if you enable sounds later, keep volume low to protect hearing
- **Breaks**: take regular breaks to avoid repetitive strain; stretch hands/wrists
- **Posture**: keep a neutral wrist position; adjust chair/desk height
- **Lighting**: avoid eye strain; consider enabling your OS’s night mode

---

## Troubleshooting

**The window is blank or crashes on start**  
- Ensure Pygame is installed: `python -m pip show pygame`  
- Try a lower resolution in `settings.ini` (`width=800`, `height=500`)

**Keyboard input seems off / no characters appear**  
- Make sure the Pygame window is focused (click the window once)  
- Some international layouts may require additional handling; try US layout

**Backspace doesn’t work**  
- By design in the default training mode; set `backspace_enabled = true` in `settings.ini` to allow corrections

**Session files aren’t saving**  
- Confirm that `data/sessions/` exists and you have write permissions  
- Check the console for a path error; create the folder manually if needed

**High CPU usage**  
- The app caps FPS at `fps` in settings; try `fps=60` or lower

