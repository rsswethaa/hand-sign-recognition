import sqlite3
import tempfile
import unittest
from pathlib import Path

from src.storage import create_session, init_db, save_detection


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / 'handsigns.db'
        init_db(self.db, seed=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_detection_is_persisted(self):
        session = create_session(self.db, 'camera-1')
        detection = save_detection(self.db, session, 3, 'OPEN_PALM', 0.88, [0.1,0.2,0.3], 21)
        with sqlite3.connect(self.db) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM detections').fetchone()[0], 1)
            self.assertEqual(db.execute('SELECT landmark_count FROM landmark_features WHERE detection_id=?',(detection,)).fetchone()[0], 21)


if __name__ == '__main__':
    unittest.main()
