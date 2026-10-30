# Safe Watch — 2023 보관 원본 소스

**이 저장소의 `main`에는 확인된 2023년 프로젝트 원본으로 분류된 코드만 남겼습니다.** 기존에 AI가 재구성한 Python/PHP/SQL, 테스트, 데모 코드는 `main`에서 제외했습니다. 2026년 작성한 README·근거 문서는 설명용이며 원본 소스라고 주장하지 않습니다.

## 근거와 우선순위

1. **최종 발표자료**: 실제로 구현했다고 발표한 기능과 단계 구분의 기준.
2. **2023 보관 소스 16개**: 당시 작성·수집된 코드의 실제 문장·파일 배치. `main`에서는 기존 Git 객체(SHA)를 수정하지 않고 그대로 옮김.
3. **프로젝트 대화 및 사용자 확인**: 모델은 변환 이후 재학습·개조하지 않았고, 면적은 실시간 산출이 아닌 고정 설정값이며, 결과 이미지 파일은 덮어썼다는 사실.
4. **2026년 재구성 코드**: 원본이 확인되지 않는 기능을 추정해 작성한 별도 자료. 현재 `main`에는 포함하지 않음.

발표자료와 원본 코드가 일치하지 않는 경우 **원본 코드를 임의로 고쳐 ‘원본’이라고 부르지 않고, 불일치를 명시**합니다. 예: 최종 발표의 위험 단계는 안전 1~2명, 경고 3~4명, 위험 5명 이상이지만, 보관 `main.py`는 `인원 수 ÷ 고정 면적`으로 단계 판정합니다.

## 실제 원본 코드 배치

```text
src/
  python/
    main.py             # 영상 프레임 획득, 사람 수/밀집도, DB 저장
    count_objects.py    # TFLite 추론, after.jpg 덮어쓰기
    stream.py           # Picamera2 MJPEG
    alarm.py            # 위험 단계 조회, 10초 단위 경고음/Twilio
    configs.ini         # delay=15, total_area=300
  web/
    index.html          # 메인 페이지
    image.php           # 내부 내용은 HTML, after.jpg 2초마다 갱신
    maininfo.html
    maininfo.php
    density.html
    densityinfo.php
    change.html
    changeinfo.php
    graph.html
    map.html
database/
  schema_legacy_percent.sql
docs/
  ORIGINAL_SOURCE_MANIFEST.md  # 각 파일의 2023 보관본 Git blob SHA
  PRESENTATION_VS_SOURCE.md    # 최종 발표와 실제 코드의 충돌·범위
  RECOVERY_STATUS.md           # 결손·제외 사항과 보존 브랜치
  attribution.md               # 팀 및 공개 예제 저작자 표기
```

**원본 16개 코드·설정 파일을 동일한 Git blob SHA로 보존**했으며 Python/PHP/SQL 기능을 재작성하지 않았습니다. 여러 웹 페이지는 당시 원본의 분리된 구성으로, 기능을 임의 통합하지 않았습니다.

## 복구 수준: 코드 구조는 있지만 완전한 실행 패키지는 아님

코드로 확인 가능한 단계: Pi MJPEG → 이미지 캡처 → TFLite 사람 검출 → 고정 면적 기반 밀집도 → MariaDB → Nginx/PHP/AJAX 웹·차트·지도 → DB 조회 기반 경고음/SMS.

**별도로 필요한 원본 자산**: `people_detect.tflite`, `people_label.txt`, `warning.wav`, 2023년 실행 환경·설정과 비밀키. Flask `/send_sms` 호출을 담당할 당시 `app.py` 원본도 확보되지 않았습니다(독립적인 `alarm.py` Twilio 호출은 확인됨). 원본 SQL에는 실행 전 준비가 필요한 내용이 있습니다. 자세한 사항은 [복구 상태](docs/RECOVERY_STATUS.md) 참고.

현재 목적은 **하드웨어 없이 당시 소스를 보존하고 설명하는 것**이므로 하드웨어 구동, 실측 정확도 또는 실제 서비스 완전 동작을 주장하지 않습니다.

## 원본과 재구성본의 분리

- 현행 **원본 중심 `main`**: [저장소 루트](https://github.com/hsw-dotcom/safe-watch-crowd-monitoring)
- **정리 이전의 원본 + 재구성본**: [archive/pre-dedup-20261031](https://github.com/hsw-dotcom/safe-watch-crowd-monitoring/tree/archive/pre-dedup-20261031)
- **최종 발표 우선으로 수정했던 복원본**: [archive/reconstruction-before-original-only-20261031](https://github.com/hsw-dotcom/safe-watch-crowd-monitoring/tree/archive/reconstruction-before-original-only-20261031)

이전 실험적 재구성 코드는 보존 브랜치에서만 확인 가능하며, `main`에 혼입하지 않습니다.

> 출처 제한: 구형 제출 ZIP 파일의 내부 전체를 직접 대조하지 못했으므로, 이 16개가 2023년 최종 실행 파일 전부라고 단정할 수 없습니다. 원본이라는 말은 **확인된 보관 소스와 바이트 단위 Git 객체가 동일하다**는 의미입니다.
