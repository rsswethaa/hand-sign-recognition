# Technical Report

## Problem
Hand-sign recognition requires robust representation of hand shape despite changes in position and scale.

## Objective
Build a testable recognition pipeline that transforms hand landmarks into normalised features and classifies gestures.

## Method
Landmarks are translated relative to the wrist and scaled by maximum radial distance. A nearest-prototype baseline demonstrates classification independently of a camera library.

## Evaluation
Tests validate translation/scale invariance, correct prototype classification and rejection of invalid input.

## Limitations
No real-camera dataset, trained detector, lighting evaluation or benchmark accuracy is claimed. Real systems must address viewpoint, occlusion, handedness, motion and signer diversity.

## Future work
MediaPipe integration, dynamic gestures, temporal models, data augmentation, confusion matrices and accessibility-oriented user studies.
