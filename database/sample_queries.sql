-- Recognition audit
SELECT s.source_name, d.frame_number, g.label, d.confidence, d.model_version, d.created_at
FROM detections d
JOIN recognition_sessions s ON s.id=d.session_id
LEFT JOIN gesture_classes g ON g.id=d.predicted_class_id
ORDER BY d.id DESC;

-- Label distribution
SELECT COALESCE(g.label,'UNKNOWN') AS label, COUNT(*) AS detections, ROUND(AVG(d.confidence),3) AS avg_confidence
FROM detections d LEFT JOIN gesture_classes g ON g.id=d.predicted_class_id
GROUP BY g.label ORDER BY detections DESC;
