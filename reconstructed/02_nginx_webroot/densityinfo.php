<?php
require_once __DIR__ . '/db_connect.php';
try {
    $db = safewatch_db();
    $camera = safewatch_camera_id();
    $stmt = $db->prepare('SELECT crowd_density, DATE_FORMAT(update_time, "%H:%i:%s") AS time_label
                          FROM receive_data WHERE camera_number = ? ORDER BY id DESC LIMIT 20');
    $stmt->bind_param('i', $camera);
    $stmt->execute();
    $rows = $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
    $stmt->close();
    $db->close();
    foreach ($rows as &$row) { $row['crowd_density'] = (float)$row['crowd_density']; }
    unset($row);
    safewatch_json(array_reverse($rows));
} catch (Throwable $e) { safewatch_api_error($e); }
