-- 2023 Safe Watch source schema with only minimal setup fixes.
-- Historical columns and the historical density-change view are preserved.
CREATE DATABASE IF NOT EXISTS safewatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE safewatch;

CREATE TABLE IF NOT EXISTS cameras (
  camera_number INT PRIMARY KEY AUTO_INCREMENT,
  location VARCHAR(100),
  status ENUM('active', 'inactive') DEFAULT 'active',
  last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- The old source omitted an initial cameras row while receive_data had a foreign key.
-- This seed is a reconstruction/setup fix, NOT an original 2023 SQL statement.
INSERT INTO cameras (camera_number, location, status)
VALUES (1, '명지대학교 골목 1', 'active')
ON DUPLICATE KEY UPDATE location=VALUES(location);

CREATE TABLE IF NOT EXISTS receive_data (
  id INT PRIMARY KEY AUTO_INCREMENT,
  camera_number INT DEFAULT 1,
  crowd_density FLOAT,
  update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  danger_level ENUM('안전', '경고', '위험') DEFAULT '안전',
  FOREIGN KEY (camera_number) REFERENCES cameras(camera_number)
);

-- Intentionally close to 2023 original: previous id+1 lookup, change_rate (%).
-- Historical original checked only previous IS NULL; division by previous=0
-- was NOT explicitly handled. MariaDB can yield NULL and/or warnings.
CREATE OR REPLACE VIEW density AS
SELECT
  current.id,
  current.camera_number,
  current.crowd_density,
  CAST(CASE WHEN previous.crowd_density IS NULL THEN 0
       ELSE ((current.crowd_density - previous.crowd_density)
             / previous.crowd_density) * 100 END AS DECIMAL(5,2)) AS change_rate,
  DATE_FORMAT(current.update_time, '%H:%i:%s') AS update_time
FROM receive_data AS current
LEFT JOIN receive_data AS previous
  ON current.camera_number = previous.camera_number
 AND current.id = previous.id + 1;
