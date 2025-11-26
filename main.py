import time
import pygame
import sys
from datetime import datetime
from constants import *
from text_stream import TextStream
from cursor import Cursor
from typing_class import TypingController
from scoring import gross_wpm, accuracy, per_key_errors
from draw import draw_hud
from results import draw_results
from menu import Menu, draw_menu
from persistence import save_session
from drill import generate_drill_text

drawable = pygame.sprite.Group()
updatable = pygame.sprite.Group()
Cursor.containers = (drawable, updatable) # type: ignore[attr-defined]
TextStream.containers = (drawable, ) # type: ignore[attr-defined]


def start_run(mode: str, text_path: str | None, drill_text: str | None = None):
    drawable.empty()
    updatable.empty()
    cursor = Cursor()
    textstream = TextStream(filepath=text_path, content=drill_text)
    typing_controller = TypingController(textstream, cursor)
    caret_x, caret_y, caret_height = textstream.caret_for_index(0)
    cursor.move_to(caret_x, caret_y, caret_height)
    start_time = time.time()
    return {
        "cursor": cursor,
        "textstream": textstream,
        "typing_controller": typing_controller,
        "start_time": start_time,
        "wpm": 0.0,
        "acc": 100.0,
        "last_metrics_update": start_time,
        "ended": False,
        "mode": mode,
        "text_path": text_path,
        "drill_text": drill_text,
    }


def finalize_run(run_state, elapsed_clamped: float):
    final_wpm = gross_wpm(run_state["typing_controller"].keystrokes, max(0.001, elapsed_clamped))
    final_acc = accuracy(run_state["typing_controller"].keystrokes)
    total_keys = len([k for k in run_state["typing_controller"].keystrokes if k.expected is not None])
    correct_keys = len(
        [k for k in run_state["typing_controller"].keystrokes if k.expected is not None and k.correct]
    )
    errors = per_key_errors(run_state["typing_controller"].keystrokes)
    results = {
        "wpm": final_wpm,
        "acc": final_acc,
        "elapsed_sec": elapsed_clamped,
        "mode": run_state["mode"],
        "total_keys": total_keys,
        "correct_keys": correct_keys,
        "errors": errors,
        "text_path": run_state.get("text_path"),
    }
    session_payload = {
        **results,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    save_session("data/sessions", session_payload)
    return results


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    duration = TIMED_DURATION_SEC
    menu = Menu()
    current_scene = "menu"  # menu, typing, results
    run_state = None
    results_data = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if current_scene == "typing" and run_state and not run_state["ended"]:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                run_state["typing_controller"].handle_event(event)
            elif current_scene == "results":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if run_state:
                            new_drill = None
                            if run_state["mode"] == "drill":
                                new_drill = generate_drill_text(length=500)
                            run_state = start_run(run_state["mode"], run_state.get("text_path"), new_drill)
                        results_data = None
                        current_scene = "typing"
                    elif event.key == pygame.K_RETURN:
                        current_scene = "menu"
                    elif event.key == pygame.K_ESCAPE:
                        return
            elif current_scene == "menu":
                selection = menu.handle_event(event)
                if selection:
                    drill_text = None
                    text_path = selection.get("text_path")
                    mode = selection["mode"]
                    if mode == "drill":
                        drill_text = generate_drill_text(length=500)
                        if not drill_text:
                            text_path = text_path or "data/texts/sample1.txt"
                    run_state = start_run(mode, text_path, drill_text)
                    results_data = None
                    current_scene = "typing"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

        now = time.time()
        elapsed = now - run_state["start_time"] if run_state else 0
        elapsed_clamped = elapsed

        if current_scene == "typing" and run_state:
            mode = run_state["mode"]
            if mode == "timed":
                if elapsed >= duration:
                    elapsed_clamped = duration
                    run_state["ended"] = True
                remaining = max(0.0, duration - elapsed_clamped)
                progress = min(1.0, elapsed_clamped / duration) if duration > 0 else 1.0
                timer_value = remaining
            else:
                if run_state["textstream"].ind >= len(run_state["textstream"].content):
                    run_state["ended"] = True
                progress = (
                    run_state["textstream"].ind / len(run_state["textstream"].content)
                    if run_state["textstream"].content
                    else 1.0
                )
                timer_value = elapsed_clamped

            updatable.update(dt)
            screen.fill("black")
            for thing in drawable:
                thing.draw(screen)

            if now - run_state["last_metrics_update"] >= 5:
                run_state["wpm"] = gross_wpm(
                    run_state["typing_controller"].keystrokes, max(0.001, elapsed_clamped)
                )
                run_state["acc"] = accuracy(run_state["typing_controller"].keystrokes)
                run_state["last_metrics_update"] = now
            draw_hud(screen, run_state["wpm"], run_state["acc"], timer_value, progress)

            if run_state["ended"]:
                results_data = finalize_run(run_state, elapsed_clamped)
                current_scene = "results"

        elif current_scene == "results":
            screen.fill("black")
            if results_data:
                draw_results(screen, results_data)
        elif current_scene == "menu":
            draw_menu(screen, menu)

        dt = clock.tick(FPS) / 1000  # Delta time in seconds.
        pygame.display.flip()


if __name__ == "__main__":
    main()
