# Accessibility Use Cases and Limits

## Potential use cases
SignFlow can demonstrate hands-free or gesture-based interaction where speech or keyboard input is inconvenient, including classroom demos, accessibility research, kiosk controls, rehabilitation exercises and simple phrase-building experiments.

## Important limits
The built-in vocabulary is a gesture demo, not a certified sign-language interpreter. Natural sign languages depend on hand shape, orientation, movement, location, facial expression, body posture, spatial grammar and community-specific language conventions.

## Inclusive design considerations
A production accessibility tool should support:

- configurable gesture vocabularies rather than imposing one fixed set;
- left/right handedness and varied mobility;
- adjustable camera framing and confidence thresholds;
- visible and non-audio feedback;
- keyboard/touch alternatives when camera recognition fails;
- signer-independent testing across skin tones, hand sizes, lighting and backgrounds;
- local processing or strong privacy controls for camera data;
- co-design with Deaf and disabled users rather than assuming their needs.

The portfolio UI keeps video processing in the browser for landmark extraction and sends only normalised landmark coordinates to the Python inference API.
