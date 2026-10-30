import csv
import cv2
import time
import configparser
import count_objects
import netifaces as ni
import os

# 웹서버 접속을 위한 IP 가져오기
def get_ip():
    ip_info = ni.ifaddresses('wlan0')
    ip = ip_info[ni.AF_INET][0]['addr']
    return ip
    
# 프레임 저장 시간과 전체 면적 값을 config.ini로 부터 불러오기
def get_config():
    config = configparser.ConfigParser()
    config.read('configs.ini')
    delay_time = float(config['settings']['delay'])
    total_area = float(config['settings']['total_area'])

    return delay_time, total_area

# 웹서버 영상으로 부터 프레임 추출해 저장
def get_frame(ip):
    url = "http://" + ip + ":8000/stream.mjpg"
    capture = cv2.VideoCapture(url)
    ret, img = capture.read()
    cv2.imwrite('/home/pi/project/image/before.jpg', img)


# DB에 면적도와 위험 단계를 SQL 문으로 저장
def write_to_db(crowd_density, danger_level):
    import mysql.connector

    # 데이터베이스 연결 설정
    config = {
        'user': os.getenv('SAFEWATCH_DB_USER', 'root'),
        'password': os.environ['SAFEWATCH_DB_PASSWORD'],
        'host': 'localhost',
        'database': 'safewatch'
    }

    # 데이터베이스 연결
    conn = mysql.connector.connect(**config)

    # 커서 생성
    cursor = conn.cursor()

    query = "INSERT INTO receive_data (crowd_density, danger_level) VALUES (%s, %s)"
    values = (crowd_density, danger_level)

    cursor.execute(query, values)

    # 변경사항 저장
    conn.commit()

    # 연결 종료
    conn.close()

# Count_object.py의 함수를 통해 인원 감지
def count_object():
    objects = count_objects.detect()
    return objects

# 장애물 면적 계산
def get_obstacle_area(obstacles):
    total_area = 0

    f = open("obstacle_area.csv", 'r')
    obstacle_list = csv.DictReader(f)

    print(obstacle_list.fieldnames)

    return total_area


# 전체 면적과 사람 수를 불러와 위험 단계를 계산
def get_alert_level(total_area, people_num):
    # 사람 평균 면적은 고정
    density = people_num / total_area

    if density <= 2:
        return '안전', density
    elif (density > 2) and (density < 4):
        return '경고', density
    else:
        return '위험', density


def main():
    # 기본 설정값들과 ip정보를 가져온다
    delay_time, total_area = get_config()
    ip = get_ip()
    
    for i in range(100):
        start_time = time.time()
        get_frame(ip)
        people_num, obstacles = count_objects.detect()
        print("프레임 저장 완료")
        
        # 정확한 시간 계산을 위해 실행 시간을 계산
        exec_time = time.time() - start_time
        wait_time = delay_time - exec_time
        
        # 위험 단계 계산
        alert_level, crowd_density = get_alert_level(total_area, people_num)
        
        # DB로 값을 저장해준다
        write_to_db(crowd_density, alert_level)
        print("위험 단계 :", alert_level)

        print("실행 시간: %.2f초" % exec_time)
        print("대기 시간: %.2f초" % wait_time)
        print("===========================================")
        
        # ==============
        
        # 실행 시간을 제외한 시간동안 기다린다
        time.sleep(delay_time)


if __name__ == '__main__':
    main()
