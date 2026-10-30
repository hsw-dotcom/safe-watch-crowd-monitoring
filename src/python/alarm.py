"""2023 warning loop: poll MariaDB every 10 seconds and alert while 위험.

The 2023 original did not have a 300-second cooldown or transition filtering.
SMS is opt-in in this archival reconstruction to prevent accidental messages.
"""
import logging
import os
import subprocess
import time
from pathlib import Path
from db import latest_measurement

LOG = logging.getLogger('alarm')
HERE = Path(__file__).resolve().parent


def send_sms(danger_level):
    if os.getenv('SAFEWATCH_ENABLE_SMS', '0') != '1':
        LOG.debug('SMS disabled for code-only reconstruction')
        return False
    sid = os.getenv('TWILIO_ACCOUNT_SID')
    token = os.getenv('TWILIO_AUTH_TOKEN')
    sender = os.getenv('TWILIO_FROM_NUMBER')
    recipient = os.getenv('ALERT_RECIPIENT')
    if not all((sid, token, sender, recipient)):
        LOG.warning('Twilio configuration missing; request not sent')
        return False
    from twilio.rest import Client
    Client(sid, token).messages.create(
        body=f'명지대학교 골목1, 위험수준 [{danger_level}]',
        from_=sender, to=recipient)
    return True


def play_sound(filename='warning.wav'):
    wav = Path(os.getenv('SAFEWATCH_WARNING_WAV', str(HERE / filename)))
    if not wav.is_file():
        LOG.warning('경고음 파일을 찾을 수 없습니다: %s', wav)
        return False
    subprocess.run(['aplay', '-D', os.getenv('SAFEWATCH_AUDIO_DEVICE', 'default'),
                    str(wav)], check=True, timeout=60)
    return True


def alert_if_danger(danger_level, sound=play_sound, sms=send_sms):
    """Historical behavior: repeat alarm and SMS on EVERY danger poll."""
    if danger_level != '위험':
        return False
    for callback, args in ((sms, ('위험',)), (sound, ())):
        try:
            callback(*args)
        except Exception:
            LOG.exception('경고 채널 호출 실패')
    return True


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    interval = max(1, float(os.getenv('SAFEWATCH_ALARM_POLL_SECONDS', '10')))
    while True:
        try:
            row = latest_measurement()
            alert_if_danger(row['danger_level'] if row else None)
            LOG.info('작동 중...')
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            LOG.exception('DB 조회 오류')
        time.sleep(interval)

if __name__ == '__main__':
    main()
