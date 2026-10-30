# Safe Watch — 2023 캡스톤디자인 최종 동작 기준 코드

> **현재 `main`은 2023년 보고서·최종 발표·당사자 확인을 대조해 2026년에 정리한 공개용 버전입니다.** 2023년 장비에서 추출한 **최종 실행 파일의 바이트 동일 복제본은 아닙니다.** 일부 코드는 2023년 소스를 보존했고, `main.py`의 최종 위험 단계와 `configs.ini`는 확인된 동작에 맞춰 최소 수정했습니다. 인증정보는 공개하지 않습니다.

## 최종 구현 기준

| 항목 | 확인된 실제 방식 | 근거 |
| --- | --- | --- |
| 사람 감지 | TensorFlow Lite 모델을 Raspberry Pi에서 추론; 모델 추출·변환 후 수정하지 않음 | 2023 보고서, 기존 소스, 당사자 확인 |
| 위험 단계 | **인원 0~2명 안전 / 3~4명 경고 / 5명 이상 위험** | 최종 발표 및 당사자 확인. **이 최종판의 원문 `main.py`는 미확보** |
| 면적 | 면적 산출·장애물 면적 차감은 **미구현**. 보고서의 `total_area=300` 고정값만 유지 | 2023 보고서와 당사자 정정 |
| 기록용 수치 | 고정 설정값 300을 이용한 `people_num / 300` 수치 저장 | 보고서의 이전 계산식과 보관 코드. **실측 면적 기반 물리적 밀집도 아님** |
| 분석·DB 저장 대기 | `delay=10`초 설정. 실행 후 대기하므로 실제 루프 주기는 처리 시간만큼 늘어날 수 있음 | 보고서 `configs.ini` 및 당사자 확인 |
| 변화 그래프 | 이전 DB 수치 대비 **백분율 변화율(%)** | 당사자 확인과 공개용 보관 SQL. 보고서에는 절대차 SQL도 수록 |
| SMS / 경고음 | `alarm.py`가 위험 DB 값 확인 후 Twilio 문자 및 WAV 경고음 호출 | 당사자 확인과 보고서, 기존 소스 |
| 영상·이미지 | Picamera2 MJPEG 포트 8000, `before.jpg`/`after.jpg` 직접 덮어쓰기, 웹 2초 갱신 | 보고서·소스·과거 대화 |

**구현하지 않은 기능:** 현장 면적 자동 측정, 장애물 탐지에 따른 유효 면적 차감, IoU 중복 박스 보정. 17종 장애물 모델은 연구·학습했지만 최종 Raspberry Pi 실행에서는 제외했습니다.

## 파일 구조

```text
src/python/
    main.py          인식 이미지 추출 → 사람 수 판단 → 수치·위험 단계 DB 기록
    configs.ini      delay=10, total_area=300
    count_objects.py TFLite 사람 탐지 / after.jpg 덮어쓰기
    stream.py        Picamera2 MJPEG 영상
    alarm.py         위험 단계 10초 조회 및 SMS/WAV
src/web/
    index.html, image.php, maininfo.html, maininfo.php
    density.html, densityinfo.php, change.html, changeinfo.php
    graph.html, map.html
database/
    schema_legacy_percent.sql
docs/
    ORIGINAL_SOURCE_MANIFEST.md   파일별 SHA와 보존/변경 분류
    PRESENTATION_VS_SOURCE.md     발표·보고서·실제 최종 동작 차이
    2023_CONVERSATIONS_AND_REPORT_AUDIT.md  개발·대화 이력
    RECOVERY_STATUS.md           실행 한계, 누락 및 출처
```

## 코드 원본과 2026년 보정의 경계

- **`src/python/main.py`**: 개인 최종보고서(7–9쪽)의 `get_alert_level(total_area, people_num, obstacle_area)` 형태를 참고하고 실제 호출에서 `obstacle_area=0` 사용. 위험 단계만 **실제 최종 구현에 대한 사용자 확인대로 사람 수로 판정하도록 2026년에 보정**. 고정값 기반 수치 계산은 웹·DB 연속성 설명용으로 유지. **2023년 최종 원문을 그대로 복구했다고 주장하지 않음**.
- **`src/python/configs.ini`**: 개인 최종보고서와 확인 결과에 따라 `delay=10`으로 변경. 이전 보관본의 `delay=15`는 Git 이력에 보존.
- **나머지 보관 소스 14개**: 기존 공개용 SHA 보존. 일부 DB/Twilio 시크릿은 이전 공개 준비 과정에서 환경변수로 치환됨.
- **SQL**: 사용자께서 최종 사용했다고 확인한 **백분율 SQL**을 유지. 보고서 29쪽의 **절대차 계산 SQL**은 변경되지 않은 다른 버전의 참고 근거로 문서화하며 현재 DB 스키마로 추가하지 않음.

원본/정리본을 함께 보지 않아도 판단할 수 있도록 [파일별 근거와 SHA](docs/ORIGINAL_SOURCE_MANIFEST.md)를 기록했습니다.

## 실행 검증 한계

2023년 개인 최종보고서 31–33쪽에는 야외 시험에서 경고·위험 단계까지 도달하지 못해, 실제 위험 상황에 대한 **카메라 감지 → 문자 자동 전송 전체 경로는 검증하지 못했다**고 기록되어 있습니다. 수신 사진으로 Twilio 문자가 도착한 사실은 별도 확인됐습니다. 인식률은 10m 이상에서 낮아지고 옷 입은 마네킹을 사람으로 오인한 시험 기록도 있습니다.

공개 저장소에 TFLite 모델·라벨·WAV·비밀번호·개인정보를 포함하지 않았고, 지금의 Raspberry Pi 구동·DB 접속·경고음 재생·SMS 수신을 실장 검증한 것은 아닙니다. `src/web/maininfo.html`에 남은 `/send_sms` 브라우저 시도 코드는 실제 최종 발송 주체가 아니며, 최종 발송은 `alarm.py`였다고 확인했습니다.

## 자료와 출처

- [발표 / 보고서 / 최종 동작 비교](docs/PRESENTATION_VS_SOURCE.md)
- [대화·보고서 교차 대조](docs/2023_CONVERSATIONS_AND_REPORT_AUDIT.md)
- [보안 처리·자료 확보 상태](docs/RECOVERY_STATUS.md)
- [SMS 실물 증거](docs/ARTIFACT_AND_SMS_EVIDENCE.md)
- [카메라 오류 로그](docs/CAMERA_ACQUIRE_ERROR.md)
- [팀 분담 및 예제 출처](docs/attribution.md)

![2023 Safe Watch 웹 화면(내부망 주소 제외)](assets/2023_original_dashboard_capture.jpg)
