import mysql.connector
import threading
import time
import datetime as dt

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


def f1_execute_query_nonvideo(connectionf1_count, f1_inout, f1_timelog, f1_gate_mode, f1_message):
    global dbon, state
    cursor = connection.cursor()
    while dbon:
        # if state != 'none':
        sql_insert = "insert into iot_project (f1_count, f1_inout, f1_timelog, f1_gate_mode, f1_message) value (%s, %s, %s, %s, %s)"
        cursor.execute(sql_insert, tuple(()))
        result = cursor.fetchall()

        for row in result:
            # 결과 처리
            print(row)
        # time.sleep(1)  # 1초마다 쿼리 실행
    cursor.close()
    connection.close()




connection = create_mysql_connection()

dbon = True
state = 'none'
query_thread = threading.Thread(target=f1_execute_query_nonvideo,args=(connection, f1_count, f1_inout, f1_timelog, f1_gate_mode, f1_message))

query_thread.start()



















# def sendQuery():
#     while dbon:
