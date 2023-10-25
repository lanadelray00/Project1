import serial
import mysql.connector
import threading
import datetime import datetime

now = datetime.now()

# '-------아두이노와 통신-------'
ardu = serial.Serial(port='/dev/ttyACM0', baudrate=9600,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     bytesize=serial.EIGHTBITS)
# ardu = serial.Serial('/dev/ttyACM0', 9600, timeout=0.1)

# '-------DB 연결-------'
# def Connect():
#     return mysql.connector.connect(
#     host = "database-1.cn4fdtxirel2.ap-northeast-2.rds.amazonaws.com",
#     port = 3306,
#     user = "robot",
#     password = '1234',
#     database = "armbase"
#     )

# remote = Connect()
# cur = remote.cursor(buffered=True)
# query = "create table iot_project(f2_dist int, f2_timelog varchar(64), f2_video LONGBLOB, f2_timelog_end varchar(64), f2_motor_angle int);"
# cur.execute(query)

# '-------f2_dist, f2_timelog------'
def read_arduino_safitysensor():
    if ardu.readable():
        try:
            # 시리얼 모니터 출력 값
            serial_data = ardu.readline()
            # print(serial_data)
            serial_data = serial_data.decode()[:len(serial_data)-2]
            # print(serial_data)
            if serial_data.find("Distance") > -1:  # "\nDistance: "로 시리얼 프린트하므로 split
                # print(serial_data.split(":"))
                f2_dist = int(serial_data.split(":")[1])  # 초음파 거리값[cm]
                print(f2_dist)
                if f2_dist <= 5:  # 테스트를 위해 임의로 5[cm]로 지정
                    f2_timelog = now.strftime('%Y-%m-%d %H:%M:%S')
                    print(f2_timelog)
                    # f2_video = 
                    # f2_timelog_end = 
                    # f2_motor_angle = 

                    # query_2 = "insert into iot_project (f2_dist, f2_timelog, f2_video, f2_timelog_end, f2_motor_angle) values (%s, %s, 0, 0, 0)"
                    # cur.execute(query_2, tuple(f2_dist, f2_timelog))
                    
                    # # DB에 잘 insert되었는지 터미널에 프린트
                    # result = cur.fetchall()
                    # for row in result:
                    #     print(row)

                # cur.close()

        except Exception as ex:
            # print(ex)
            pass

insertdb_arduino_run = threading.Thread(target=read_arduino_safitysensor)
insertdb_arduino_run.start()