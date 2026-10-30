# 공개 보안 및 출처

- 원본 ZIP/최종 보고서/PPT/사진·동영상은 인증정보, 연락처, 얼굴 등으로 공개 저장소에 게시하지 않습니다.
- PHP/Python의 평문 DB 비밀번호, Twilio 인증정보/발신·수신 전화번호를 공개 사본에서는 환경변수로 분리합니다.
- 브라우저 측 자동 SMS 호출은 공개 사본에서 비활성화합니다. 원본의 127.0.0.1:5000 호출은 클라이언트 측에서 의도치 않은 주소를 가리킬 수 있습니다.
- 과거 유효했던 API 토큰과 Twilio 자격증명은 현재도 유효하다면 폐기·교체해야 합니다.
- count_objects.py는 원본 주석상 TensorFlow Lite 관련 예제 및 Evan Juras 예제의 영향을 받았습니다. 참고: https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi
- stream.py도 Picamera2 MJPEG 서버 예제를 기반으로 합니다. 관련 상위 라이선스 및 팀 공동 저작권은 별도 확인이 필요합니다.
- 이 저장소는 팀 프로젝트의 보존 기록입니다. 계정 소유자가 모든 소스의 단독 창작자라고 주장하지 않습니다. 프로젝트 전체에 대한 무조건적인 라이선스는 부여하지 않습니다.
