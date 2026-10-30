# 로컬 검증 보고서
- 이 파일은 자동화 검증 보고를 위한 자리입니다. 실제 수행 결과는 빌드 후 `FINAL_CHECKS.txt`에도 기록합니다.
- `python -m unittest discover -s 06_tests -p 'test_*.py' -v`
- `python 06_tests/verify_structure.py`
- 모든 Python 파일: `python -m py_compile 01_raspberry_pi_project/*.py`
- 모든 PHP 파일: `php -l <file>`
- JS: `node --check ...` (node가 있는 환경에서만)

소프트웨어 정적 테스트가 통과하더라도 실제 Raspberry Pi/DB/TFLite/Twilio 운영 결과는 보장하지 않습니다.
