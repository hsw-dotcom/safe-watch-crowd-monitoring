# 보관 소스 상태·별도 확보 자료·보존 브랜치 (2026년 작성)

## A. 유지한 것: 기존 공개용 Git 보관본과 blob SHA가 일치하는 2023 기반 소스

- Python 5개: `main.py`, `count_objects.py`, `stream.py`, `alarm.py`, `configs.ini`.
- HTML/PHP 10개: `index.html`, `image.php`, `maininfo.html`, `maininfo.php`, `graph.html`, `density.html`, `densityinfo.php`, `change.html`, `changeinfo.php`, `map.html`.
- SQL 1개: `schema_legacy_percent.sql`.

2026년 신규 실행 로직은 main에서 제외했습니다. 루트 README 및 docs는 **설명용 비실행 문서**입니다. 공개 준비 당시 암호·전화번호 등 인증정보를 치환한 소스이므로 비공개 2023 ZIP과 완전 동일하다는 뜻은 아닙니다.

## B. 원본만으로 가능한 것과 불가능한 것

**가능**: 프로젝트의 주요 함수·파일 구조, 영상 → 사람 검출 → 위험 결과 저장 → 웹 조회 → 경고 요청 흐름을 확인하고 분석할 수 있음. 원본 PHP/HTML 웹 화면과 그래프 구성 확인 가능.

**별도 확인된 사실**: 사적 백업에서 모델·라벨·경고음 파일을 확보했고, 휴대전화 사진에서 Twilio 위험 문자 **실제 수신**이 확인됩니다. [상세 증거](ARTIFACT_AND_SMS_EVIDENCE.md).

**불가능하거나 미확인**: 현재 공개 저장소에 모델·라벨·음원은 없고, 실물 장치·이전 실행환경도 없어 현재 재현할 수 없음. 모델 정확도 및 **실제 카메라 위험 감지 → SMS 자동 발송** 전 과정은 확인되지 않음.

## C. 보관 원본에서 확인된 불완전 지점

1. `count_objects.py`는 `models/people_detect.tflite`와 `models/people_label.txt`를 외부 파일로 요구. 파일 본체는 현재 `main`에 없음.
2. `alarm.py`는 `warning.wav` 및 Twilio 환경변수와 장치가 있어야 경고를 실행. WAV 원본은 **비공개 백업에서 확보**했으나 이 공개 저장소에는 포함하지 않음.
3. `maininfo.html`은 `http://127.0.0.1:5000/send_sms`에 브라우저에서 요청하지만 당시 Flask `app.py` 보관본은 없음. 이는 브라우저가 실행되는 PC/폰의 localhost를 가리킬 수 있으므로 분리된 `alarm.py`의 SMS 기능과 혼동하면 안 됨.
4. SQL 파일 첫 줄 `sudo mysql -u root -p`는 SQL이 아닌 셸 명령. DB 선택/생성과 `cameras` 기본 행의 사전 준비가 누락되어 빈 DB에 그대로 복사 실행할 경우 오류가 발생할 수 있음.
5. SQL VIEW는 이전 밀집도 0에서 나눗셈 예외에 대한 명시적 방어가 없음. 이를 뒤늦게 추가하지 않고 원본 상태로 둠.
6. 최종 발표와 `main.py`의 위험 단계 판정 불일치. [비교 문서](PRESENTATION_VS_SOURCE.md) 참고.
7. 미완성 장애물 면적 처리·IoU 예정 사항은 기능 완료로 간주하지 않음.

## D. 2026년 재작성·보완 코드는 현재 main에서 제거

다음 항목은 **보관 원본이 아니어서** 삭제했습니다: `src/python/{db.py,risk.py,settings.py}`, 새 PHP `api.php`, 그래프/대시보드 JS·CSS 통합본, 합성 demo JSON 및 --dry-run, 새로운 schema.sql, 새 테스트, 경고 cooldown, 새 모델 캐싱, 원자적 이미지 저장, 자동 실행/서버 설정 예시. 원본에 있는 동일 역할 파일만 유지했습니다.

복구 가능한 보관 위치:
- 원본과 초기 재작성 혼재: [archive/pre-dedup-20261031](https://github.com/hsw-dotcom/safe-watch-crowd-monitoring/tree/archive/pre-dedup-20261031)
- 최종 발표에 맞추려 수정했던 **후대 재구성본**: [archive/reconstruction-before-original-only-20261031](https://github.com/hsw-dotcom/safe-watch-crowd-monitoring/tree/archive/reconstruction-before-original-only-20261031)

추가 제출된 `backup.zip`에서는 모델·라벨·경고 WAV 존재를 확인했습니다. 다만 당시 실제 최종 배포본 전체를 빠짐없이 복원했다는 뜻은 아닙니다. Git blob의 일치는 기존 **공개용 보안 처리 사본** 기준입니다.

## E. 대화·2023년 개인 최종보고서 교차 확인

추가 대조 결과, 2023년 개인 최종보고서에는 **원본 소스와 다른 시점/버전의 코드**가 들어 있습니다. 구체적으로 `delay=10`(보관본 15), `get_alert_level(..., obstacle_area)`(호출할 때 0 전달), `density` SQL의 절대 차이 방식(보관본은 이전값 대비 %)을 확인했습니다. 이 차이는 원본을 수정할 근거가 아니므로 [검토 기록](2023_CONVERSATIONS_AND_REPORT_AUDIT.md)에만 남겼습니다.

최종보고서는 개인적으로 경고음이 계획한 방식으로 구현됐다고 서술하되, 야외 시험은 경고/위험 수준에 도달하지 않아 **실제 위험 감지 → SMS/경고음 전체 자동 연동은 시험하지 못했다**고 구분합니다. 당시 증거를 넘어 성능·완성도를 단정하지 않습니다.
