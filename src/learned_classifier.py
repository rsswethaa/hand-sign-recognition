from pathlib import Path

from .features import normalise_landmarks


class LearnedGestureClassifier:
    """Optional scikit-learn gesture model loaded from a joblib artifact."""
    def __init__(self, model_path='models/gesture_classifier.joblib'):
        self.model_path = Path(model_path)
        self._model = None

    @property
    def available(self):
        return self.model_path.exists()

    def _load(self):
        if self._model is None:
            if not self.available:
                raise FileNotFoundError(self.model_path)
            try:
                import joblib
            except ImportError as exc:
                raise RuntimeError('Install requirements-training.txt to load the trained classifier') from exc
            self._model = joblib.load(self.model_path)
        return self._model

    def predict(self, landmarks):
        points = [(float(p[0]), float(p[1])) for p in landmarks]
        vector = normalise_landmarks(points)
        model = self._load()
        label = str(model.predict([vector])[0])
        confidence = None
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba([vector])[0]
            confidence = float(max(probabilities))
        return {'label': label, 'confidence': confidence, 'model': self.model_path.name}
