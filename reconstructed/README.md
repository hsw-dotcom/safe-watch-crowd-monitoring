# Safe Watch 2023 · 4학년 1학기 캡스톤 · 코드 재구성 최종안

**분류: 대화·확인 원본에 근거한 복원/보완본(재작성). 2023년 당시의 1:1 원본 소스 아님.**

## 프로젝트 개요
Raspberry Pi 4 + Camera Module 3 → Picamera2 MJPEG(8000) → 프레임 저장 → TFLite 사람 감지 → 밀집도/3단계 위험 평가 → MariaDB → Nginx PHP JSON → HTML/AJAX/Chart.js 대시보드/지도. `alarm.py`는 DB 위험 상태를 읽어 WAV 스피커와 Twilio SMS를 선택적으로 호출합니다.

2023년 대화에서 요청한 `/tensorflow/after.jpg`의 2초 주기 새로고침, 캐시 무효화 `?t=...`, 외부 IP로 웹페이지 접근, HTML/PHP/AJAX 연계, 웹 그래프, 위험 경고 동선에 대응합니다.

## 폴더 배치
```text
SafeWatch_2023_Final_Reconstructed/
├── 01_raspberry_pi_project/       → /home/pi/project/
│   ├── main.py                    카메라 프레임 수집 → 분석 → DB 기록
│   ├── stream.py                  Picamera2 → MJPEG HTTP :8000
│   ├── count_objects.py           TFLite 추론 → after.jpg
│   ├── alarm.py                   DB 모니터링 → 선택적 WAV / SMS
│   ├── app.py                     선택적 localhost Flask 재구성(미사용 기본 경로)
│   ├── db.py, risk.py, settings.py
│   ├── configs.ini, requirements-pip.txt
│   ├── image/                     실행 시 before.jpg 생성
│   └── models/                    사용자 모델/라벨 별도 필요
├── 02_nginx_webroot/              → /var/www/html/
│   ├── index.html, maininfo.html, image.php, graph.html, map.html
│   ├── maininfo.php, densityinfo.php, changeinfo.php, db_connect.php
│   ├── density.html, change.html, assets/
│   └── tensorflow/               실행 시 after.jpg 생성
├── 03_database/                   MariaDB 신규 스키마/이전 SQL 및 차이
├── 04_configuration/              환경변수, Nginx/systemd 예시(실제 원본 아님)
├── 05_documentation/              설치, 근거, 차이점, 검증 범위
├── 06_tests/                      단위 및 구조 검사
└── 07_original_reference/         변경하지 않은 기존 GitHub 원본 링크
```

## 시작하기
자세한 실행법: `05_documentation/INSTALL_AND_OPERATION.md`
변경 근거: `05_documentation/COMPARISON_AND_PROVENANCE.md`
로컬 검증: `FINAL_CHECKS.txt`

1. 먼저 Pi에서 실제 원본 TFLite 모델과 `people_label.txt` 확보 및 라이브러리 설치가 필요합니다.
2. 신규 MariaDB에서는 `03_database/schema.sql`을 검토해 적용하십시오. **기존 DB는 별도 마이그레이션 확인이 필요합니다.**
3. Python 실행 환경과 PHP-FPM **양쪽**에 DB 환경변수를 제공합니다.
4. `/var/www/html/tensorflow/` 쓰기 권한과 `RPI_IP_ADDRESS` 값을 확인합니다.
5. 개별 터미널에서 `stream.py`, `main.py`, `alarm.py`를 실행합니다.

## 중요한 경계
- 모델/라벨, 원본 WAV, 계정정보, Flask 원본, 기존 모든 ZIP 내부 자료는 이 ZIP에 포함된 것으로 주장하지 않습니다.
- 실제 하드웨어·모델·데이터베이스·외부 네트워크·문자 발송 전체 연동 성공은 **미검증**입니다.
- 안전 임계값은 당시 소스에 기록된 예시이며 실제 인명 안전 판단용으로 검증되지 않았습니다.
- 오리지널 소스는 연결된 GitHub 저장소 `main`에서 그대로 확인할 수 있습니다. 개선본과 원본을 혼동하지 마십시오.
