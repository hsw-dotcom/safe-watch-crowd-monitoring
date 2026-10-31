# Safe Watch | AI 기반 군중 밀집 감지 및 경고 시스템

**기간:** 2023.03 ~ 2023.06  
**유형:** 대학교 캡스톤디자인 · 4인 팀 프로젝트  
**주요 기술:** Python, Raspberry Pi, Linux, OpenCV, TensorFlow Lite, MariaDB, Nginx, PHP, HTML/CSS/JavaScript, AJAX, Twilio

## 프로젝트 소개

Raspberry Pi 카메라에서 인원을 검출하고, 위험 단계를 데이터베이스와 웹 화면에 표시하며, 위험 상황에 대응할 수 있도록 현장 경고음과 SMS 알림을 연동한 모니터링 시스템입니다.

![2023년 Safe Watch 웹 모니터링 화면](assets/2023_original_dashboard_capture.jpg)

## 주요 구현 기능

- **영상 수집 및 사람 검출:** Picamera2 기반 카메라 영상과 TensorFlow Lite 모델을 연동하고 검출 결과 이미지를 생성
- **위험 단계 구분:** 최종 발표 기준 인원 수 **0~2명 안전 / 3~4명 경고 / 5명 이상 위험**
- **DB 기록:** MariaDB에 밀집도 표시용 수치와 위험 단계를 저장
- **웹 모니터링:** Nginx·PHP·AJAX 기반으로 실시간 영상, 사람 인식 결과, 위험 상태, 밀집도·변화율 그래프 및 CCTV 위치 표시
- **현장 알림:** DB의 위험 단계에 따라 USB 스피커 경고음 및 Twilio 문자 발송 기능 연동

초기 밀집도 산출 방식을 검토한 뒤, 최종 시연에서는 **검출 인원 수를 기준으로 위험 단계를 판정**했습니다. 고정 면적 설정값은 표시용 밀집도 수치에 사용했습니다.

## 본인 담당 업무

- Raspberry Pi 환경에 사람 검출 기능을 적용하고 카메라·영상 처리 프로그램 연동
- MariaDB 데이터 저장 및 조회 흐름 구축
- Nginx 웹 환경 구성과 PHP·AJAX 기반 모니터링 페이지 구현
- 위험 상태 표시, 밀집도·변화율 그래프와 화면 자동 갱신 기능 개발
- 경고음 및 Twilio 문자 발송 기능 연동·시험

사람 검출 모델의 최초 학습은 팀 내 다른 구성원이 담당했습니다. 본인은 실제 Raspberry Pi 환경에서의 적용, 데이터·웹·알림 기능 연결과 검증에 참여했습니다.

## 구현 및 시험 결과

카메라 영상에서 인식한 결과를 데이터베이스와 웹 모니터링 화면에 연결했습니다. 실제 웹 대시보드 시연 자료를 확보했으며, **Twilio 위험 알림 문자의 휴대전화 수신**도 별도 시험에서 확인했습니다.

## 주요 파일

| 경로 | 역할 |
|---|---|
| [`src/python/main.py`](src/python/main.py) | 영상 프레임 처리, 인원 수 기반 단계 판정, DB 기록 |
| [`src/python/count_objects.py`](src/python/count_objects.py) | 사람 검출 및 결과 이미지 생성 |
| [`src/python/stream.py`](src/python/stream.py) | 카메라 MJPEG 스트리밍 |
| [`src/python/alarm.py`](src/python/alarm.py) | 위험 상태 조회 및 경고음·문자 발송 |
| [`src/web/`](src/web/) | 웹 대시보드, 상태 정보, 그래프 및 지도 |
| [`database/schema.sql`](database/schema.sql) | MariaDB 데이터 구조와 변화율 조회 |

## 코드 및 참고자료

공개된 코드는 당시 최종 발표·개발 자료를 바탕으로 **포트폴리오 열람용으로 정리한 구성**입니다. 실제 실행에는 Raspberry Pi, 학습된 모델, 음원, DB·웹서버 및 인증정보 설정이 필요합니다.

검출 코드에는 Evan Juras의 [TensorFlow Lite 객체 검출 예제](https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi)를 참고했고, 카메라 스트리밍에도 Picamera2 예제 구성을 참고했습니다. 프로젝트 결과물은 팀 공동 개발에 기반합니다.
