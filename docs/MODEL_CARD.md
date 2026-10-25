# Model Card — Prototype Baseline v1

## Intended use
Educational static hand-sign recognition from normalised landmark features.

## Inputs
Hand landmark coordinates or derived normalised feature vectors.

## Outputs
Gesture label and distance-derived confidence-like value.

## Limitations
No camera benchmark accuracy is claimed. The baseline does not model dynamic gestures and may be sensitive to landmark-detector errors, viewpoint, handedness and sign variation. Confidence is not calibrated.

## Future model
A trained classifier could use landmark sequences or image features with representative datasets and signer-independent evaluation.
