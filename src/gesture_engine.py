from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass

TIP_IDS = [4, 8, 12, 16, 20]
PIP_IDS = [3, 6, 10, 14, 18]


def _validate(points):
    if len(points) != 21:
        raise ValueError('exactly 21 MediaPipe hand landmarks are required')
    return [(float(p[0]), float(p[1])) for p in points]


def finger_states(points, handedness='Right'):
    p = _validate(points)
    thumb_open = p[4][0] < p[3][0] if handedness.lower() == 'right' else p[4][0] > p[3][0]
    extended = [thumb_open]
    for tip, pip in zip(TIP_IDS[1:], PIP_IDS[1:]):
        extended.append(p[tip][1] < p[pip][1])
    return extended


def classify_static(points, handedness='Right'):
    p = _validate(points)
    t, i, m, r, pinky = finger_states(p, handedness)
    states = [t, i, m, r, pinky]
    label = 'UNKNOWN'
    if all(states):
        label = 'OPEN_PALM'
    elif not any(states):
        label = 'FIST'
    elif i and not any([m, r, pinky]):
        label = 'POINT'
    elif i and m and not r and not pinky:
        label = 'V_SIGN'
    elif t and not any([i, m, r, pinky]):
        label = 'THUMBS_UP'
    elif t and i and pinky and not m and not r:
        label = 'I_LOVE_YOU'

    confidence = 0.95 if label != 'UNKNOWN' else 0.35
    return {'label': label, 'confidence': confidence, 'finger_states': states}


class DynamicGestureTracker:
    def __init__(self, window=8, threshold=0.22):
        self.x = deque(maxlen=window)
        self.threshold = threshold

    def update(self, points):
        p = _validate(points)
        self.x.append(p[0][0])
        if len(self.x) < self.x.maxlen:
            return None
        displacement = self.x[-1] - self.x[0]
        if displacement > self.threshold:
            self.x.clear()
            return 'SWIPE_RIGHT'
        if displacement < -self.threshold:
            self.x.clear()
            return 'SWIPE_LEFT'
        return None


class PredictionSmoother:
    def __init__(self, window=5):
        self.labels = deque(maxlen=window)

    def update(self, label):
        self.labels.append(label)
        winner, count = Counter(self.labels).most_common(1)[0]
        return winner, round(count / len(self.labels), 2)


DEFAULT_WORDS = {
    'OPEN_PALM': 'hello',
    'FIST': 'stop',
    'POINT': 'there',
    'V_SIGN': 'two',
    'THUMBS_UP': 'yes',
    'I_LOVE_YOU': 'love',
    'SWIPE_RIGHT': 'next',
    'SWIPE_LEFT': 'back',
}


class SentenceBuilder:
    def __init__(self, max_words=12):
        self.words = deque(maxlen=max_words)
        self.last_label = None

    def push(self, label):
        if label in ('UNKNOWN', None) or label == self.last_label:
            return self.text
        word = DEFAULT_WORDS.get(label, label.lower().replace('_', ' '))
        self.words.append(word)
        self.last_label = label
        return self.text

    def reset_debounce(self):
        self.last_label = None

    @property
    def text(self):
        return ' '.join(self.words)

    def clear(self):
        self.words.clear()
        self.last_label = None
        return ''
