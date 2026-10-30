-- OPTIONAL, manually reviewed migration for a DB created from 2023 archive.
-- Backup your database first. Run once after confirming actual column names.
USE safewatch;
ALTER TABLE receive_data ADD COLUMN IF NOT EXISTS people_count INT NOT NULL DEFAULT 0;
-- To avoid dropping data or mismatching interleaved cameras, rebuild view only.
CREATE OR REPLACE VIEW density AS
SELECT t.id, t.camera_number, t.crowd_density, t.update_time,
   CAST(CASE WHEN t.previous_density IS NULL THEN NULL
             ELSE t.crowd_density - t.previous_density END AS DECIMAL(12,4)) AS change_amount,
   CAST(CASE WHEN t.previous_density IS NULL OR t.previous_density = 0 THEN NULL
             ELSE 100 * (t.crowd_density - t.previous_density) / t.previous_density END AS DECIMAL(12,2)) AS change_rate
FROM (
    SELECT id, camera_number, crowd_density, update_time,
        LAG(crowd_density) OVER (PARTITION BY camera_number ORDER BY id) AS previous_density
    FROM receive_data
) AS t;
-- Historical rows cannot have people_count back-calculated with certainty; defaults to 0.
