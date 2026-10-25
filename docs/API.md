# Interface Contracts

Core recognition interfaces live under `src/` and are demonstrated by `demo.py`.

Persistence interfaces:
- `init_db(path, seed=False)`
- `create_session(path, source_name)`
- `save_detection(path, session_id, frame_number, label, confidence, features, landmark_count, model_version)`

A production service could add authenticated image/video ingestion and return detections through REST/WebSocket endpoints.
