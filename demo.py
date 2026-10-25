from src.features import normalise_landmarks
from src.classifier import PrototypeClassifier

open_hand = normalise_landmarks([(0,0),(0,1),(1,1),(1,0)])
fist = normalise_landmarks([(0,0),(0.2,0.2),(0.3,0.2),(0.2,0.3)])
model = PrototypeClassifier({"OPEN_HAND": open_hand, "FIST": fist})
sample = normalise_landmarks([(10,10),(10,12),(12,12),(12,10)])
print(model.predict(sample))
