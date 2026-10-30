# 복원 범위 및 근거: 2023년 Q&A·2026년 저장소 대조

## A. 확인된 원본 근거
- GitHub: `hsw-dotcom/safe-watch-crowd-monitoring`, `main` (2026-10-31 확인, 소스 트리 기준 `52792eac6652580e118b3b3c33a964fc1bf1b308`)
- 연결된 원본에서 확인: `src/python/{main.py,count_objects.py,stream.py,alarm.py,configs.ini}`, `src/web/{index.html,image.php,maininfo.html,maininfo.php,graph.html,density.html,densityinfo.php,change.html,changeinfo.php,map.html}`, `database/schema_legacy_percent.sql` 등.
- 프로젝트 대화 기록: 2023년 5월 11일 HTML 페이지/DB 접근, 5월 17일 차트 크기, 6월 3일 SMS, 라즈베리파이 웹 공개/IP 접근 관련 질문.
- 2023년 Q&A 스니펫: `/tensorflow/after.jpg`만 읽기, `? + new Date().getTime()`로 2초 이미지 새로고침, PHP/DB 기반 정보 표시, 웹 접근 경로와 500 서버 오류 이슈.
- 최근 프로젝트 논의: ipTIME DMZ에 내부 IP를 대표 호스트로 지정했으며 Python HTTP(MJPEG), Nginx/PHP/MariaDB의 분리를 설명함. `127.0.0.1:5000/send_sms` 프런트엔드 호출은 외부 브라우저에서 라즈베리파이가 아닌 *브라우저 자신*을 가리키는 문제였음.

## B. 원본 대비 개선 코드
| 영역 | 2023년 확인된 구성 | 재구성 적용 / 판단 근거 | 분류 |
|---|---|---|---|
| 카메라 | `stream.py` Picamera2+MJPEG :8000 | 같은 엔드포인트와 분리 실행 유지, 연결/종료 처리 정리 | 근거 기반 개선 |
| 추론 | `main.py` 주기적 정지영상, `count_objects.detect()` 호출 | 인식 1회마다 `before.jpg`→`after.jpg` 경로 유지, 추론 인터프리터 캐시, 실제 영상 너비/높이 box 사용 | 근거 기반 개선 |
| 처리 주기 | `configs.ini delay=15`, 코드에서도 처리 후 `time.sleep(delay_time)` | 연산시간 차감 후 남은 간격만 sleep. 실제 1초 인식이라고 주장하지 않음 | 코드 결함 보완 |
| 원본 반복 횟수 | 100회 반복 후 종료 | 서비스 구동 편의를 위해 기본 무한 반복, `max_iterations` 설정 가능 | **새 설계** |
| 위험 임계치 | 안전 ≤2, 경고 <4, 위험 ≥4; 밀집도=인원/설정면적 | 같은 규칙을 설정화, 입력 유효성 검사 | 원본 규칙 보존 |
| 장애물 보정 | 코드에 이름은 있으나 모델 호출 주석 처리 | 비활성화 유지; 근거 없는 분석 기능을 만들지 않음 | 원본 규칙 보존 |
| DB | MariaDB `cameras`,`receive_data`,`density` | 카메라 기본행 선등록, `people_count` 필드 추가, 카메라별 직전값 `LAG`, 0 나눗셈 방어 | **스키마 변경** |
| 변화량 표시 | 제출 SQL 비율(%), 개인 보고서 설명에는 절대 차이 | `change_rate`(%)와 `change_amount`(절대 차) 함께 제공; UI는 비율로 표기 | 출처 불일치 해소 |
| 웹 | Nginx HTML/PHP, AJAX, 그래프, 지도, 실시간/검출 영상 나란히 표시 | 원래 URL/페이지 이름 유지, 재로드 대신 API 폴링, 빈 결과 처리 | 근거 기반 개선 |
| 이미지 캐시 | 2초 주기 `/tensorflow/after.jpg?timestamp` | `image.php`에 그대로 적용 | 2023 대화 근거 |
| SMS | 원본 `alarm.py` Twilio, Flask `app.py` 누락, 브라우저 loopback 오류 | DB 폴링 경고를 기본 동선으로 사용, 중복 발송 방지, SMS 기본 꺼짐. 선택적 localhost Flask `app.py` 신규 작성 | **원본 미확보 재구성** |
| 외부 접근 | ipTIME 대표 내부 IP(DMZ) 테스트 | 라즈베리파이 고정 IP/공인 IP 테스트 관련 문서만 추가; 외부 공개/보안 검증은 미실시 | 문서화 |
| 자동 시작 | 부팅 후 Python 자동 실행 경험 기록 | systemd 예시 3개 추가; **당시 실제로 systemd 사용했다는 근거는 없음** | **새 배포 예시** |

## C. 대조하지 못한 원본
과거 프로젝트/다른 대화방 첨부로 표시된 `개발코드.zip`, `개발코드(1).zip`, `backup.zip`, `제출자료.zip`, `SafeWatch_추가원본_분류정리_비공개용.zip` 등은 파일 이름·크기가 확인되었지만 이 작업 환경에서 ZIP 내부 바이너리를 직접 열 수 없어 파일 단위 비교와 전체 원본 재포장이 불가했음. **그 원본까지 모두 대조·흡수했다고 주장하지 않음.**

2023년의 대화 문장 전체가 이 세션에 원문으로 모두 제공된 것은 아니므로, 그 내용에서 유추한 구현은 `RECONSTRUCTED`로 명시함. 기존 GitHub `main`의 원본 내용은 별도 보존됨.

## D. 실행 검증 수준
- Python 문법/단위테스트, PHP 문법 검사, 웹 내부 파일 참조 검사: 정적 로컬 검증 가능.
- 미검증: Raspberry Pi 물리 카메라·Picamera2, TFLite 모델 파일별 입출력 텐서, 실제 MariaDB/MySQL 버전 호환성, 외부 네트워크·DMZ 노출, 브라우저 자동 사운드 정책, 경고음 하드웨어/실제 문자 도착.
