# Architecture

```mermaid
sequenceDiagram
  participant F as Camera Frame
  participant D as Hand Detector
  participant N as Normaliser
  participant C as Classifier
  F->>D: image
  D-->>N: hand landmarks
  N-->>C: scale/translation-normalised vector
  C-->>F: sign + confidence
```

The current repository implements deterministic feature processing and a nearest-prototype ML baseline. A full camera application can replace the detector boundary with MediaPipe Hands or another keypoint model and train an SVM, random forest or neural classifier on labelled gestures.
