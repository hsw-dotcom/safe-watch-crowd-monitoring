# Safe Watch | AI 기반 압사 사고 예방 CCTV

2023년 1학기 4인 팀 캡스톤디자인 프로젝트. Raspberry Pi 카메라로 사람 수를 감지하고, 위험 수준을 데이터베이스·웹페이지에 표시하며 위험 시 현장 경고음과 SMS를 호출하는 시스템입니다.

![2023년 Safe Watch 웹 모니터링 화면](assets/2023_original_dashboard_capture.jpg)

## 핵심 기능

- **사람 인식:** Raspberry Pi 4 + Camera Module v3, Picamera2 MJPEG 스트리밍, TensorFlow Lite 사람 검출
- **위험 판정:** 검출 인원 **0~2명 안전 / 3~4명 경고 / 5명 이상 위험**
- **데이터 기록:** MariaDB에 위험 단계와 화면 표시용 수치 저장. 설정된 분석 후 대기시간 **10초**
- **웹 모니터링:** Nginx·PHP·HTML·AJAX로 영상·검출 결과·현재 상태 확인, 밀집도 및 백분율 변화 그래프, CCTV 위치 지도
- **경고:** `alarm.py`가 DB의 위험 상태를 조회해 Twilio SMS 및 USB 스피커의 WAV 경고를 실행

**구현 범위:** 초기에는 장애물과 현장 면적을 산출하여 밀집도를 구하려 했으나 **자동 면적 산출·장애물 면적 차감은 구현하지 못했습니다.** 최종 위험 판정은 **인원 수 기준**으로 변경했습니다. 기존 설정 `total_area=300`은 기록·그래프에 쓰는 고정값일 뿐, 실제 공간 면적을 측정한 결과가 아닙니다.

## 코드 구조

```text
src/
  python/
    main.py             프레임 추출, 사람 수·위험 단계 판정, DB 기록
    count_objects.py    TFLite 사람 검출 및 after.jpg 저장
    stream.py           Picamera2 MJPEG 영상 서버
    alarm.py            DB 위험 조회, SMS·스피커 알림
    configs.ini         설정값 (delay=10, total_area=300)
  web/
    index.html          메인 대시보드
    image.php           인식 화면 이미지 2초 주기 갱신
    maininfo.html       위험 상태·밀집도 표시 및 경고 모달
    maininfo.php        DB 상태 조회
    graph.html          그래프 페이지
    density.html        밀집도 그래프
    densityinfo.php     밀집도 데이터 조회
    change.html         변화율 그래프
    changeinfo.php      변화율 데이터 조회
    map.html            CCTV 위치 지도
database/
  schema.sql            카메라·측정 기록 테이블, 변화율 VIEW
assets/
  2023_original_dashboard_capture.jpg
```

## 사용 기술

**Python**, OpenCV, TensorFlow Lite, Picamera2, Raspberry Pi, **MariaDB**, **Nginx**, PHP, HTML/CSS/JavaScript, AJAX, Chart.js, Google Maps, **Twilio**.

## 구현·검증 범위 및 출처

- 이 저장소는 **2023년 최종보고서·최종 발표·보관 코드·프로젝트 담당자의 확인**을 기준으로 2026년에 정리한 **공개용 코드**입니다. 2023년 최종 실행 파일을 바이트 단위로 그대로 복원한 것은 아닙니다.
- 보고서에 본문이 빠져 있는 `count_objects.py`는 별도 보관 소스에서 확보한 인식 코드입니다. 해당 코드는 Evan Juras의 [TensorFlow Lite 객체 검출 예제](https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi)를 바탕으로 작성되었으며, `stream.py`도 Picamera2 MJPEG 예제를 참고합니다. **4인 팀 공동 개발 결과물**입니다.
- 구체적인 2026년 정리 내용: 미사용 면적 산출 함수·브라우저 SMS 시험 경로·위험 상태 시험용 SQL 입력을 제거했습니다. 보고서에 보존된 일부 이전 판정 코드 대신 **최종 발표에서 확인된 인원 수 기준**을 적용했습니다.
- TFLite 모델·라벨, 경고 WAV, 당시 계정 정보와 인물 사진·영상은 공개하지 않습니다. 실행하려면 별도 모델·장치·DB/웹서버 설정 및 개인 인증정보가 필요합니다. `schema.sql` 사용 시 카메라 기본 행을 먼저 등록해야 하고, 밀집도 변화율 계산은 이전 값이 0인 경우를 별도로 처리하지 않습니다.
- 당시 야외 시험에서는 경고·위험 수준에 도달하지 못하여 **실제 위험 상황에서 탐지부터 문자 수신까지 자동으로 동작했다는 종단 간 검증은 없었습니다.** Twilio 메시지 수신 자체는 별도의 시험 자료에서 확인했습니다. 현재 환경에서 하드웨어 통합 재실행을 검증하지 않았습니다.
- 알림 코드는 위험 DB 값을 반복 조회하므로 실제 Twilio 계정을 연결할 때는 **반복 문자 발송 및 비용 발생**에 주의해야 합니다. 외부 라이브러리와 예제 코드의 라이선스는 각 원저작자에 따릅니다.
