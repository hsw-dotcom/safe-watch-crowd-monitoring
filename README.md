# Safe Watch — Crowd Density Monitoring (2023 Capstone)

> **2023년 대학 캡스톤 프로젝트 기록 보관소.** 당시 Raspberry Pi 환경에서 구현·시연한 코드를 정리한 자료이며, 현재 전체 시스템의 실행을 보증하지 않습니다.

## 프로젝트
- 기간: 2023년 3월~6월 / 4인 팀
- 목표: 카메라 영상에서 사람 수를 탐지하고 밀집도·위험 단계를 저장·표시하는 모니터링 시제품
- 환경: Raspberry Pi 4, Camera Module 3, Raspberry Pi OS, Python, Picamera2, OpenCV, TensorFlow Lite, Nginx, PHP, AJAX, MariaDB
- 주요 화면: 실시간 MJPEG 카메라 영상, 사람 탐지 결과, 밀집도·위험 단계, 시계열 그래프, 위치 지도

## 시스템 흐름
```text
Pi Camera -> Picamera2 MJPEG server (:8000)
               |-> Browser live-stream view
               |-> Python frame capture -> TensorFlow Lite detection
                      -> density and risk calculation -> MariaDB
                            |-> PHP + AJAX + Chart.js dashboard
                            |-> alarm.py (WAV / Twilio attempt)
```

## 개인 담당 업무와 팀 분담
당시 개인 최종보고서의 업무 분담 기준입니다.

| 구분 | 담당 |
|---|---|
| 웹 서버·DB 조사 및 구축, PHP/AJAX 동적 웹페이지 | 본인 |
| MJPEG 스트리밍 연동, 경고음·SMS 기능 구현 | 본인 |
| AI 학습 데이터셋·모델 학습 및 모델 적용 | 다른 팀원 |
| 밀집도 계산식 설계 | 다른 팀원 |
| Raspberry Pi 하드웨어 구매·초기 연결 | 다른 팀원 |

**팀 프로젝트의 공동 결과물이며, 저장소에 있는 모든 코드를 개인이 독자 작성했다는 의미는 아닙니다.**

## 당시 시험 기록
카메라·인식 결과와 웹 상태 화면의 동시 표시, 로컬 네트워크 접속, VNC를 통한 Raspberry Pi 실행, 수동 DB 입력값의 웹 반영, 위험 모달 표시가 사진·영상으로 확인되었습니다. 인식 거리·마네킹 오인식 문제도 보고서에 기록되어 있습니다.

**확인되지 않은 부분:** 실제 현장의 위험 상황에서 SMS 전송 성공, 전체 기능의 현재 재실행, 정량 모델 정확도 및 안정적인 1초 처리.

## 공개본 보안 및 재실행 한계
원본에 있던 DB 비밀번호·Twilio 인증정보·수신번호는 환경변수 참조로 변경합니다. 사진·영상·원본 보고서·훈련 노트북은 개인정보, 초상권 및 API 키 문제 때문에 공개하지 않습니다.

원본 Raspberry Pi 장비, `people_detect.tflite` 및 라벨 파일, WAV 파일과 Flask `app.py`가 없는 상태라 재현 실행은 검증하지 않았습니다. 원본 코드의 하드웨어 의존 경로와 구현 한계는 문서에 따로 설명합니다.

## 파일 안내
- `src/python/`: Python 프로그램
- `src/web/`: HTML/PHP 대시보드
- `database/`: 원본 SQL의 변화율(백분율) 버전
- `docs/`: 아키텍처·문제해결·기술적 한계·보안 및 출처

## 출처와 재사용
TensorFlow Lite 객체 인식 예제와 Picamera2 MJPEG 스트리밍 예제를 기반으로 한 부분이 있습니다. 외부 예제 및 팀원 작성 부분의 권리 관계가 별도로 존재할 수 있으므로 프로젝트 전체에 일괄적인 오픈소스 라이선스를 부여하지 않습니다.

현재 저장소는 **안전사고 방지 제품이 아니라 2023년 시제품 구현 및 검증 기록**입니다.
