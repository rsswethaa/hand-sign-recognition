# Hand Sign Recognition

A machine-learning/computer-vision portfolio project for recognising hand signs from normalised hand-landmark features.

## Features
- landmark normalisation relative to wrist position
- scale-invariant feature vectors
- nearest-prototype sign classification baseline
- confidence estimation from feature distance
- synthetic sample landmarks for reproducible testing
- tests, CI, architecture and report

## Architecture
```mermaid
flowchart LR
  C[Camera frame] --> H[Hand landmark detector]
  H --> N[Normalisation]
  N --> V[Feature vector]
  V --> M[ML classifier]
  M --> L[Sign label + confidence]
```

## Run
```bash
python demo.py
python -m unittest discover -s tests -v
```

The repository implements the feature and classification layers without claiming trained-camera benchmark accuracy. A production CV version would connect these modules to a hand detector such as MediaPipe and a validated trained classifier.
