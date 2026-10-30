import os
import mysql.connector
import time
import subprocess
from twilio.rest import Client

device = "hw:3"
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_number = os.environ['TWILIO_FROM_NUMBER']

def get_danger_level():
    db_config = {
        "host": "localhost",
        "user": os.getenv("SAFEWATCH_DB_USER", "root"),
        "password": os.environ["SAFEWATCH_DB_PASSWORD"],
        "database": "safewatch"
    }
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT danger_level FROM receive_data ORDER BY id DESC LIMIT 1;"
    cursor.execute(query)
    result = cursor.fetchone()
    danger_level = result[0] if result else None
    cursor.close()
    conn.close()
    return danger_level

def send_sms(danger_level):
    client = Client(account_sid, auth_token)
    try:
        recipients = [os.environ['ALERT_RECIPIENT']]
        for recipient in recipients:
            message = client.messages.create(
                body="명지대학교 골목1, 위험수준 [" + danger_level + "]",
                from_=twilio_number,
                to=recipient
            )
        return "SMS sent"
    except Exception as e:
        return f"Error: {str(e)}"

def play_sound(file_path):
    subprocess.run(["aplay", "-D", device, "--disable-resample", file_path])

while True:
    danger_level = get_danger_level()
    if danger_level == "위험":
        send_sms(danger_level)
        play_sound("warning.wav")
    print("작동 중...")
    time.sleep(10)
