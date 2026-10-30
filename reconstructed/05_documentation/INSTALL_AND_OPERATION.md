# Safe Watch — 설치 및 운영 참고서

> **현장 재가동 검증을 대신하는 문서는 아닙니다.** 당시 Raspberry Pi OS/카메라/모델 정보를 기준으로 환경별 조정이 필요합니다.

## 1. 폴더 배치
- `01_raspberry_pi_project/*` → `/home/pi/project/`
- `02_nginx_webroot/*` → `/var/www/html/`
- `03_database/schema.sql`은 **신규 DB**에서 수동 확인 후 MariaDB에 적용합니다.
- `04_configuration/*`은 서버 설정 예시이며, 실제 서비스 설정과 비밀번호를 직접 구성합니다.
- 모델 `people_detect.tflite`, `people_label.txt`를 `/home/pi/project/models/`에 확보해야 실제 TFLite 탐지 가능.
- 경고음 `warning.wav`는 두 위치 `/home/pi/project/` (aplay), `/var/www/html/` (브라우저)에서 각각 필요할 수 있습니다. 이 ZIP에는 포함되지 않습니다.

## 2. 구성 순서
1. Raspberry Pi OS와 Camera Module(Picamera2)을 정상적으로 구동되는지 확인하고 `libcamera`·Picamera2를 OS 패키지로 설치합니다.
2. Python 패키지 `numpy`, `opencv`, MariaDB 드라이버, Twilio를 Pi의 Python 환경에 맞춰 설치합니다. `tflite_runtime`은 Raspberry Pi OS/Python ABI와 호환되는 wheel을 별도 확인해야 합니다.
3. MariaDB에 `schema.sql`을 적용하되, **기존 2023 DB에는 그대로 재적용하지 마십시오.** 기존 DB라면 백업 후 `migration_from_legacy.sql` 검토가 필요합니다.
4. MariaDB에 필요한 최소 권한의 사용자(`SELECT`,`INSERT`)를 생성하고 Python 및 PHP-FPM의 환경변수에 계정정보를 전달합니다. `.env.example` 파일은 자동 적용되지 않습니다.
5. Nginx와 PHP-FPM을 구성합니다. 버전에 따라 PHP-FPM 소켓/환경변수(`clear_env`)가 달라질 수 있습니다. 실제 경로는 배포 환경에 맞춰 변경합니다.
6. `/var/www/html/tensorflow/` 폴더 쓰기 권한(추론 프로세스)과 Nginx 읽기 권한을 확인합니다.
7. `02_nginx_webroot/index.html`의 `RPI_IP_ADDRESS`를 실제 Pi IP로 교체합니다. 원본에서 `wlan0` IP를 사용했지만 재구성본에서는 같은 장치의 로컬 MJPEG 주소를 설정으로 지정합니다.

## 3. 실행
```bash
cd /home/pi/project
python3 stream.py                       # 터미널 1, 포트 8000 MJPEG
python3 main.py                         # 터미널 2, 모델 추론 + DB 저장
python3 alarm.py                        # 터미널 3, DB 경고 조회
```
테스트 목적으로 카메라/모델/DB 없이 계산 결과만 확인하려면 `python3 main.py --dry-run`을 사용합니다. (무한 반복이므로 Ctrl+C 종료)

## 4. 웹/네트워크
- 브라우저: `http://<라즈베리파이의 사설 IP>/` (Nginx :80), MJPEG :8000.
- ipTIME 관리자 페이지에서 내부 IP를 대표 호스트로 설정한 과거 DMZ 테스트는 가능했으나, 인터넷 전체에 PHP/HTTP/MJPEG를 노출하면 접근제어/HTTPS/방화벽/계정 관리 문제가 있습니다. 외부 공개보다 내부망 테스트 또는 VPN 사용을 권장합니다.
- 웹 템플릿이 `http://` URL을 iframe으로 직접 표시하므로 HTTPS로 배포하면 mixed content 차단이 발생할 수 있습니다.

## 5. 위험/경고
- 원본의 `people_count / total_area`를 그대로 사용합니다. **안전≤2, 경고<4, 위험≥4는 물리적으로 검증된 보편적 안전 기준이 아닙니다.** `total_area=300`이라면 인식 인원이 600명에 도달할 때까지 안전으로 판정될 수 있어, 실제 사고 예방 목적으로 사용해서는 안 됩니다.
- `SAFEWATCH_ENABLE_SMS=0` 기본값. 본인 테스트 환경에서 합법적·사전동의된 수신자만 설정하고, 번호/계정/비용/재시도 정책을 확인한 후에만 활성화하세요.
- 브라우저 경고음은 직접 **경고음 켜기**를 눌러야 동작하도록 설계했습니다. 실제 Pi 스피커는 `alarm.py`를 사용합니다.
- `app.py`의 `/send_sms`는 역사적 코드가 아니라, 대화에 등장한 경로를 재구성한 **수동 로컬 전용 선택 기능**입니다. 웹 메인 페이지는 이를 호출하지 않습니다.

## 6. 추가 확인이 필요한 자료
`TFLite 모델 및 라벨`, `warning.wav`, `app.py` 원본, 당시 Nginx/PHP-FPM 실제 설정, 실사용 `sql` 최종판, 원본 ZIP 내부 파일, 외부 접속 구성과 보안 설정.
