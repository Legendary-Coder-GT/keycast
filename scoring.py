from collections import Counter
from typing import Iterable

from typing_class import Keystroke


def gross_wpm(keystrokes: Iterable[Keystroke], elapsed_sec: float) -> float:
    """Gross WPM = (total chars / 5) per minute."""
    if elapsed_sec <= 0:
        return 0.0
    total_chars = sum(1 for _ in keystrokes)
    return (total_chars / 5) / (elapsed_sec / 60)


def accuracy(keystrokes: Iterable[Keystroke]) -> float:
    considered = [k for k in keystrokes if k.expected is not None]
    if not considered:
        return 100.0
    correct = sum(1 for k in considered if k.correct)
    return (correct / len(considered)) * 100


def per_key_errors(keystrokes: Iterable[Keystroke]) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for ks in keystrokes:
        if ks.expected is None:
            continue
        if not ks.correct:
            counter[ks.expected] += 1
    return dict(counter)
