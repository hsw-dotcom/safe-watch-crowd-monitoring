# 원본 코드 진위 및 SHA 목록

이 문서는 **2026년에 새로 작성한 검증 기록**입니다. 아래 소스는 `archive/pre-dedup-20261031`에서 확인한 Git blob SHA를 변형 없이 현재 `main`으로 복사한 것입니다. GitHub에서 파일 변경이 발생하면 원본 인증 대상으로 취급하지 마십시오.

| 보관 원본 상대경로 | SHA-1 Git blob | 원본에서 확인된 역할 |
| --- | --- | --- |
| `src/python/main.py` | `4cdb0912703b77e918cf07c37ab58f58dfef5b53` | 주기적 프레임 추출 → 인원 탐지 → 밀집도·단계 판단 → DB INSERT |
| `src/python/count_objects.py` | `084e2541894725143c1c571352d764e0dac2a5cc` | TensorFlow Lite 추론 및 검출 사각형 출력, after.jpg 덮어쓰기 |
| `src/python/stream.py` | `79a2c561d23d9203dac8987984641b84d33b09ff` | Picamera2 기반 MJPEG 스트리밍 |
| `src/python/alarm.py` | `36cec9cdf19633594dc5dec393abbd1b3c0977fa` | DB 위험 조회 및 10초 간격 경고음·Twilio 문자 호출 |
| `src/python/configs.ini` | `50bcf438ccbef59857beb97160be9ac82168430c` | 고정 면적 300, 지연값 15초 |
| `src/web/index.html` | `3b6f95c51e976be408cbe6d25ac30cd1b9b7cbf3` | 메인 웹 화면 및 영상·정보 프레임 배치 |
| `src/web/image.php` | `b8dbf05517577cdf9267bf7a300f6980837ba154` | after.jpg 표시 및 2초 주기 캐시 무효화 갱신(내용은 HTML) |
| `src/web/maininfo.html` | `c3aeaf8d04fc76876537b8089458b68c76bad416` | 상태 표시·위험 알림 UI |
| `src/web/maininfo.php` | `094174ab054576624dfc8093563b125d976e2039` | MariaDB 최신 측정값 조회 |
| `src/web/density.html` | `6a3989bed8d96da9c3cb54523a998c399824c360` | 밀집도 차트 |
| `src/web/densityinfo.php` | `2ce9d3fa130920544fa62182bb3fc9f376201c7f` | 밀집도 그래프의 PHP 조회 |
| `src/web/change.html` | `8c1dc8d7ed90baa5f5c53e74920864f011f4f75e` | 변화율 차트 |
| `src/web/changeinfo.php` | `b41402b6eafae65ef7d22c5045f3b1bdfba873ad` | 변화율 그래프의 PHP 조회 |
| `src/web/graph.html` | `4ea09d698723529fb616724bcf77d8b76bbea11a` | 두 그래프를 표시하는 페이지 |
| `src/web/map.html` | `3f748239b44fb7b405bc9d2676fafe1935e0f7b0` | CCTV 위치 Google 지도 |
| `database/schema_legacy_percent.sql` | `7a19a773482487a1104d001ac7d58a742699b5b9` | cameras, receive_data 및 density VIEW 정의 |

**총 16개 원본 코드·설정 파일.** README와 docs는 2026년 설명 문서이며 당시 소스가 아닙니다. 누락된 TFLite 모델·라벨·음원 파일을 임의로 생성하거나 원본이라 주장하지 않았습니다.

원본 확보 경로: [2026년 통합 정리 전 보존 브랜치](https://github.com/hsw-dotcom/safe-watch-crowd-monitoring/tree/archive/pre-dedup-20261031).

한계: 사용자가 이전 대화에서 올린 ZIP 전체의 바이너리 내용까지 1:1로 대조한 것은 아닙니다. 따라서 2023년 당시 모든 배포 파일을 완전 복구했다고 표시하지 않습니다.
