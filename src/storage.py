from pathlib import Path
import json
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'database' / 'schema.sql'
SEED = ROOT / 'database' / 'seed.sql'


def connect(db_path):
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db


def init_db(db_path, seed=False):
    with connect(db_path) as db:
        db.executescript(SCHEMA.read_text(encoding='utf-8'))
        if seed:
            db.executescript(SEED.read_text(encoding='utf-8'))
    return Path(db_path)


def create_session(db_path, source_name):
    with connect(db_path) as db:
        cur = db.execute('INSERT INTO recognition_sessions(source_name) VALUES (?)', (source_name,))
        return cur.lastrowid


def save_detection(db_path, session_id, frame_number, label, confidence, features, landmark_count, model_version='prototype-baseline-v1'):
    with connect(db_path) as db:
        cls = db.execute('SELECT id FROM gesture_classes WHERE label=?', (label,)).fetchone()
        class_id = cls['id'] if cls else None
        cur = db.execute('''INSERT INTO detections(session_id,frame_number,predicted_class_id,confidence,model_version)
                            VALUES (?,?,?,?,?)''', (session_id, frame_number, class_id, float(confidence), model_version))
        detection_id = cur.lastrowid
        db.execute('INSERT INTO landmark_features(detection_id,feature_json,landmark_count) VALUES (?,?,?)',
                   (detection_id, json.dumps(features), int(landmark_count)))
        return detection_id
