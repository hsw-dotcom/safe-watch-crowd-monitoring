<?php
$servername = "127.0.0.1";
$username = getenv('SAFEWATCH_DB_USER') ?: 'root';
$password = getenv('SAFEWATCH_DB_PASSWORD');
$dbname = "safewatch";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("데이터베이스 연결 실패: " . $conn->connect_error);
}
$sql = "SELECT * FROM receive_data ORDER BY id DESC LIMIT 1";
$result = $conn->query($sql);
$data = [];
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $crowd_density = $row['crowd_density'];
        $danger_level = $row['danger_level'];
        $data[] = [
            'crowd_density' => $crowd_density,
            'danger_level' => $danger_level,
        ];
    }
}
$conn->close();
header('Content-Type: application/json');
echo json_encode($data);
?>
