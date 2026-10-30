# Picamera2 카메라 점유 충돌: 보존된 오류 로그

사용자가 당시 오류 기록을 추가 제공했습니다. 프로젝트 경로는 `/home/pi/project/stream.py`이며 `Picamera2()` 생성 중 예외가 발생했습니다.

```text
RuntimeError: Failed to acquire camera: Device or resource busy
RuntimeError: Camera __init__ sequence did not complete.
```

## 검증된 사실

- Picamera2의 `_open_camera()` → `camera.acquire()` 단계에서 장치 획득에 실패했습니다.
- `stream.py`가 카메라를 열지 못해 초기화가 완료되지 않았습니다.
- **다른 프로세스가 카메라를 점유했을 가능성이 높지만**, 이 로그만으로 점유 주체는 알 수 없습니다. 권한·드라이버/장치 상태 등도 점검 대상입니다.
- 오류 로그는 **장애 발생 사실의 증거**이며, 해결 조치 또는 최종 복구 성공을 직접 증명하지 않습니다.

## 당시 또는 향후 사용할 수 있는 점검 경로(새로 작성한 참고사항)

```bash
ps aux | grep -E 'python|libcamera|rpicam'
sudo fuser -v /dev/video*
```

해당 장치를 점유한 프로세스가 실제로 확인되면 필요한 카메라 작업만 정상 종료 후 재시도할 수 있습니다. **과거에 위 명령을 실행했다고 주장하는 문서는 아닙니다.**

두 개의 독립 `Picamera2` 프로세스에서 같은 카메라를 동시에 점유하는 대신, 스트리밍 프로세스가 제공하는 MJPEG 프레임을 분석 루틴에서 소비하는 구조가 원본 `stream.py`/`main.py`에 등장합니다. 이 연동 구조가 실제 장애를 해결했다는 직접적인 로그는 없습니다.

## 취업용 설명 시 주의

가능: “Raspberry Pi 카메라 초기화 시 장치 점유 오류가 발생한 로그를 분석하여 프로세스 동시 접근 가능성을 확인했다.”

불가: “특정 프로세스를 종료하여 장애를 해결했다” / “운영 장애를 즉시 복구했다”와 같은 미확인 조치·성과의 단정.
