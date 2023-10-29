from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from serial import Serial
import mysql.connector
import sys
import threading
from datetime import datetime
import time
import sqlite3
import pandas as pd

# '------------------변수 선언-------------------'
f1_hist_index = 0
f1_warning_index = 0
f1_gate = 'D'

dbon = True
check_in = 0
check_out = 0

f1_count = 0
f1_inout = 0
f1_timelog = 0
f1_gate_mode = 0
f1_message = 'message'
f1_index = 0

now = datetime.now()

from_class = uic.loadUiType("GUI.ui")[0]

class WindowClass(QMainWindow, from_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # '----------------아두이노와 통신----------------'
        # self.ardu = Serial(port='/dev/ttyACM0', baudrate=9600,
        #                    parity=serial.PARITY_NONE,
        #                    stopbits=serial.STOPBITS_ONE,
        #                    bytesize=serial.EIGHTBITS)
        self.ardu = Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)  # 접속 대기
        self.serial = SerialManager(self.ardu)
        self.serial.start()

        self.pushButton_g1_open.clicked.connect(self.Send)
        self.pushButton_g1_close.clicked.connect(self.Send)
        self.pushButton_g2_open.clicked.connect(self.Send)
        self.pushButton_g2_close.clicked.connect(self.Send)
        self.serial.receive.connect(self.Recv)

    def Send(self):
        sending_button = self.sender()

        if sending_button == self.pushButton_g1_open:
            text = 'a'

        elif sending_button == self.pushButton_g1_close:
            text = 'b'

        elif sending_button == self.pushButton_g2_open:
            text = 'c'

        elif sending_button == self.pushButton_g2_close:
            text = 'd'
        
        text += "\n"
        self.ardu.write(text.encode())

    def printEmp(self, f1_uid):
        global f1_hist_index, f1_warning_index, f1_gate
        now = datetime.now()
        f1_timelog = str(now.strftime('%Y-%m-%d %H:%M:%S'))
        
        self.Connect()
        f1_type = f1_uid.split(":")[0]
        f1_uid = f1_uid.split(":")[1]

        query_last = "';"
        query_1 = "select * from iot_project_f1_emp where 보안출입증_ID = '" + str(f1_uid) + query_last
        # self.label.setText(query_1)
        self.cur.execute(query_1)
        self.result_query_1 = self.cur.fetchall()
        # for row in result:
        #     print(row)

        self.df_result_query_1 = pd.DataFrame(self.result_query_1)

        self.tableWidget_2.setRowCount(len(self.df_result_query_1))
        self.tableWidget_2.clearContents()

        for x in range(len(self.df_result_query_1)):
            사원번호, 부서번호, 직급, 이름, 성별, 입사일자, 보안출입증_ID = self.df_result_query_1.iloc[x, :]
            self.tableWidget_2.setItem(x, 0, QTableWidgetItem(str(사원번호)))
            self.tableWidget_2.setItem(x, 1, QTableWidgetItem(str(부서번호)))
            self.tableWidget_2.setItem(x, 2, QTableWidgetItem(str(직급)))
            self.tableWidget_2.setItem(x, 3, QTableWidgetItem(str(이름)))
            self.tableWidget_2.setItem(x, 4, QTableWidgetItem(str(성별)))
            self.tableWidget_2.setItem(x, 5, QTableWidgetItem(str(입사일자)))
            self.tableWidget_2.setItem(x, 6, QTableWidgetItem(str(보안출입증_ID)))

        f1_empnum = int(self.df_result_query_1[0][0])

        if f1_type == "Warning":
            f1_warning_index += 1
            query_2 = "insert into iot_project_f1_warning (순번, 사원번호, 보안출입증_ID, timelog, 출입문) values (%s, %s, %s, %s, %s);"
            self.cur.execute(query_2, ((f1_warning_index, f1_empnum, f1_uid, f1_timelog, f1_gate)))
            self.remote.commit()

            self.query_3 = "select * from iot_project_f1_warning order by timelog desc;"

            self.cur.execute(self.query_3)
            self.result_query_2 = self.cur.fetchall()
            self.df_result_query_2 = pd.DataFrame(self.result_query_2)

            self.tableWidget_3.setRowCount(len(self.df_result_query_2))
            self.tableWidget_3.clearContents()

            for x in range(len(self.df_result_query_2)):
                순번, 사원번호, 보안출입증_ID, timelog, 출입문 = self.df_result_query_2.iloc[x, :]
                self.tableWidget_3.setItem(x, 0, QTableWidgetItem(str(순번)))
                self.tableWidget_3.setItem(x, 1, QTableWidgetItem(str(사원번호)))
                self.tableWidget_3.setItem(x, 2, QTableWidgetItem(str(보안출입증_ID)))
                self.tableWidget_3.setItem(x, 3, QTableWidgetItem(str(timelog)))
                self.tableWidget_3.setItem(x, 4, QTableWidgetItem(str(출입문)))

        elif f1_type == 'In':
            f1_hist_index += 1
            query_2 = "insert into iot_project_f1_hist (순번, 사원번호, 보안출입증_ID, timelog_in, 출입문) values (%s, %s, %s, %s, %s);"
            self.cur.execute(query_2, ((f1_hist_index, f1_empnum, f1_uid, f1_timelog, f1_gate)))
            self.remote.commit()

            self.query_3 = "select * from iot_project_f1_hist order by timelog_in desc;"

        elif f1_type == 'Out':
            query_2 = "update iot_project_f1_hist set timelog_out='" +  f1_timelog + "' order by timelog_in desc limit 1;"
            self.cur.execute(query_2)
            self.remote.commit()

            self.query_3 = "select * from iot_project_f1_hist order by timelog_in desc;"

        if f1_type == 'In' or f1_type == 'Out':
            self.cur.execute(self.query_3)
            self.result_query_2 = self.cur.fetchall()
            self.df_result_query_2 = pd.DataFrame(self.result_query_2)

            self.tableWidget.setRowCount(len(self.df_result_query_2))
            self.tableWidget.clearContents()

            for x in range(len(self.df_result_query_2)):
                순번, 사원번호, 보안출입증_ID, timelog_in, timelog_out, 출입문 = self.df_result_query_2.iloc[x, :]
                self.tableWidget.setItem(x, 0, QTableWidgetItem(str(순번)))
                self.tableWidget.setItem(x, 1, QTableWidgetItem(str(사원번호)))
                self.tableWidget.setItem(x, 2, QTableWidgetItem(str(보안출입증_ID)))
                self.tableWidget.setItem(x, 3, QTableWidgetItem(str(timelog_in)))
                self.tableWidget.setItem(x, 4, QTableWidgetItem(str(timelog_out)))
                self.tableWidget.setItem(x, 5, QTableWidgetItem(str(출입문)))

        self.remote.close()

    def Connect(self):
        self.remote = mysql.connector.connect(
        host = "database-1.cn4fdtxirel2.ap-northeast-2.rds.amazonaws.com",
        port = 3306,
        user = "robot",
        password = '1234',
        database = "armbase"
        # host = 'database-1.cupwi98n8kxr.ap-northeast-2.rds.amazonaws.com',
        # port = 3306,
        # user = 'robot',
        # password = '728778',
        # database = 'amrbase'
        )
        self.cur = self.remote.cursor(buffered=True)

    def Recv(self, message):
        self.textEdit.append(message)
        # self.printEmp(message)


class SerialManager(QThread):
    receive = pyqtSignal(str)

    def __init__(self, serial=None):
        super().__init__()
        self.serial = serial
        self.running = True
        self.f1_uid = None
        self.remote = self.Connect()
        self.cur = self.remote.cursor(buffered=True)

    def run(self):
        while self.running == True:
            if self.serial.readable():
                self.f1_execute_query_nonvideo(f1_count, f1_inout, f1_timelog, f1_gate_mode, f1_message, f1_index)

    def stop(self):
        self.running = False

    def f1_execute_query_nonvideo(self, f1_count, f1_inout, f1_timelog, f1_gate_mode, f1_message, f1_index):
        global dbon, check_in, check_out
        try:
            # 시리얼 모니터 출력 값
            serial_data = self.serial.readline().decode()
            parts = serial_data.strip().split()
            self.receive.emit(str(parts))

            if serial_data.find("peopleCount") > -1:
                print(parts)
                f1_count, check_in, check_out = parts[1], parts[2], parts[3]
                # print(parts[1], parts[2], parts[3]) 
                
                if check_in == '1' or check_out == '1':
                    # print('Change!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    
                    if check_in == '1':
                        f1_inout = 1
                    elif check_out == '1':
                        f1_inout = 2
                    
                    current_time = datetime.now()
                    f1_timelog = current_time.strftime("%Y-%m-%d %H:%M:%S")

                    sql_insert = "insert into iot_project_f1 (f1_count, f1_inout, f1_timelog, f1_gate_mode, f1_message, f1_index) value (%s, %s, %s, %s, %s, %s)"
                    self.cur.execute(sql_insert, (f1_count, f1_inout, f1_timelog, f1_gate_mode, f1_message, f1_index))
                    f1_index += 1
                    self.remote.commit()

                    # DB에 잘 insert되었는지 터미널에 프린트
                    query_checking = "select * from iot_project_f1 order by f1_timelog desc limit 1;"
                    self.cur.execute(query_checking)

                    result = self.cur.fetchall()
                    for row in result:
                        print(row)
                    
            if (serial_data.find("In") > -1) or (serial_data.find("Out") > -1) or (serial_data.find("Warning") > -1):
                f1_uid = str(serial_data)[:-2]
                # print(f1_uid)
                # self.receive.emit(f1_uid)

        except Exception as ex:
            print(ex)
            pass
    
    def Connect(self):
        return mysql.connector.connect(
        host = "database-1.cn4fdtxirel2.ap-northeast-2.rds.amazonaws.com",
        port = 3306,
        user = "robot",
        password = '1234',
        database = "armbase"
        # host = 'database-1.cupwi98n8kxr.ap-northeast-2.rds.amazonaws.com',
        # port = 3306,
        # user = 'robot',
        # password = '728778',
        # database = 'amrbase'
    )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec())