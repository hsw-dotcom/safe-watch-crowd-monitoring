# 복원 상태·누락·보존 브랜치 (2026년 작성)

## A. 유지한 것: Git blob SHA가 일치하는 원본

- Python 5개: `main.py`, `count_objects.py`, `stream.py`, `alarm.py`, `configs.ini`.
- HTML/PHP 10개: `index.html`, `image.php`, `maininfo.html`, `maininfo.php`, `graph.html`, `density.html`, `densityinfo.php`, `change.html`, `changeinfo.php`, `map.html`.
- SQL 1개: `schema_legacy_percent.sql`.

원본 외 코드가 0개입니다. 루트 README 및 docs는 **설명용 비실행 문서**입니다.

## B. 원본만으로 가능한 것과 불가능한 것

**가능**: 프로젝트의 주요 함수·파일 구조, 영상 → 사람 검출 → 위험 결과 저장 → 웹 조회 → 경고 요청 흐름을 확인하고 분석할 수 있음. 원본 PHP/HTML 웹 화면과 그래프 구성 확인 가능.

**불가능하거나 미확인**: 모델 파일·라벨, 음원, 보안 변수 및 과거 실행 환경 없이 장비/DB 연동을 검증할 수 없음. 모델 검출 정확도, 실제 SMS 수신, 하드웨어 작동도 재현했다고 말할 수 없음.

## C. 보관 원본에서 확인된 불완전 지점

1. `count_objects.py`는 `models/people_detect.tflite`와 `models/people_label.txt`를 외부 파일로 요구. 파일 본체는 현재 `main`에 없음.
2. `alarm.py`는 `warning.wav` 및 Twilio 환경변수와 장치가 있어야 경고를 실행. 모델과 마찬가지로 WAV 원본은 미확보.
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

구형 ZIP 파일(`개발코드.zip`, `backup.zip`, `제출자료.zip`)의 전체 내부 구성과 대조할 수 없었으므로 이 16개가 전부인지는 미확인입니다.
