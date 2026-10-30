# 코드 파일별 출처 / 변경 경계와 SHA (2026-10-31 정리)

> **구분**: 2023년 원본 소스 자체 / 기존 공개용 보안 처리 보관본 / 당사자 확인 기반 2026년 수정본은 서로 다릅니다. Git blob SHA는 **현재 공개 버전 파일의 식별자**로서 2023년 실제 최종 실행 코드와 바이트 동일함을 보증하지 않습니다.

| 현행 코드 경로 | 현재 Git blob SHA | 보존·수정 경계 |
| --- | --- | --- |
| `src/python/main.py` | `8a41353107e367e7ce0d3e2ca423f20cdadac6b0` | 보관 소스를 토대로 보고서의 인자 구조 및 사용자 확인 인원 수 단계 판정을 2026년에 반영 (2023 최종 파일 원문 미확보) |
| `src/python/configs.ini` | `c3758d3019cfbf55f40101ef7682027133cc0d63` | 보고서와 사용자 확인에 따라 delay 10, total_area 300으로 2026년에 설정 갱신 |
| `src/python/count_objects.py` | `084e2541894725143c1c571352d764e0dac2a5cc` | 기존 보안 처리 보관본: TFLite, JPG 덮어쓰기 |
| `src/python/stream.py` | `79a2c561d23d9203dac8987984641b84d33b09ff` | 기존 보안 처리 보관본: Picamera2 / MJPEG :8000 |
| `src/python/alarm.py` | `36cec9cdf19633594dc5dec393abbd1b3c0977fa` | 기존 보안 처리 보관본: Twilio 및 WAV 경고 |
| `src/web/index.html` | `3b6f95c51e976be408cbe6d25ac30cd1b9b7cbf3` | 기존 보안 처리 보관본: 대시보드 |
| `src/web/image.php` | `b8dbf05517577cdf9267bf7a300f6980837ba154` | 기존 보안 처리 보관본: 2초 JPG 갱신 |
| `src/web/maininfo.html` | `c3aeaf8d04fc76876537b8089458b68c76bad416` | 기존 보안 처리 보관본: 정보·위험 UI, 사용하지 않은 브라우저 문자 시도 경로 잔존 |
| `src/web/maininfo.php` | `094174ab054576624dfc8093563b125d976e2039` | 기존 보안 처리 보관본: DB 조회 |
| `src/web/density.html` | `6a3989bed8d96da9c3cb54523a998c399824c360` | 기존 보안 처리 보관본: 밀집도 그래프 |
| `src/web/densityinfo.php` | `2ce9d3fa130920544fa62182bb3fc9f376201c7f` | 기존 보안 처리 보관본: 최근 20개 조회 |
| `src/web/change.html` | `8c1dc8d7ed90baa5f5c53e74920864f011f4f75e` | 기존 보안 처리 보관본: 변화율 그래프 |
| `src/web/changeinfo.php` | `b41402b6eafae65ef7d22c5045f3b1bdfba873ad` | 기존 보안 처리 보관본: SQL VIEW 차트 데이터 |
| `src/web/graph.html` | `4ea09d698723529fb616724bcf77d8b76bbea11a` | 기존 보안 처리 보관본: 차트 화면 |
| `src/web/map.html` | `3f748239b44fb7b405bc9d2676fafe1935e0f7b0` | 기존 보안 처리 보관본: CCTV 위치 지도 |
| `database/schema_legacy_percent.sql` | `7a19a773482487a1104d001ac7d58a742699b5b9` | 기존 보안 처리 보관본: 백분율 변화율(%) SQL; 보고서의 절대차 SQL과 불일치 |

현행 **16개 코드·설정 파일 중 14개**는 이번 정리에서 기존 Git SHA 그대로 유지합니다. **두 개(`main.py`, `configs.ini`)는 보고서와 최종 구현 확인을 반영해 수정**했습니다.

## 변경 전 버전 추적

- 과거 `src/python/main.py` blob: `4cdb0912703b77e918cf07c37ab58f58dfef5b53` — 위험 기준을 `인원/300`에 적용.
- 과거 `src/python/configs.ini` blob: `50bcf438ccbef59857beb97160be9ac82168430c` — `delay=15`.
- `database/schema_legacy_percent.sql` blob `7a19a773482487a1104d001ac7d58a742699b5b9`은 **백분율 계산**을 보존. 개인 최종보고서 29쪽의 절대차 SQL과 다릅니다.

**변경 시점**: 2026-10-31. 최종 위험 단계의 정확한 2023년 파일 원문이 없으므로 **당사자·발표 확인 기반 최소 수정**으로 표시합니다. 2023년 원본에 추가 구현이 있었다는 뜻으로 해석하지 않습니다.
