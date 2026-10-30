# 코드만 있는 복원 환경의 검증 범위

다음은 소스·합성 데이터 기반 점검입니다. 실제 Raspberry Pi, Picamera2, TFLite 모델, DB 서버, SMS, 음향장치는 없으며 해당 환경에서 직접 실행하지 않았습니다.

- `python -m unittest discover -s tests -v` — 위험 계산 경계값, 경고 상태 변화, 합성 JSON·API 계약 확인
- `python tests/verify_structure.py` — HTML의 로컬 리소스 참조, 중복 PHP·HTML 제거 상태 확인
- `python -m compileall -q src/python tests` — Python 구문 검사
- `php -l src/web/api.php` — PHP 구문 검사 (PHP 설치 환경일 때)
- `node --check src/web/assets/dashboard.js && node --check src/web/assets/chart.js` — JS 구문 검사 (Node 설치 환경일 때)
- `python src/python/main.py --dry-run --iterations 3` — 카메라·모델·DB 없이 계산 파이프라인 흐름 확인

`--dry-run`과 `?demo=1`에 쓰는 값은 **임의 생성 예시**입니다. 정확도·실시간성·실제 경고 발송을 뜻하지 않습니다.

## 2026-10-31 코드 정리 시 검사 결과

- Python `unittest` 9개 통과 (하드웨어/DB 없음)
- 구조 참조 확인 통과
- `compileall` Python 구문 검사 통과
- PHP `php -l` 통과
- JavaScript `node --check` 2개 통과
- `main.py --dry-run --iterations 3` 모의 처리 3회 정상 종료

실제 하드웨어/모델, DB 연결 및 문자 전송은 **검증하지 않았습니다.**
