# Training a Gesture Classifier

SignFlow can operate in two modes:

1. a transparent rule baseline for the built-in demo gestures;
2. an optional learned classifier trained from webcam landmarks captured in the product.

## Collect samples

1. Run `python app.py` and open the web interface.
2. Start the camera.
3. Enter a gesture label in **Collect real training samples**.
4. Hold the gesture in different positions, distances and orientations and capture repeated examples.
5. Repeat for multiple users and for every target class.

Samples are stored locally in `training_data/landmarks.jsonl` and are intentionally ignored by Git because real hand data should not be committed casually.

## Train

```bash
pip install -r requirements-training.txt
python training/train_classifier.py training_data/landmarks.jsonl
```

The script creates `models/gesture_classifier.joblib`, prints a confusion matrix and classification report, and uses a stratified holdout set. Once the model artifact exists, the Flask app automatically prefers it for static-gesture inference and keeps the rule engine as a fallback.

## Evaluation guidance

Do not evaluate with random frames from the same recording split across train and test. A stronger experiment separates users/signers so the test set measures generalisation to unseen people. Report per-class precision/recall, the confusion matrix, sample counts, camera conditions and signer diversity.

A serious sign-language system would also require temporal sequences, orientation, movement, facial/body cues and language grammar rather than treating isolated hand poses as complete signs.
