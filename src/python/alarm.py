import os
import mysql.connector
import time
import subprocess
from twilio.rest import Client

device = "hw:3"

# Twilio 계정 정보
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_number = os.environ['TWILIO_FROM_NUMBER']

def get_danger_level():
    # MySQL 서버 접속 설정
    db_config = {
        "host": "localhost",
        "user": os.getenv("SAFEWATCH_DB_USER", "root"),
        "password": os.environ["SAFEWATCH_DB_PASSWORD"],
        "database": "safewatch"
    }

    # 데이터베이스 연결
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # 쿼리 실행
    query = "SELECT danger_level FROM receive_data ORDER BY id DESC LIMIT 1;"
    cursor.execute(query)

    # 결과 가져오기
    result = cursor.fetchone()
    danger_level = result[0] if result else None

    # 연결 종료
    cursor.close()
    conn.close()

    return danger_level

def send_sms(danger_level):
    # Twilio 클라이언트 생성
    client = Client(account_sid, auth_token)

    try:
        recipients = [os.environ['ALERT_RECIPIENT']]
        for recipient in recipients: 
            # SMS 메시지 생성 및 전송
            message = client.messages.create(
                 body="명지대학교 골목1, 위험수준 [" + danger_level + "]",
                 from_=twilio_number,
                 to=recipient
            )

        return "SMS sent"
    except Exception as e:
        return f"Error: {str(e)}"

def play_sound(file_path):
    # 외부 프로그램 실행
    subprocess.run(["aplay", "-D", device, "--disable-resample", file_path])



# 주기적으로 데이터베이스에서 위험 단계 확인하고, 소리 재생
while True:
    danger_level = get_danger_level()
    if danger_level == "위험":
        # 소리 재생 코드 작성
        send_sms(danger_level)
        play_sound("warning.wav")

    print("작동 중...")
    # 일정 시간 대기
    time.sleep(10)  # 10초 간격으로 데이터베이스에서 위험 단계 확인
