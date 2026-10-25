from flask import Flask, jsonify, render_template, request

from src.gesture_engine import DynamicGestureTracker, PredictionSmoother, SentenceBuilder, classify_static

app = Flask(__name__)
tracker = DynamicGestureTracker()
smoother = PredictionSmoother()
sentence = SentenceBuilder()


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/health')
def health():
    return jsonify({'status':'ok','service':'hand-sign-live'})


@app.post('/api/predict')
def predict():
    payload = request.get_json(silent=True) or {}
    points = payload.get('landmarks') or []
    handedness = payload.get('handedness', 'Right')
    try:
        static = classify_static(points, handedness)
        dynamic = tracker.update(points)
    except (TypeError, ValueError) as exc:
        return jsonify({'error':str(exc)}), 400
    raw_label = dynamic or static['label']
    stable_label, stability = smoother.update(raw_label)
    text = sentence.push(stable_label) if stability >= .6 else sentence.text
    return jsonify({**static,'raw_label':raw_label,'label':stable_label,'stability':stability,'sentence':text})


@app.post('/api/sentence/clear')
def clear_sentence():
    return jsonify({'sentence':sentence.clear()})


@app.post('/api/sentence/space')
def reset_debounce():
    sentence.reset_debounce()
    return jsonify({'sentence':sentence.text})


if __name__ == '__main__':
    app.run(debug=True)
