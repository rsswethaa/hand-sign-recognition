import json
from pathlib import Path

from .features import normalise_landmarks


def append_sample(path, label, landmarks, handedness='Right'):
    label = (label or '').strip().upper().replace(' ', '_')
    if not label:
        raise ValueError('label is required')
    if len(landmarks) != 21:
        raise ValueError('exactly 21 hand landmarks are required')
    points = [(float(p[0]), float(p[1])) for p in landmarks]
    vector = normalise_landmarks(points)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    record = {'label':label,'handedness':handedness,'landmarks':points,'features':vector}
    with target.open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(record) + '\n')
    return record


def load_samples(path):
    target = Path(path)
    if not target.exists():
        return []
    return [json.loads(line) for line in target.read_text(encoding='utf-8').splitlines() if line.strip()]
