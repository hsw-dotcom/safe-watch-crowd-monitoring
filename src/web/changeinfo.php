<?php
$servername = "127.0.0.1";
$username = getenv('SAFEWATCH_DB_USER') ?: 'root';
$password = getenv('SAFEWATCH_DB_PASSWORD');
$dbname = "safewatch";
$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("데이터베이스 연결 실패: " . $conn->connect_error);
}
$sql = "SELECT * FROM density ORDER BY id DESC LIMIT 20";
$result = $conn->query($sql);
$data = [];
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $data[] = [
            'time_label' => $row['update_time'],
            'change_rate' => $row['change_rate'],
        ];
    }
}
$conn->close();
$data = array_reverse($data);
header('Content-Type: application/json');
echo json_encode($data);
?>
