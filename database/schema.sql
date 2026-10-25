PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS gesture_classes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  label TEXT NOT NULL UNIQUE,
  description TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS recognition_sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_name TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS detections (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL,
  frame_number INTEGER NOT NULL CHECK(frame_number >= 0),
  predicted_class_id INTEGER,
  confidence REAL CHECK(confidence IS NULL OR confidence BETWEEN 0 AND 1),
  model_version TEXT NOT NULL DEFAULT 'prototype-baseline-v1',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(session_id) REFERENCES recognition_sessions(id) ON DELETE CASCADE,
  FOREIGN KEY(predicted_class_id) REFERENCES gesture_classes(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS landmark_features (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  detection_id INTEGER NOT NULL UNIQUE,
  feature_json TEXT NOT NULL,
  landmark_count INTEGER NOT NULL CHECK(landmark_count > 0),
  FOREIGN KEY(detection_id) REFERENCES detections(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_detections_session ON detections(session_id);
CREATE INDEX IF NOT EXISTS idx_detections_class ON detections(predicted_class_id);
