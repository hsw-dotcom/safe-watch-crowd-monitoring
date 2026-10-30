# Safe Watch (2023) — 최종 발표 기준 코드 복원본

**목표: 당시 캡스톤의 기능·방법을 최대한 정확하게 기록하는 것.**
실물 Raspberry Pi·모델·DB 없이 코드를 보존하고 검토합니다. 2023년 원본을 그대로 재현했다고 주장하지 않습니다.

- **최종 발표가 우선**: 안전 0~2명, 경고 3~4명, 위험 5명 이상 (최종 PPT는 안전 1~2명으로 설명; 0명도 안전 처리)
- **고정 면적 300**: 원본 `configs.ini` 고정값을 사용해 밀집도는 `감지 인원 / 300`. 장애물 면적 차감이나 실시간 면적 재계산 없음
- **모델 그대로 사용**: 학습/추출된 `people_detect.tflite` 파일을 불러오기만 하며 모델 업데이트·재학습 없음
- **이미지 덮어쓰기**: `before.jpg`와 `/tensorflow/after.jpg`를 프레임마다 직접 갱신
- **경고 반복**: 당시 `alarm.py`처럼 10초마다 위험을 확인하고 위험이면 다시 알림; SMS는 사고 방지를 위해 기본 비활성
- **변화율**: 기존 SQL의 직전 행 조회와 백분율 계산 유지. 직전값 0에 대한 별도 나눗셈 방어는 당시 구현이 아니었음

## 파일 배치 (중복 정리 유지)

```text
src/python/    main.py, count_objects.py, stream.py, alarm.py, db.py, risk.py, settings.py, configs.ini
src/web/       index.html, image.html, graph.html, map.html, api.php, assets/
database/      schema.sql
tests/         순수 Python 로직 및 정적 파일 구조 검사
docs/          최종 PPT 대조, 코드 출처, 원본 보관 이력
.env.example   실제 비밀번호가 없는 설정 이름
```

`src/python/main.py`는 영상에서 프레임을 얻고, TFLite 사람 수를 읽고, 정해진 면적과 인원 수에 따라 밀집도·위험을 계산해 DB에 기록합니다. `src/python/alarm.py`는 DB 위험 행을 주기적으로 확인합니다. 웹은 원래 PHP·Nginx·MariaDB 구조를 따라 상태/그래프/지도/이미지를 제공하되, 중복된 역할의 페이지는 하나로 합쳤습니다. 웹 통합 API와 브라우저 데모는 후대의 코드 정리 방법입니다.

## 하드웨어 없는 검증

```bash
python -m unittest discover -s tests -v
python tests/verify_structure.py
python src/python/main.py --dry-run --iterations 7
python -m http.server 8080 --directory src/web
```

웹의 `http://localhost:8080/index.html?demo=1`과 `graph.html?demo=1`은 **합성 예시**만 보여줍니다. 이 예시와 테스트는 실제 2023년 측정이나 성능 결과가 아닙니다. 그래프는 Chart.js CDN을 참조합니다.

## 출처, 차이점, 주의

[최종 발표 우선 복원 근거](docs/PRESENTATION_PRIORITY.md) · [복원 출처](docs/PROVENANCE.md) · [검사](docs/VALIDATION.md) · [2023년 원본 보관](docs/ARCHIVE.md)

2023년 소스 파일은 GitHub `archive/pre-dedup-20261031` 브랜치에 보존되었습니다. 원본은 변경하지 않았고 이 `main`은 **최종 발표 내용과 원본 사이의 불일치를 명시적으로 해소한 코드 복원본**입니다. 사람 수 기준은 역사적 시연의 기술이지 보편적 인명 안전 기준이 아닙니다.
