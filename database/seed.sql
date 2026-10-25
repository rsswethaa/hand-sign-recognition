INSERT OR IGNORE INTO gesture_classes(label, description) VALUES
('OPEN_PALM','Open-palm demonstration class'),
('FIST','Closed-fist demonstration class'),
('POINT','Index-point demonstration class');

INSERT INTO recognition_sessions(source_name)
SELECT 'synthetic-demo' WHERE NOT EXISTS (SELECT 1 FROM recognition_sessions WHERE source_name='synthetic-demo');
