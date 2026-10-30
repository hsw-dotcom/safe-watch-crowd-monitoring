<?php
    // 데이터베이스 연결 설정
    $servername = "127.0.0.1";
    $username = getenv('SAFEWATCH_DB_USER') ?: 'root';
    $password = getenv('SAFEWATCH_DB_PASSWORD');
    $dbname = "safewatch";

    // 데이터베이스 연결 생성
    $conn = new mysqli($servername, $username, $password, $dbname);

    // 연결 확인
    if ($conn->connect_error) {
        die("데이터베이스 연결 실패: " . $conn->connect_error);
    }

    // 데이터베이스에서 데이터 가져오기
    $sql = "SELECT * FROM density ORDER BY id DESC LIMIT 20";
    $result = $conn->query($sql);

    // 가져온 데이터 저장할 배열 초기화
    $data = [];
    // 가져온 데이터 배열에 저장
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            $time_label = $row['update_time'];
            $change_rate = $row['change_rate'];

            $data[] = [
                'time_label' => $time_label,
                'change_rate' => $change_rate,
            ];
        }
    }
    // 데이터베이스 연결 종료
    $conn->close();

    // 배열 순서 뒤집기
    $data = array_reverse($data);

    // JSON 형식으로 데이터 반환
    header('Content-Type: application/json');
    echo json_encode($data);
?>
