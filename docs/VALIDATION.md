# 물리 하드웨어가 없는 코드 복원 검증

다음은 순수 로직·구문·정적 파일 검사입니다. 카메라·모델·DB·음향·Twilio는 연결하지 않았습니다.

```bash
python -m unittest discover -s tests -v
python tests/verify_structure.py
python -m compileall -q src/python tests
php -l src/web/api.php                  # PHP 설치 시
node --check src/web/assets/dashboard.js # Node 설치 시
node --check src/web/assets/chart.js
python src/python/main.py --dry-run --iterations 7
```

## 검증 항목
- 최종 발표의 0~2명 안전, 3~4명 경고, 5명 이상 위험 판정
- 원본 고정 면적 300 기준 밀집도 산식
- 위험 상태에서 쿨다운 없이 매 조회마다 경고 채널 호출 (실제 발송하지 않는 모의 객체 사용)
- 원본과 같은 `before.jpg`/`after.jpg` 직접 덮어쓰기, 변환된 모델 로드 방식의 코드 경로
- 신규 `people_count` DB 열/0분기 보호 추가 없이 원본 SQL VIEW 구조
- 웹 API/데모 JSON 계약, HTML/JavaScript 리소스 연결

해당 테스트가 통과해도 모델 정확도나 실제 물리 장치·DB 동작 검증을 의미하지 않습니다.
