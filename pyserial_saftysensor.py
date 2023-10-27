import serial
import mysql.connector
import threading
from datetime import datetime
import time

# '----------------아두이노와 통신----------------'
# ardu = serial.Serial(port='/dev/ttyACM0', baudrate=9600,
#                      parity=serial.PARITY_NONE,
#                      stopbits=serial.STOPBITS_ONE,
#                      bytesize=serial.EIGHTBITS)
ardu = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # 접속 대기

# '-------------------DB 연결-------------------'
def Connect():
    return mysql.connector.connect(
    host = 'database-1.cupwi98n8kxr.ap-northeast-2.rds.amazonaws.com',
    port = 3306,
    user = 'robot',
    password = '728778',
    database = 'amrbase'
    )

# '---------------데이터테이블 생성----------------'
# remote = Connect()
# cur = remote.cursor(buffered=True)
# query_create_table = "create table iot_project_f2(f2_id int, f2_index int, f2_dist_1 int, f2_dist_2 int, f2_timelog varchar(64), f2_video LONGBLOB, f2_stepmotor_angle int);"
# cur.execute(query_create_table)

# '------------------변수 선언-------------------'
f2_id = 0  # 몇번째 인식인지 알려주는 id
f2_index = 0  # 인덱스
danger_distance = 5  # 접근 금지 거리[cm]
filter_sec = 3  # 해당 초 내에 다시 감지되는 경우 같은 경우로 인지
now = datetime.now()

# '--------f2_id, f2_index, f2_dist_1, f2_dist_2, f2_timelog, f2_stepmotor_angle--------'
def read_arduino_safitysensor():
    global f2_id, f2_index, now
    if ardu.readable():
        try:
            # 시리얼 모니터 출력 값
            serial_data = ardu.readline()
            serial_data = serial_data.decode()[:len(serial_data)-2]
            # print(serial_data)

            if serial_data.find("Distance") > -1:  # "\nDistance: "로 시리얼 프린트하므로 split
                f2_dist_1 = int(serial_data.split(":")[1])  # 초음파 거리값[cm]
                f2_dist_2 = int(serial_data.split(":")[2])
                f2_stepmotor_angle = float(serial_data.split(":")[3])
                # print(f2_dist_1)

                if (f2_dist_1 <= danger_distance) or (f2_dist_2 <= danger_distance):  # 테스트를 위해 임의로 5[cm]로 지정
                    print(f2_index)

                    now = datetime.now()
                    f2_timelog = str(now.strftime('%Y-%m-%d %H:%M:%S'))
                    print('접근시간: ', now)

                    query_2 = "insert into iot_project_f2 (f2_id, f2_index, f2_dist_1, f2_dist_2, f2_timelog, f2_stepmotor_angle) values (%s, %s, %s, %s, %s, %s);"
                    cur.execute(query_2, ((f2_id, f2_index, f2_dist_1, f2_dist_2, f2_timelog, f2_stepmotor_angle)))
                    remote.commit()
                    
                    # DB에 잘 insert되었는지 터미널에 프린트
                    query_3 = "select * from iot_project_f2 order by f2_timelog desc limit 1;"
                    cur.execute(query_3)

                    result = cur.fetchall()
                    for row in result:
                        print(row)

                    f2_index += 1
                    
                f2_timelog_last = now
                print('마지막 접근시간: ', f2_timelog_last)
                    
                if (f2_dist_1 > danger_distance) and (f2_dist_2 > danger_distance):
                    now_2 = datetime.now()
                    # print(now_2)
                    diff = now_2 - f2_timelog_last
                    print('경과시간: ', diff.seconds)
                    
                    if (diff.seconds > filter_sec):
                        f2_id += 1
                        f2_index = 0

        except Exception as ex:
            print(ex)
            pass

# '-------------양방향 통신 test------------'
# def flash():
#     while True:
#         cmd = input()
#         if cmd == "0":
#             ardu.write(b'L')
#         elif cmd == "1":
#             ardu.write(b'H')
#         elif cmd == "2":
#             ardu.write(b'L')
#             break
#         else:
#             print("0/1/2 입력")

# flash_run = threading.Thread(target=flash)
# flash_run.start()

# '-----------------실행------------------'
while True:
    remote = Connect()
    cur = remote.cursor(buffered=True)
    read_arduino_safitysensor()
    remote.close()

# insertdb_arduino_run = threading.Thread(target=read_arduino_safitysensor)
# insertdb_arduino_run.start()