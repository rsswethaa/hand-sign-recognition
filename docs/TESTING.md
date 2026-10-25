# Testing Strategy

Automated tests validate landmark normalisation, translation/scale invariance, prototype classification, invalid-input behaviour and SQLite persistence.

Run:
```bash
python -m unittest discover -s tests -v
```

Future evaluation should use signer-independent train/test splits, diverse skin tones/backgrounds/lighting, handedness and viewpoint variation, confusion matrices and dynamic-gesture tests.
