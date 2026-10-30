<?php
require_once __DIR__ . '/db_connect.php';
try {
    $db = safewatch_db();
    $camera = safewatch_camera_id();
    // density VIEW handles previous row from the SAME camera; protects zero denominator.
    $stmt = $db->prepare('SELECT change_rate, change_amount,
                                  DATE_FORMAT(update_time, "%H:%i:%s") AS time_label
                           FROM density WHERE camera_number = ? ORDER BY id DESC LIMIT 20');
    $stmt->bind_param('i', $camera);
    $stmt->execute();
    $rows = $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
    $stmt->close();
    $db->close();
    foreach ($rows as &$row) {
        $row['change_rate'] = $row['change_rate'] === null ? null : (float)$row['change_rate'];
        $row['change_amount'] = $row['change_amount'] === null ? null : (float)$row['change_amount'];
    }
    unset($row);
    safewatch_json(array_reverse($rows));
} catch (Throwable $e) { safewatch_api_error($e); }
