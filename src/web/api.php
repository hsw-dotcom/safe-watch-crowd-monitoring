<?php
/** Single read-only JSON API for the reconstructed PHP dashboard (no hardware required to review). */
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store, private');
header('X-Content-Type-Options: nosniff');

function respond($payload, int $status = 200): void {
    http_response_code($status);
    echo json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR);
}

$view = $_GET['view'] ?? 'latest';
if (!in_array($view, ['latest', 'history'], true)) {
    respond(['error' => '지원하지 않는 조회 유형입니다.'], 400);
    exit;
}

try {
    $password = getenv('SAFEWATCH_DB_PASSWORD');
    if ($password === false) {
        throw new RuntimeException('Database credentials missing');
    }
    mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
    $db = new mysqli(
        getenv('SAFEWATCH_DB_HOST') ?: '127.0.0.1',
        getenv('SAFEWATCH_DB_USER') ?: 'safewatch',
        $password,
        getenv('SAFEWATCH_DB_NAME') ?: 'safewatch',
        (int)(getenv('SAFEWATCH_DB_PORT') ?: 3306)
    );
    $db->set_charset('utf8mb4');
    $camera = max(1, (int)(getenv('SAFEWATCH_CAMERA_NUMBER') ?: 1));
    try {
        if ($view === 'latest') {
            $sql = "SELECT id, camera_number, crowd_density, danger_level,
                           DATE_FORMAT(update_time, '%Y-%m-%d %H:%i:%s') AS update_time
                    FROM receive_data WHERE camera_number = ? ORDER BY id DESC LIMIT 1";
            $stmt = $db->prepare($sql);
            $stmt->bind_param('i', $camera);
            $stmt->execute();
            $row = $stmt->get_result()->fetch_assoc();
            if ($row !== null) {
                $row['id'] = (int)$row['id'];
                $row['camera_number'] = (int)$row['camera_number'];
                $row['crowd_density'] = (float)$row['crowd_density'];
            }
            $stmt->close();
            respond($row);
        } else {
            $sql = "SELECT id, crowd_density, change_rate,
                           update_time AS time_label
                    FROM density WHERE camera_number = ? ORDER BY id DESC LIMIT 20";
            $stmt = $db->prepare($sql);
            $stmt->bind_param('i', $camera);
            $stmt->execute();
            $rows = $stmt->get_result()->fetch_all(MYSQLI_ASSOC);
            $stmt->close();
            foreach ($rows as &$row) {
                $row['id'] = (int)$row['id'];
                $row['crowd_density'] = (float)$row['crowd_density'];
                $row['change_rate'] = $row['change_rate'] === null ? null : (float)$row['change_rate'];
            }
            unset($row);
            respond(array_reverse($rows));
        }
    } finally {
        $db->close();
    }
} catch (Throwable $e) {
    error_log('[Safe Watch API] ' . $e->getMessage());
    respond(['error' => '데이터를 조회할 수 없습니다.'], 503);
}
