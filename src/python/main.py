import csv
import cv2
import time
import configparser
import count_objects
import netifaces as ni
import os

# Historical source with database credentials externalized for public archival use.
def get_ip():
    ip_info = ni.ifaddresses('wlan0')
    ip = ip_info[ni.AF_INET][0]['addr']
    return ip

def get_config():
    config = configparser.ConfigParser()
    config.read('configs.ini')
    delay_time = float(config['settings']['delay'])
    total_area = float(config['settings']['total_area'])
    return delay_time, total_area

def get_frame(ip):
    url = "http://" + ip + ":8000/stream.mjpg"
    capture = cv2.VideoCapture(url)
    ret, img = capture.read()
    cv2.imwrite('/home/pi/project/image/before.jpg', img)

def write_to_db(crowd_density, danger_level):
    import mysql.connector
    config = {
        'user': os.getenv('SAFEWATCH_DB_USER', 'root'),
        'password': os.environ['SAFEWATCH_DB_PASSWORD'],
        'host': 'localhost',
        'database': 'safewatch'
    }
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    query = "INSERT INTO receive_data (crowd_density, danger_level) VALUES (%s, %s)"
    values = (crowd_density, danger_level)
    cursor.execute(query, values)
    conn.commit()
    conn.close()

def count_object():
    objects = count_objects.detect()
    return objects

def get_obstacle_area(obstacles):
    total_area = 0
    f = open("obstacle_area.csv", 'r')
    obstacle_list = csv.DictReader(f)
    print(obstacle_list.fieldnames)
    return total_area

def get_alert_level(total_area, people_num):
    density = people_num / total_area
    if density <= 2:
        return '안전', density
    elif (density > 2) and (density < 4):
        return '경고', density
    else:
        return '위험', density

def main():
    delay_time, total_area = get_config()
    ip = get_ip()
    for i in range(100):
        start_time = time.time()
        get_frame(ip)
        people_num, obstacles = count_objects.detect()
        print("프레임 저장 완료")
        exec_time = time.time() - start_time
        wait_time = delay_time - exec_time
        alert_level, crowd_density = get_alert_level(total_area, people_num)
        write_to_db(crowd_density, alert_level)
        print("위험 단계 :", alert_level)
        print("실행 시간: %.2f초" % exec_time)
        print("대기 시간: %.2f초" % wait_time)
        print("===========================================")
        time.sleep(delay_time)

if __name__ == '__main__':
    main()
