import unittest
from src.features import normalise_landmarks
from src.classifier import PrototypeClassifier

class HandSignTests(unittest.TestCase):
    def test_translation_and_scale_invariance(self):
        a = normalise_landmarks([(0,0),(0,1),(1,1),(1,0)])
        b = normalise_landmarks([(10,10),(10,12),(12,12),(12,10)])
        self.assertEqual(a, b)

    def test_prediction(self):
        open_hand = normalise_landmarks([(0,0),(0,1),(1,1),(1,0)])
        fist = normalise_landmarks([(0,0),(0.2,0.2),(0.3,0.2),(0.2,0.3)])
        model = PrototypeClassifier({"OPEN_HAND": open_hand, "FIST": fist})
        self.assertEqual(model.predict(open_hand)["label"], "OPEN_HAND")

    def test_bad_landmarks(self):
        with self.assertRaises(ValueError):
            normalise_landmarks([(0,0)])

if __name__ == "__main__":
    unittest.main()
