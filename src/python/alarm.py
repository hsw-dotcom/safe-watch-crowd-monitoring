"""DB danger polling: state-change detection + cooldown prevents alert storms.

Historical alarm.py tried to play WAV and send Twilio SMS every 10 seconds while
danger persisted. This reconstructed variant requires explicit opt-in for SMS.
"""
import logging
import os
import subprocess
import time
from pathlib import Path
from db import latest_measurement

LOG = logging.getLogger('alarm')
HERE = Path(__file__).resolve().parent

def should_alert(last_id, last_level, current_row, last_alert_time, now, cooldown):
    if not current_row or current_row['danger_level'] != '위험':
        return False
    # fire on newly observed danger only if minimum cooldown elapsed
    is_new = current_row['id'] != last_id
    entered_danger = last_level != '위험'
    return (is_new and entered_danger and now - last_alert_time >= cooldown)

def send_sms():
    if os.getenv('SAFEWATCH_ENABLE_SMS', '0') != '1':
        LOG.info('SMS 비활성화 상태: SAFEWATCH_ENABLE_SMS=1 필요')
        return False
    sid = os.getenv('TWILIO_ACCOUNT_SID')
    token = os.getenv('TWILIO_AUTH_TOKEN')
    sender = os.getenv('TWILIO_FROM_NUMBER')
    recipient = os.getenv('ALERT_RECIPIENT')
    if not all((sid, token, sender, recipient)):
        LOG.error('Twilio 환경변수 미설정: 실제 발송하지 않습니다.')
        return False
    from twilio.rest import Client
    Client(sid, token).messages.create(
        body=os.getenv('SAFEWATCH_ALERT_MESSAGE', 'Safe Watch 위험 수준 감지'),
        from_=sender, to=recipient)
    LOG.info('SMS 발송 요청 완료 (수신 성공 여부는 별도 확인 필요)')
    return True

def play_audio():
    sound = Path(os.getenv('SAFEWATCH_WARNING_WAV', str(HERE / 'warning.wav')))
    if not sound.is_file():
        LOG.warning('경고음 파일 누락: %s', sound)
        return False
    device = os.getenv('SAFEWATCH_AUDIO_DEVICE', 'default')
    subprocess.run(['aplay', '-D', device, str(sound)], check=True, timeout=60)
    return True

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    camera = int(os.getenv('SAFEWATCH_CAMERA_NUMBER', '1'))
    poll = max(1, float(os.getenv('SAFEWATCH_ALARM_POLL_SECONDS', '10')))
    cooldown = max(1, float(os.getenv('SAFEWATCH_ALERT_COOLDOWN_SECONDS', '300')))
    last_id, last_level, last_alert_time = None, None, float('-inf')
    while True:
        try:
            row = latest_measurement(camera)
            now = time.monotonic()
            if should_alert(last_id, last_level, row, last_alert_time, now, cooldown):
                # Mark once per danger episode; do not repeat merely on polling.
                last_alert_time = now
                for func in (play_audio, send_sms):
                    try:
                        func()
                    except Exception:
                        LOG.exception('경고 채널 처리 오류')
            if row:
                last_id, last_level = row['id'], row['danger_level']
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            LOG.exception('DB 조회 오류 (다음 주기에 재시도)')
        try:
            time.sleep(poll)
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()
