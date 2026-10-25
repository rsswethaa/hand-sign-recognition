from pathlib import Path

from flask import Flask, jsonify, render_template, request

from src.gesture_engine import DynamicGestureTracker, PredictionSmoother, SentenceBuilder, classify_static
from src.learned_classifier import LearnedGestureClassifier
from src.sample_store import append_sample, load_samples

app = Flask(__name__)
tracker = DynamicGestureTracker()
smoother = PredictionSmoother()
sentence = SentenceBuilder()
learned = LearnedGestureClassifier()
SAMPLE_PATH = Path('training_data/landmarks.jsonl')


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/health')
def health():
    return jsonify({'status':'ok','service':'hand-sign-live','trained_model_available':learned.available})


@app.post('/api/predict')
def predict():
    payload = request.get_json(silent=True) or {}
    points = payload.get('landmarks') or []
    handedness = payload.get('handedness', 'Right')
    try:
        rule = classify_static(points, handedness)
        dynamic = tracker.update(points)
        model_source = 'rule-baseline'
        if learned.available:
            try:
                trained = learned.predict(points)
                rule = {**rule, 'label':trained['label'], 'confidence':trained['confidence'] if trained['confidence'] is not None else rule.get('confidence', .5)}
                model_source = trained['model']
            except Exception:
                model_source = 'rule-baseline-fallback'
    except (TypeError, ValueError) as exc:
        return jsonify({'error':str(exc)}), 400
    raw_label = dynamic or rule['label']
    stable_label, stability = smoother.update(raw_label)
    text = sentence.push(stable_label) if stability >= .6 else sentence.text
    return jsonify({**rule,'raw_label':raw_label,'label':stable_label,'stability':stability,'sentence':text,'model_source':model_source})


@app.post('/api/training/sample')
def collect_training_sample():
    payload = request.get_json(silent=True) or {}
    try:
        record = append_sample(SAMPLE_PATH, payload.get('label'), payload.get('landmarks') or [], payload.get('handedness','Right'))
    except (TypeError, ValueError) as exc:
        return jsonify({'error':str(exc)}), 400
    return jsonify({'saved':True,'label':record['label'],'sample_count':len(load_samples(SAMPLE_PATH))})


@app.get('/api/training/status')
def training_status():
    samples = load_samples(SAMPLE_PATH)
    counts = {}
    for row in samples:
        counts[row['label']] = counts.get(row['label'], 0) + 1
    return jsonify({'sample_count':len(samples),'by_label':counts,'trained_model_available':learned.available})


@app.post('/api/sentence/clear')
def clear_sentence():
    return jsonify({'sentence':sentence.clear()})


@app.post('/api/sentence/space')
def reset_debounce():
    sentence.reset_debounce()
    return jsonify({'sentence':sentence.text})


if __name__ == '__main__':
    app.run(debug=True)
