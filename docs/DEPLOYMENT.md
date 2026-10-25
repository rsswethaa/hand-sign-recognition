# Setup and Deployment

```bash
git clone https://github.com/rsswethaa/hand-sign-recognition.git
cd hand-sign-recognition
python demo.py
python -m unittest discover -s tests -v
```

Optional database:
```bash
python -c "from src.storage import init_db; init_db('handsigns.db', seed=True)"
```

A full deployment would add a camera/MediaPipe-style landmark adapter, model-serving layer, managed database, observability and device/performance testing.
