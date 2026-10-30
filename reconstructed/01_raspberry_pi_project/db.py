"""MariaDB storage adapter: parameterized queries and explicitly configured credentials."""
import os

def connection():
    import mysql.connector
    password = os.getenv('SAFEWATCH_DB_PASSWORD')
    if password is None:
        raise RuntimeError('SAFEWATCH_DB_PASSWORD 환경변수를 설정해야 합니다.')
    return mysql.connector.connect(
        host=os.getenv('SAFEWATCH_DB_HOST', '127.0.0.1'),
        port=int(os.getenv('SAFEWATCH_DB_PORT', '3306')),
        user=os.getenv('SAFEWATCH_DB_USER', 'safewatch'),
        password=password,
        database=os.getenv('SAFEWATCH_DB_NAME', 'safewatch'),
        connection_timeout=5,
    )

def save_measurement(camera_number, people_count, crowd_density, danger_level):
    cn = connection()
    try:
        cur = cn.cursor()
        try:
            cur.execute("""INSERT INTO receive_data
                (camera_number, people_count, crowd_density, danger_level)
                VALUES (%s,%s,%s,%s)""",
                (camera_number, people_count, crowd_density, danger_level))
            cn.commit()
            return cur.lastrowid
        finally:
            cur.close()
    except Exception:
        cn.rollback()
        raise
    finally:
        cn.close()

def latest_measurement(camera_number):
    cn = connection()
    try:
        cur = cn.cursor(dictionary=True)
        try:
            cur.execute("""SELECT id, camera_number, people_count, crowd_density,
                danger_level, update_time FROM receive_data
                WHERE camera_number=%s ORDER BY id DESC LIMIT 1""",
                (camera_number,))
            return cur.fetchone()
        finally:
            cur.close()
    finally:
        cn.close()
