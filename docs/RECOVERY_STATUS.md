# Safe Watch — 현행 구현 파일, 원본과의 차이, 실행 검증 범위

> 작성·갱신: 2026-10-31. **최종 구현의 완전한 2023년 소스 복사본이 아니라, 보존 소스 + 2023 보고서 및 직접 확인 결과에 근거한 최소 수정본**.

## 현행 파일 상태

- Python 5개(`main.py`, `configs.ini`, `count_objects.py`, `stream.py`, `alarm.py`), 웹 HTML/PHP 10개, SQL 1개: 총 **코드·설정 16개**.
- `main.py`는 2026년에 **인원 수 직접 단계 판정** 및 **개인 보고서의 장애물면적 인자 구조(실제 0)**를 반영한 수정본. 원래 보고서와 코드 줄 전체가 같지 않음.
- `configs.ini`는 보고서의 **10초**로 갱신. 이전 보관본은 15초. 다른 소스 14개는 기존 SHA 그대로.
- 백분율 변화율 SQL은 앞서 확인한 최종 사용 방식에 맞춰 유지. 보고서에 수록된 절대차 SQL과는 다름.
- 문서·출처 목록은 2026년 작성. Git 원본과 동일한 바이트라는 보장을 부여하지 않음.

## 확인된 주요 동작

Raspberry Pi/Camera Module v3 → Picamera2 MJPEG → JPG 캡처 → TFLite 사람 수 검출 → **인원 수 직접 위험 단계** → MariaDB → Nginx/PHP/Chart.js/Google 지도 → Python `alarm.py`의 10초 위험 상태 조회/Twilio SMS/WAV 경고 경로. JPG는 직접 덮어쓰기, 웹은 2초마다 새 JPG 요청.

**실측 면적 산출, 장애물 면적 차감, 장애물 모델 최종 탑재, IoU 중복 보정은 구현했다고 주장하지 않음.** `total_area=300`은 이전 설계에서 사용한 설정값이고 화면/DB의 수치는 실측 면적 기반 군중 밀도와 다름.

## 현재 실행하기 전에 필요한 외부 조건

- `models/people_detect.tflite`, `models/people_label.txt`, `warning.wav` 원본은 별도 비공개 백업에서 확인. 공개 Git에서는 제외.
- Raspberry Pi 하드웨어, Picamera2, TFLite, MySQL 드라이버 및 MariaDB 서버, PHP/Nginx 환경과 실행 경로가 필요.
- 비밀정보는 환경변수로 읽도록 기존 공개용 코드에서 치환된 상태. 개별 설정값 및 실사용 자격 증명은 포함하지 않음.
- 현재 SQL 파일 맨 위의 `sudo mysql -u root -p`는 SQL 실행문이 아니라 셸 명령. DB 생성·선행 `cameras` 행 등은 외부 준비가 필요.
- `maininfo.html`에는 2023 개발 중 실험한 브라우저 `/send_sms` 경로가 남아 있으나, 실제 최종 문자 발송 경로는 `alarm.py`로 확인됨. Flask `app.py` 원본 및 브라우저 경로의 성공 기록은 미확보.
- 원본 `density` VIEW는 이전 0 값에 대한 명시적인 분모 처리 없음. 새 설계의 안전 보강을 원본 기능이라고 설명하지 않음.

## 실제 검증의 한계

- 개인 최종보고서 31–33쪽: 높은 위험 단계의 야외 종단 간 시험 성공 기록 없음, 원거리 인식률 저하 및 마네킹 오인식 문제 명시.
- 별도 휴대전화 사진: Twilio 위험 문자의 실제 수신은 확인되나 자동 카메라 위험 감지의 결과인지 미확인.
- 코드를 갱신한 현재 환경에서 Raspberry Pi·카메라·SMS·DB를 직접 재실행하지 않았음. 코드 구문과 위험 분기만 검증할 수 있음.

## 변경 이력 참조

- [코드 SHA 및 2023 원본/2026 수정 경계](ORIGINAL_SOURCE_MANIFEST.md)
- [최종 발표와 제출 보고서의 충돌](PRESENTATION_VS_SOURCE.md)
- [프로젝트 대화 확인 내용](2023_CONVERSATIONS_AND_REPORT_AUDIT.md)
- [SMS 자산 확인](ARTIFACT_AND_SMS_EVIDENCE.md)

이전 보관 버전은 Git 커밋 및 별도 archive 브랜치에서 추적 가능합니다. **최종 사용 코드 원문을 확인했다고 오인할 수 있는 표현은 피해야 합니다**.
