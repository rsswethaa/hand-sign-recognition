import math


def normalise_landmarks(points: list[tuple[float, float]]) -> list[float]:
    if len(points) < 2:
        raise ValueError("at least two landmarks are required")
    wrist_x, wrist_y = points[0]
    shifted = [(x - wrist_x, y - wrist_y) for x, y in points]
    scale = max(math.hypot(x, y) for x, y in shifted)
    if scale == 0:
        raise ValueError("landmarks must not all overlap")
    vector = []
    for x, y in shifted:
        vector.extend([round(x / scale, 6), round(y / scale, 6)])
    return vector


def euclidean(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("feature vectors must have equal length")
    return math.sqrt(sum((x-y)**2 for x, y in zip(a, b)))
