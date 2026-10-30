"""2023 MariaDB storage columns retained; credential handling is externalized."""
import os


def connection():
    import mysql.connector
    password = os.getenv('SAFEWATCH_DB_PASSWORD')
    if password is None:
        raise RuntimeError('SAFEWATCH_DB_PASSWORD is required')
    return mysql.connector.connect(
        host=os.getenv('SAFEWATCH_DB_HOST', '127.0.0.1'),
        user=os.getenv('SAFEWATCH_DB_USER', 'safewatch'),
        password=password,
        port=int(os.getenv('SAFEWATCH_DB_PORT', '3306')),
        database=os.getenv('SAFEWATCH_DB_NAME', 'safewatch'),
        connection_timeout=5,
    )


def save_measurement(crowd_density, danger_level):
    """2023 source inserted only these two columns."""
    cn = connection()
    try:
        cur = cn.cursor()
        try:
            cur.execute('INSERT INTO receive_data (crowd_density, danger_level) VALUES (%s, %s)',
                        (crowd_density, danger_level))
            cn.commit()
            return cur.lastrowid
        finally:
            cur.close()
    except Exception:
        cn.rollback()
        raise
    finally:
        cn.close()


def latest_measurement():
    cn = connection()
    try:
        cur = cn.cursor(dictionary=True)
        try:
            cur.execute('SELECT id, crowd_density, danger_level, update_time '
                        'FROM receive_data ORDER BY id DESC LIMIT 1')
            return cur.fetchone()
        finally:
            cur.close()
    finally:
        cn.close()
