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

# '------------------변수 선언-------------------'
# f2_id = 0  # 몇번째 인식인지 알려주는 id
f2_index = 0  # 인덱스
danger_distance = 5  # 접근 금지 거리[cm]
filter_sec = 3  # 해당 초 내에 다시 감지되는 경우 같은 경우로 인지
now = datetime.now()

from_class = uic.loadUiType("pyqt_kcm.ui")[0]

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

        self.pushButton.clicked.connect(self.Send)
        self.serial.receive.connect(self.Recv)
        
    def Send(self):
        text = self.lineEdit.text()
        text += "\n"
        self.ardu.write(text.encode())

        #if self.conn.readable():
        #    res = self.conn.readline()
        #    self.textEdit.append(res.decode())

    def Recv(self, message):
        self.textEdit.append(message)


class SerialManager(QThread):
    receive = pyqtSignal(str)

    def __init__(self, serial=None):
        super().__init__()
        self.serial = serial
        self.running = True
        self.f2_id = 0

    def run(self):
        self.remote = self.Connect()
        self.cur = self.remote.cursor(buffered=True)
        while self.running == True:
            if self.serial.readable():
                self.read_arduino_safitysensor()

    def stop(self):
        self.running = False

    def read_arduino_safitysensor(self):
        global f2_index, now
        # if self.serial.readable():
        try:
            # 시리얼 모니터 출력 값
            serial_data = self.serial.readline()
            serial_data = serial_data.decode()[:len(serial_data)-2]
            # print(serial_data)

            self.receive.emit(str(serial_data))

            if serial_data.find("Distance") > -1:  # "\nDistance: "로 시리얼 프린트하므로 split
                
                # self.receive.emit(str(serial_data))
                
                f2_dist_1 = int(serial_data.split(":")[1])  # 초음파 거리값[cm]
                f2_dist_2 = int(serial_data.split(":")[2])
                f2_stepmotor_angle = float(serial_data.split(":")[3])
                # print(f2_dist_1)

                if (f2_dist_1 <= danger_distance) or (f2_dist_2 <= danger_distance):  # 테스트를 위해 임의로 5[cm]로 지정
                    
                    if f2_index == 0:
                        self.f2_id += 1
                    
                    print(f2_index)

                    now = datetime.now()
                    f2_timelog = str(now.strftime('%Y-%m-%d %H:%M:%S'))
                    print('접근시간: ', now)

                    query_2 = "insert into iot_project_f2 (f2_id, f2_index, f2_dist_1, f2_dist_2, f2_timelog, f2_stepmotor_angle) values (%s, %s, %s, %s, %s, %s);"
                    self.cur.execute(query_2, ((self.f2_id, f2_index, f2_dist_1, f2_dist_2, f2_timelog, f2_stepmotor_angle)))
                    self.remote.commit()
                    
                    # DB에 잘 insert되었는지 터미널에 프린트
                    query_3 = "select * from iot_project_f2 order by f2_timelog desc limit 1;"
                    self.cur.execute(query_3)

                    result = self.cur.fetchall()
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
                        f2_index = 0

        except Exception as ex:
            print(ex)
            pass
    
    def Connect(self):
        return mysql.connector.connect(
        # host = "database-1.cn4fdtxirel2.ap-northeast-2.rds.amazonaws.com",
        # port = 3306,
        # user = "robot",
        # password = '1234',
        # database = "armbase"
        host = 'database-1.cupwi98n8kxr.ap-northeast-2.rds.amazonaws.com',
        port = 3306,
        user = 'robot',
        password = '728778',
        database = 'amrbase'
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec())