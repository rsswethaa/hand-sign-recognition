import tempfile
import unittest
from pathlib import Path

from src.sample_store import append_sample, load_samples


def landmarks():
    return [[0.5,0.8]] + [[0.3 + (i%4)*0.1, 0.2 + (i//4)*0.1] for i in range(20)]


class TrainingDataTests(unittest.TestCase):
    def test_capture_and_reload_real_landmark_sample(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'samples.jsonl'
            record=append_sample(path,'hello',landmarks(),'Right')
            rows=load_samples(path)
            self.assertEqual(record['label'],'HELLO')
            self.assertEqual(len(record['features']),42)
            self.assertEqual(len(rows),1)
            self.assertEqual(rows[0]['handedness'],'Right')

    def test_requires_21_landmarks(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                append_sample(Path(tmp)/'samples.jsonl','bad',[[0,0]])


if __name__=='__main__':
    unittest.main()
