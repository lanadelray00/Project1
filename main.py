import mysql.connector
import threading
import sqlite3
import time
import datetime as dt
import serial
import time
from datetime import datetime
# 테이블: 인덱스, 시간 추가

# MySQL 연결 설정
def create_mysql_connection():
    return mysql.connector.connect(
    host = 'database-1.cupwi98n8kxr.ap-northeast-2.rds.amazonaws.com',
    port = 3306,
    user = 'robot',
    password = '728778',
    database = 'amrbase'
)


# 쿼리 실행 함수
'''
IoT에서 파이썬으로 받은
인원 수, 출입 여부 랑 받은 시점에 생성하는 현재 날짜 및 시간 (datetime 사용) 등등을 db에 저장.
(영상을 저장하는 쿼리는 따로 작성 예정) 

----
추가 예정
check in, check out이 1 이 될때만 
'''


# def tempSpace():
    # check_in or check_out이 1이 들어오면 tempSpace queue에 저장
    # f1_execute_query_nonvideo 업데이트 시 저장된 데이터들을 모두 전달해줌. 이때, queue는 전부 clear.
    
    
def f1_execute_query_nonvideo(connection, f1_count, f1_inout, f1_timelog, f1_gate_mode, f1_message, f1_index):
    global dbon, check_in, check_out
    cursor = connection.cursor()
    while dbon:
        # 'COM3' 부분에 환경에 맞는 포트 입력
        ser = serial.Serial('/dev/ttyACM0', 9600)
        while ser:
            if ser.readable():
                val = ser.readline()
                parts = val.strip().split()
                for i in range(len(parts)):
                    parts[i] = str(parts[i]).replace("b'", "").replace("'", "")
                if len(parts) == 3:
                    f1_count, check_in, check_out = parts[0], parts[1], parts[2]
                    print(parts[0], parts[1], parts[2]) 
                if check_in == '1' or check_out == '1':
                    print('Change!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    sql_insert = "insert into iot_project (f1_count, f1_inout, f1_timelog, f1_gate_mode, f1_message, f1_index) value (%s, %s, %s, %s, %s, %s)"
                    if check_in == '1':
                        f1_inout = 1
                    elif check_out == '1':
                        f1_inout = 2
                    
                    current_time = datetime.now()
                    f1_timelog = current_time.strftime("%Y-%m-%d %H:%M:%S")
                    
                    cursor.execute(sql_insert, (f1_count, f1_inout, f1_timelog, f1_gate_mode, f1_message, f1_index))
                    f1_index += 1
                    connection.commit()
                    
                    cursor.execute("SELECT * FROM iot_project")
                    result = cursor.fetchall()
                    for row in result:
                        # 결과 처리
                        print(row)
            # time.sleep(1)  # 1초마다 쿼리 실행
            
    # cursor.close()
    # connection.close()

connection = create_mysql_connection()
dbon = True
check_in = 0
check_out = 0

f1_count = 0
f1_inout = 0
f1_timelog = 0
f1_gate_mode = 0
f1_message = 'message'
f1_index = 0

query_thread = threading.Thread(target=f1_execute_query_nonvideo,args=(connection, f1_count, f1_inout, f1_timelog, f1_gate_mode, f1_message, f1_index))
query_thread.start()
