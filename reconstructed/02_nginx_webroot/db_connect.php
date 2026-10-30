<?php
// [RECONSTRUCTED] Shared PHP DB connection. Do not expose this file as documentation.
function safewatch_db(): mysqli {
    $host = getenv('SAFEWATCH_DB_HOST') ?: '127.0.0.1';
    $user = getenv('SAFEWATCH_DB_USER') ?: 'safewatch';
    $pass = getenv('SAFEWATCH_DB_PASSWORD');
    $name = getenv('SAFEWATCH_DB_NAME') ?: 'safewatch';
    $port = (int)(getenv('SAFEWATCH_DB_PORT') ?: '3306');
    if ($pass === false) {
        throw new RuntimeException('Database credentials are not configured');
    }
    mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
    $db = new mysqli($host, $user, $pass, $name, $port);
    $db->set_charset('utf8mb4');
    return $db;
}
function safewatch_camera_id(): int {
    $id = (int)(getenv('SAFEWATCH_CAMERA_NUMBER') ?: '1');
    return max(1, $id);
}
function safewatch_json($value, int $status = 200): void {
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store, private');
    header('X-Content-Type-Options: nosniff');
    echo json_encode($value, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR);
}
function safewatch_api_error(Throwable $e): void {
    error_log('[SafeWatch] DB/API error: ' . $e->getMessage());
    safewatch_json(['error' => 'DB 데이터 조회에 실패했습니다. 서버 설정과 로그를 확인하세요.'], 503);
}
