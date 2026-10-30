<?php
require_once __DIR__ . '/db_connect.php';
try {
    $db = safewatch_db();
    $camera = safewatch_camera_id();
    $stmt = $db->prepare('SELECT id, camera_number, people_count, crowd_density, danger_level,
                                 DATE_FORMAT(update_time, "%Y-%m-%d %H:%i:%s") AS update_time
                          FROM receive_data WHERE camera_number = ? ORDER BY id DESC LIMIT 1');
    $stmt->bind_param('i', $camera);
    $stmt->execute();
    $row = $stmt->get_result()->fetch_assoc();
    $stmt->close();
    $db->close();
    // Legacy frontend expected a one-element array. Empty array indicates no measurements.
    if ($row !== null) {
        $row['id'] = (int)$row['id'];
        $row['camera_number'] = (int)$row['camera_number'];
        $row['people_count'] = (int)$row['people_count'];
        $row['crowd_density'] = (float)$row['crowd_density'];
    }
    safewatch_json($row === null ? [] : [$row]);
} catch (Throwable $e) { safewatch_api_error($e); }
