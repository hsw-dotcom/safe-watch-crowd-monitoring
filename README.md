# Safe Watch — 2023 군중 밀집도 감지 카메라 코드 복원본

> **코드 복원 및 정리 프로젝트**입니다. 원본 Raspberry Pi·카메라·TFLite 모델 등 하드웨어/모델은 현재 없으며, **실장 동작과 2023년 실측 성능을 검증한 프로젝트가 아닙니다.** 2023년 프로젝트 대화와 보관 소스에 근거해 재구성한 코드로, 정확한 역사적 원본과 혼동하지 않습니다.

## 구성

```text
src/python/    main.py, count_objects.py, stream.py, alarm.py, db.py, risk.py, settings.py, configs.ini
src/web/       index.html, graph.html, map.html, image.html, api.php, assets/
database/      schema.sql
 tests/         Python 순수 로직 테스트, 웹 구조 확인
 docs/          근거와 원본 보존 지점, 변경표, 검증 범위
.env.example   개발자가 직접 제공할 환경변수 이름만
```

### 코드 역할 (각 기능은 한 곳에서 관리)
- `src/python/main.py` — 1회 프레임 획득 → 사람 감지 → 위험 계산 → DB 저장 (합성 데이터만 쓰는 `--dry-run` 제공)
- `src/python/count_objects.py` — TFLite 인식 및 `before.jpg`→`after.jpg` 저장 경로
- `src/python/risk.py` — 사람이 계산/위험 경계를 담당하는 유일한 함수 모듈
- `src/python/db.py` — Python 측 MariaDB INSERT / 최근 데이터 SELECT
- `src/python/stream.py` — Picamera2 MJPEG 스트리밍(원본 구조 보존; 실행 검증 안 함)
- `src/python/alarm.py` — 경고음/Twilio 전송 경로(기본 비활성·반복 발송 방지)
- `src/web/index.html` + `assets/dashboard.js` — 단일 대시보드
- `src/web/graph.html` + `assets/chart.js` — 2개 그래프를 단일 화면, 단일 조회로 관리
- `src/web/api.php` — 단일 PHP API `?view=latest`, `?view=history` (Python용 `db.py`와는 별도 프로세스의 코드)
- `src/web/image.html` — `/tensorflow/after.jpg`를 2초마다 캐시 방지 쿼리로 갱신

## 하드웨어 없이 코드와 화면 보기

```bash
python -m unittest discover -s tests -v
python tests/verify_structure.py
python src/python/main.py --dry-run --iterations 3
python -m http.server 8080 --directory src/web
```

마지막 명령을 실행한 후 `http://localhost:8080/index.html?demo=1`과 `http://localhost:8080/graph.html?demo=1`을 열 수 있습니다. **예시 JSON 값은 합성 데이터이며 2023년 실제 측정이나 모델 인식 결과가 아닙니다.** 그래프는 CDN Chart.js를 사용하므로 외부 네트워크 연결이 필요할 수 있습니다.

실제 모드(`demo=1` 없음)는 PHP/MariaDB/카메라·모델·네트워크·경고 음원을 필요로 하지만, 보존 목적일 뿐 현재 구동 검증은 하지 않았습니다.

## 중복 제거 요약

| 이전 중복/불필요 항목 | 통합 결과 |
| --- | --- |
| 2023 보관 소스 `src/` + 재구성본 `reconstructed/` | 메인에는 복원본 `src/` 하나만 유지; 과거 원본은 별도 보관 브랜치와 커밋으로 추적 |
| `index.html`, `maininfo.html` 상태 화면 | `index.html` |
| `density.html`, `change.html`, iframe식 `graph.html` | 2개 캔버스를 가진 `graph.html` |
| `densityinfo.php`, `changeinfo.php`, `maininfo.php`, `db_connect.php` | `api.php`에 안전한 읽기 전용 데이터 조회 통합 |
| 선택용 Flask `app.py`, `alarm.py` 문자 기능 중복 | `alarm.py`만 유지, Flask 재구성본은 제거 |
| `image.php` (실제는 HTML) | `image.html` |
| Nginx/systemd/DMZ 예시와 수동 DB 마이그레이션 | 코드 복원본에서 제거; 보관 브랜치에 남김 |

## 복원 근거와 범위

[원본 및 보완 근거](docs/PROVENANCE.md) · [검증 결과](docs/VALIDATION.md) · [보관본 안내](docs/ARCHIVE.md)

**주의:** 원본 SQL의 위험 임계값(안전 ≤2, 경고 <4, 위험 ≥4)과 `people_count / total_area`는 2023년 코드 구조를 따른 임의 산식이며 실제 군중 안전 기준으로 사용해서는 안 됩니다. 모델/라벨·경고음·실제 시크릿은 저장소에 포함하지 않습니다.
