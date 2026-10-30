-- [RECONSTRUCTED] MariaDB 10.2+ (window functions) reference schema.
-- Creates a new database. On an existing DB, review/migrate before executing.
CREATE DATABASE IF NOT EXISTS safewatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE safewatch;

CREATE TABLE IF NOT EXISTS cameras (
   camera_number INT PRIMARY KEY AUTO_INCREMENT,
   location VARCHAR(100) NOT NULL,
   status ENUM('active','inactive') NOT NULL DEFAULT 'active',
   last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO cameras (camera_number, location, status)
VALUES (1, '명지대학교 골목 1', 'active')
ON DUPLICATE KEY UPDATE location=VALUES(location);

CREATE TABLE IF NOT EXISTS receive_data (
   id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
   camera_number INT NOT NULL DEFAULT 1,
   people_count INT NOT NULL DEFAULT 0,
   crowd_density DOUBLE NOT NULL,
   update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   danger_level ENUM('안전','경고','위험') NOT NULL DEFAULT '안전',
   INDEX idx_camera_measurement (camera_number, id),
   CONSTRAINT fk_measurement_camera FOREIGN KEY (camera_number)
       REFERENCES cameras(camera_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Per-camera previous sample, unlike historical JOIN id = previous.id+1.
-- First row and previous density=0 have NULL percentage change, not division error.
CREATE OR REPLACE VIEW density AS
SELECT t.id, t.camera_number, t.crowd_density, t.update_time,
   CAST(CASE WHEN t.previous_density IS NULL THEN NULL
        ELSE t.crowd_density - t.previous_density END AS DECIMAL(12,4)) AS change_amount,
   CAST(CASE WHEN t.previous_density IS NULL OR t.previous_density = 0 THEN NULL
        ELSE ((t.crowd_density - t.previous_density) / t.previous_density) * 100 END AS DECIMAL(12,2)) AS change_rate
FROM (
   SELECT r.id, r.camera_number, r.crowd_density, r.update_time,
          LAG(r.crowd_density) OVER (PARTITION BY r.camera_number ORDER BY r.id) AS previous_density
   FROM receive_data AS r
) AS t;
