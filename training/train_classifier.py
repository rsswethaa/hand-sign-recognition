"""Train a gesture classifier from landmark samples captured by SignFlow.

Usage:
  pip install -r requirements-training.txt
  python training/train_classifier.py training_data/landmarks.jsonl
"""
import argparse
import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split


def load_jsonl(path):
    rows = [json.loads(line) for line in Path(path).read_text(encoding='utf-8').splitlines() if line.strip()]
    if len(rows) < 20:
        raise ValueError('collect at least 20 labelled samples before training')
    X = np.asarray([row['features'] for row in rows], dtype=float)
    y = np.asarray([row['label'] for row in rows])
    if len(set(y)) < 2:
        raise ValueError('collect samples for at least two gesture classes')
    return X, y


def train(path, output='models/gesture_classifier.joblib'):
    X, y = load_jsonl(path)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25, stratify=y, random_state=42)
    model = RandomForestClassifier(n_estimators=300, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    report = classification_report(y_test, pred, output_dict=True, zero_division=0)
    labels = sorted(set(y))
    matrix = confusion_matrix(y_test, pred, labels=labels).tolist()
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output)
    return {'model_path':output,'labels':labels,'confusion_matrix':matrix,'classification_report':report,'n_train':len(y_train),'n_test':len(y_test)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('samples')
    parser.add_argument('--output', default='models/gesture_classifier.joblib')
    args = parser.parse_args()
    print(json.dumps(train(args.samples, args.output), indent=2))


if __name__ == '__main__':
    main()
