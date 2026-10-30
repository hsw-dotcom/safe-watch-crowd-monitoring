# 구현 및 검증 기록

2023년 4인 캡스톤 프로젝트 원본 분석 기록입니다. GitHub에 공개된 파일은 역사적 코드의 보안 정리본이며 Raspberry Pi가 없어 현재 전체 동작을 검증하지 못했습니다.

## 흐름
Pi Camera Module 3 → Picamera2 MJPEG stream (port 8000) → OpenCV frame capture → TFLite people detection → people / total_area → MariaDB receive_data → Nginx/PHP/AJAX dashboard and charts. 별도 alarm.py가 DB 최신 위험 상태를 조회하고 WAV/Twilio 경고를 시도하는 구조입니다.

## 보존된 버전 차이
- ZIP configs.ini: delay=15. 개인 최종보고서에 실린 코드는 delay=10. 코드에서는 추론시간 이후 delay 전체를 sleep하여 1초 처리라고 말할 수 없습니다.
- Python 위험 임계값: 2 이하 안전, 2 초과 4 미만 경고, 4 이상 위험. PPT의 척도는 이 값과 다릅니다.
- ZIP의 실제 계산은 탐지 인원 수 / 고정 총면적이며 장애물 면적 보정은 최종 실행 경로에서 미사용입니다.
- 제출 sql.txt는 직전 밀집도 대비 백분율 VIEW입니다. 개인 보고서의 최종 SQL은 밀집도 차이를 사용한다고 기록합니다. 어느 것이 실제 운영 DB에 적용됐는지는 미확인입니다.

## 알려진 결함 및 한계
- SQL의 previous.id + 1 조건은 카메라별 이전 값을 안정적으로 찾지 못합니다. 이전 밀집도가 0인 경우도 명시적 처리하지 않습니다.
- 웹 PHP 최신조회는 camera_number 필터가 없으므로 다중 카메라 확장에 취약합니다.
- 기본 FK 카메라 1번을 등록하는 초기화 SQL이 없습니다.
- Raspberry Pi 경로와 일부 브라우저 주소는 배포환경에 고정되어 있습니다.
- Flask app.py, TFLite 모델/라벨, 경고음 파일과 Nginx 서비스 세부 설정은 보유하지 않습니다.
- 필드 테스트는 위험 단계에 도달하지 못해 실제 위기에서 SMS 및 스피커가 연동됐다는 검증이 없습니다.

## 확인된 실제 결과
당시 VNC/DB 접속, 웹페이지, 객체 감지 결과 표시, 수동 INSERT 데이터의 웹 그래프/위험 표시, 경고 모달은 사진·영상으로 확인했습니다. 인식 성능의 정량 정확도나 상시 운용 성능은 측정하지 않았습니다.
