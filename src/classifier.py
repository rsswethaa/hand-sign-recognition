from .features import euclidean

class PrototypeClassifier:
    def __init__(self, prototypes: dict[str, list[float]]):
        if not prototypes:
            raise ValueError("at least one prototype is required")
        self.prototypes = prototypes

    def predict(self, vector: list[float]) -> dict:
        distances = {label: euclidean(vector, proto) for label, proto in self.prototypes.items()}
        label = min(distances, key=distances.get)
        distance = distances[label]
        confidence = round(1 / (1 + distance), 3)
        return {"label": label, "confidence": confidence, "distance": round(distance, 4)}
