# KeyCast — Typing Trainer (Pygame)

KeyCast is a local-first typing trainer with a simple HUD, session logging, and practice modes that adapt to your mistakes.

---

## Features
- **Modes**: Timed (countdown), Fixed Text (finish the passage), Drill (bias toward your weakest keys from recent sessions).
- **HUD**: WPM, accuracy, timer, and progress bar; metrics refresh every 5s for readability.
- **Feedback**: green for correct, red for mistakes, blinking caret.
- **Results screen**: shows WPM, accuracy, totals, and top error keys; navigation with R/Enter/Esc.
- **Session history**: every run saved as JSON in `data/sessions/`.
- **Drill generation**: uses recent session errors; if `OPENAI_API_KEY` is in `.env`, generates richer drills via AI, otherwise uses a local fallback.
- **Configurable**: `settings.ini` controls window size, FPS, durations, colors, caret blink, and backspace policy.

---

## Setup
Prereqs: Python 3.10+, Pygame.

```bash
git clone https://github.com/<you>/keycast.git
cd keycast
python3 -m venv .venv && . .venv/bin/activate  # or equivalent
python3 -m pip install --upgrade pip
python3 -m pip install pygame
```

Run:
```bash
python3 main.py
```

Optional AI drills: create `.env` with `OPENAI_API_KEY=...`

---

## Controls & Flow
- **Menu**: `↑/↓` or `1/2/3` to choose Timed / Fixed Text / Drill; `Enter` to start; `Esc` quits.
- **Typing**: type to advance; errors mark red and advance the expected index; caret blinks. Backspace obeys `settings.ini`.
- **Results**: `R` retry same mode/text (drill regenerates), `Enter` back to menu, `Esc` quits.

Scene flow: Menu → Typing → Results → Menu. Esc always quits immediately.

---

## Modes
- **Timed**: countdown (default 60s).
- **Fixed Text**: pick a `.txt` from `data/texts/`; ends at last char.
- **Drill**: builds practice text from your top error keys; uses AI when available, local fallback otherwise.

---

## Settings (`settings.ini`)
Example (defaults shown):
```ini
[display]
width = 1280
height = 720
fps = 60
hud_height = 70

[timed]
duration_sec = 60

[input]
allow_backspace = true

[cursor]
blink_rate = 0.5

[colors]
white = 255,255,255
black = 0,0,0
green = 0,200,70
red = 200,30,30
```

---

## Data
- Sessions saved to `data/sessions/` as JSON (one per run; includes mode, text path, WPM, accuracy, per-key errors, timestamp).
- Practice texts live in `data/texts/` (`.txt`).

---

## Project Map
```
main.py              # scenes + loop + HUD
text_stream.py       # text layout/rendering
cursor.py            # blinking caret
typing_class.py      # keystroke handling
menu.py              # mode selection + file picker
results.py           # results overlay
draw.py              # HUD
scoring.py           # WPM/accuracy/error stats
drill.py             # drill text generation (AI or fallback)
persistence.py       # save/load sessions
settings.ini         # optional overrides
data/texts/          # source texts
data/sessions/       # saved runs
```

---

## Notes
- No network required unless you opt into AI drills.
- Esc at any point quits cleanly.
- `.env` is ignored by git for API keys or other secrets.
