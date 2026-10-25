# Technical Project Report — Hand Sign Recognition

## Executive summary
This project implements an end-to-end recognition layer for hand-sign analysis: landmark normalisation, feature extraction, classification, persistent detection history and evaluation-ready database records.

## 1. Problem
Hand-sign recognition must represent hand shape robustly despite translation, scale, signer and camera variation.

## 2. Objective
Create a reproducible ML pipeline whose feature/classification layers can be tested without requiring a camera library, while keeping a clear path to real-time CV integration.

## 3. Method
Landmarks are translated relative to the wrist and scaled by maximum radial distance. A nearest-prototype baseline demonstrates classification independently from a detector vendor.

## 4. Data model
Recognition sessions contain detections; detections reference controlled gesture classes and store versioned confidence plus serialised landmark features. SQL queries support distribution and audit analysis.

## 5. Testing
Tests validate geometry invariance, classification and persistence. CI compiles modules and runs all tests.

## 6. Privacy
Real camera data requires consent/notice, minimised retention and secure access. This project does not perform identity or sensitive-trait inference.

## 7. Limitations
No real-camera benchmark, trained detector, dynamic-gesture evaluation or production confidence calibration is claimed.

## 8. Future work
MediaPipe integration, temporal gestures, learned classifiers, augmentation, signer-independent datasets, confusion matrices and accessibility-oriented user studies.

## Conclusion
The repository includes working code, persistence, SQL assets, ER/data-flow diagrams, tests, CI, deployment/security docs, model documentation and a full technical report.
