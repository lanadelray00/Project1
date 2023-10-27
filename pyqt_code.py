import cv2, imutils
import platform
import flask
import csv
import sys
import time
import mysql.connector
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from flask import request
from flask import Response
from flask import stream_with_context
import datetime
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow
import numpy as np
import serial

## webCam test
# src = 0
# if platform.system() == 'Windows' :
#     cap = cv2.VideoCapture( src , cv2.CAP_DSHOW )
    
# else :
#     cap = cv2.VideoCapture( src )
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
# while cap.isOpened():
    
#     (grabbed, frame) = cap.read()
    
#     if grabbed:
#         cv2.imshow('Wandlab Camera Window', frame)
 
#         key = cv2.waitKey(1) & 0xFF
#         if (key == 27): 
#             break
 
# cap.release()
# cv2.destroyAllWindows()

from_class = uic.loadUiType("GUI.ui")[0]


class getlogFromDB(QThread):
    update = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__()
        # self.main = VideoStreamGUI(self)
        # self.main = parent
        self.running = True
        self.update_f1 = None
        self.init_f1 = None
        self.update_f2 = None
        self.init_f2 = None
        self.conn = self.create_mysql_connection()
        cursor = self.conn.cursor()
        self.validate_date = 0
        self.validate_index = 0
        self.cnt = 0

    def create_mysql_connection(self):
        return mysql.connector.connect(
        host = 'database-1.cupwi98n8kxr.ap-northeast-2.rds.amazonaws.com',
        port = 3306,
        user = 'robot',
        password = '728778',
        database = 'amrbase'
    )


    # def testf2_mysql_connetion(self):


    def run(self):
        # count = 0
        while self.running == True:
            try:
                self.conn = self.create_mysql_connection()
                cursor = self.conn.cursor()
                    # SELECT * FROM iot_project WHERE timestamp_column = (SELECT MAX(timestamp_column) FROM iot_project
                # self.conn.commit()
                # result = cursor.fetchall()
                # for row in result:
                #     # 결과 처리
                #     print(row)
                # self.updatetable(cursor)
                # cursor.close()
                # print("Database connection is active.")
                if self.cnt == 0:
                    print(self.cnt)
                    self.inittable(cursor)
                    self.cnt = 1
                else:
                    self.updatetable(cursor)
                self.update.emit()
            except:
                print("Error Occured")
            time.sleep(1)  # 5초마다 데이터베이스 연결 상태 확인

    def inittable(self,cursor):
        cursor.execute('select * from iot_project_f1')
        result = cursor.fetchall()
        self.init_f1 = result # f1 데이터
        for row in result[:-1]:
            # 결과 처리
            print(row)    
        cursor.execute('select * from iot_project_f2')
        result = cursor.fetchall()
        self.init_f2 = result # f2 데이터    
        for row in result[:-1]:
        # 결과 처리
            print(row)    
            # self.Add(row)

    def updatetable(self,cursor):
        # cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM iot_project_f1 order by f1_timelog desc limit 1")
        result = cursor.fetchall()
        for row in result:
            # 결과 처리
            if row[2] != self.validate_date:
                # print(row)
                self.update_f1 = row
                # print(row)
                # self.Add(row)
                self.validate_date = row[2]
        # cursor.close()
        # self.conn = self.create_mysql_connection()
        # cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM iot_project_f2 order by f2_timelog desc limit 1")
        result = cursor.fetchall()
        for row in result:
            # 결과 처리
            if row[1] != self.validate_index:
                # print(row)
                self.update_f2 = row
                # print(row)
                # self.Add(row)
                self.validate_index = row[1]
        cursor.close()
        # self.conn.close()

    def Add(self,res):
            line = self.f1_log.rowCount()
            
            for each in res:
                self.f1_log.insertRow(line)
                self.f1_log.setItem(line, 0, QTableWidgetItem(str(each[0]) + '명'))
                self.f1_log.setItem(line, 1, QTableWidgetItem(self.inout[each[1]]))
                self.f1_log.setItem(line, 2, QTableWidgetItem(each[2]))
                self.f1_log.setItem(line, 3, QTableWidgetItem(self.mode[each[3]]))
                self.f1_log.setItem(line, 4, QTableWidgetItem(each[4]))

    def stop(self):
        self.running = False
        self.conn.cursor().close()
        self.conn.close()

class Camera(QThread):
    update = pyqtSignal()
    
    def __init__(self, sec=0, parent=None):
        super().__init__()

        self.main = parent
        self.running = True

    def run(self):
        # count = 0
        while self.running == True:
            self.update.emit()
            time.sleep(0.1)

    def stop(self):
        self.running = False


class VideoStreamGUI(QMainWindow, from_class):
    def __init__(self, parent = None):
        super().__init__()
        self.setupUi(self)
        # self.update_f1 = None
        # self.init_f1 = None
        self.isCameraOn = False
        self.isRecStart = False
        self.dbmonitor = getlogFromDB(self)
        self.dbmonitor.daemon = True
        self.dbmonitor.start()
        self.validate_date = 0
        self.inout = {1:'in',2:'out'}
        self.mode = {0:'Auto', 1:'manual'}
        self.init = 0
        # self.cnt = 0
        # self.now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.fps = 10

        # date 초기값 설정
        # self.date_start.setDate()


        self.logsave_f1.clicked.connect(self.save_f1_data_to_csv)
        self.logsave_f2.clicked.connect(self.save_f2_data_to_csv)
        self.pixmap1 = QPixmap()
        self.log_frame.setPixmap(self.pixmap1)
        self.pixmap2 = QPixmap()
        self.now_frame.setPixmap(self.pixmap2)
        self.logsave_f1.hide()
        self.logsave_f2.hide()
        self.camera = Camera(self)
        self.camera.daemon = True
        
        # self.Add1(self.dbmonitor.init_f1)
        # self.dbmonitor.update.connect()
        self.f1_log.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.f2_log.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.record = Camera(self)
        self.record.daemon = True


        self.shot.hide()
        self.RecordStart.hide()
        self.RecordStop.hide()
        self.cnt = 0
        self.cap = None
        self.Camonoff.setText('Cam on')
        self.f1_button.clicked.connect(self.f1_select)
        self.f2_button.clicked.connect(self.f2_select)
        self.camera.update.connect(self.updateCamera)
        self.record.update.connect(self.updateRecording)
        # if self.cnt == 0:
        #     self.dbmonitor.update.connect(self.init_f1_add)
        #     # self.dbmonitor.update.connect(self.Add2)
        #     self.cnt += 1
        # else:
        #     self.dbmonitor.update.connect(self.update_f1_add)
        self.Camonoff.clicked.connect(self.clickCamera)
        self.RecordStart.clicked.connect(self.clickRecord)
        self.RecordStop.clicked.connect(self.clickRecord)
        self.shot.clicked.connect(self.capture)
        self.openFile.clicked.connect(self.searchFile)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.resetDB_f1.clicked.connect(self.Question_f1)
        self.resetDB_f2.clicked.connect(self.Question_f2)
        self.Search_f1.clicked.connect(self.setdateRange_f1)
        self.Search_f2.clicked.connect(self.setdateRange_f2)
        self.dbmonitor.update.connect(self.dbtotable)

    


    def dbtotable(self):
        if self.init == 0:
            self.init_f1_add()
            self.init_f2_add()
            self.init += 1
            # print(self.init)
        else:
            self.update_f1_add()
            self.update_f2_add()
            # print(self.init)

    def init_f1_add(self):
        self.Add1_init(self.dbmonitor.init_f1)

    def update_f1_add(self):
        self.Add1_update(self.dbmonitor.update_f1)

    def init_f2_add(self):
        self.Add2_init(self.dbmonitor.init_f2)

    def update_f2_add(self):
        self.Add2_update(self.dbmonitor.update_f2)

    def qdate2int(self,date):
        return date.date().year() * 10e+10 + date.date().month() *10e+8 + date.date().day()*10e+6 + date.time().hour()*10000 + date.time().minute()*100 + date.time().second()
    
    def str2int(self,date):
        return int(date[:4])*10e+10 + int(date[5:7])*10e+8 + int(date[8:10])*10e+6 + int(date[11:13])*10e+4 + int(date[14:16])*10e+2 + int(date[17:19])

    # 조건에 따라 행을 필터링하는 함수를 정의합니다.
    def filter_rows(self,condition,table_widget):
        for row in range(table_widget.rowCount()):
            item = table_widget.item(row, 2)  # 조건이 나이 열을 기반으로 한다고 가정 (열 인덱스 2)
            if item is not None:
                each = item.text()
                if condition(self.str2int(each)):
                    table_widget.setRowHidden(row, False)
                else:
                    table_widget.setRowHidden(row, True)

    def setdateRange_f2(self):
        start = self.qdate2int(self.date_start.dateTime())
        end = self.qdate2int(self.date_end.dateTime())
        self.condition = lambda date : date >= start and date <= end
        # print(start)
        self.filter_rows(self.condition, self.f2_log)

    def setdateRange_f1(self):
        start = self.qdate2int(self.date_start.dateTime())
        end = self.qdate2int(self.date_end.dateTime())
        self.condition = lambda date : date >= start and date <= end
        # print(start)
        self.filter_rows(self.condition, self.f1_log)
        
        # condition = lambda date : date.st
    def save_f2_data_to_csv(self):
        self.now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(self.now + '_f1.csv' , 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            table_widget = self.f2_log
            for row in range(table_widget.rowCount()):
                row_data = []
                for column in range(table_widget.columnCount()):
                    item = table_widget.item(row, column)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append('')  # 빈 셀은 빈 문자열로 저장
                csv_writer.writerow(row_data)

    def save_f1_data_to_csv(self):
        self.now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(self.now + '_f1.csv' , 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            table_widget = self.f1_log
            for row in range(table_widget.rowCount()):
                row_data = []
                for column in range(table_widget.columnCount()):
                    item = table_widget.item(row, column)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append('')  # 빈 셀은 빈 문자열로 저장
                csv_writer.writerow(row_data)


    def Add2_update(self,res):
        line = self.f2_log.rowCount()
        try:
            if res[1] != self.past_validate_index:
                # print(res)
                self.f2_log.insertRow(0)
                self.f2_log.setItem(0, 0, QTableWidgetItem(res[0]))
                self.f2_log.setItem(0, 1, QTableWidgetItem(res[1]))
                self.f2_log.setItem(0, 2, QTableWidgetItem(res[2]))
                self.f2_log.setItem(0, 3, QTableWidgetItem(res[3]))
                self.f2_log.setItem(0, 4, QTableWidgetItem(res[4]))
                self.f2_log.setItem(0, 5, QTableWidgetItem(res[5]))
                self.f2_log.setItem(0, 6, QTableWidgetItem(str(res[6]))) 
                self.past_validate_index = res[1] 
        except:
            pass

    def Add2_init(self,res):
        line = self.f2_log.rowCount()
        # self.past_validate_date = res[0][2]
        for each in res:
            # print(res)
        # self.Add(row)
            self.f2_log.insertRow(line)
            self.past_validate_index = each[1]
            self.f2_log.setItem(line, 0, QTableWidgetItem(each[0]))
            self.f2_log.setItem(line, 1, QTableWidgetItem(each[1]))
            self.f2_log.setItem(line, 2, QTableWidgetItem(each[2]))
            self.f2_log.setItem(line, 3, QTableWidgetItem(each[3]))
            self.f2_log.setItem(line, 4, QTableWidgetItem(each[4]))
            self.f2_log.setItem(line, 5, QTableWidgetItem(each[5]))
            self.f2_log.setItem(line, 6, QTableWidgetItem(str(each[6])))

    def Add1_update(self,res):
        line = self.f1_log.rowCount()
        # try:
        if res[2] != self.past_validate_date:
            # print(res)
            self.f1_log.insertRow(0)
            self.f1_log.setItem(0, 0, QTableWidgetItem(str(res[0]) + '명'))
            self.f1_log.setItem(0, 1, QTableWidgetItem(self.inout[res[1]]))
            self.f1_log.setItem(0, 2, QTableWidgetItem(res[2]))
            self.f1_log.setItem(0, 3, QTableWidgetItem(self.mode[res[3]]))
            self.f1_log.setItem(0, 4, QTableWidgetItem(res[4]))   
            self.past_validate_date = res[2] 
        # except:
        #     pass


    def Add1_init(self,res):
        line = self.f1_log.rowCount()
            # self.past_validate_date = res[0][2]
        for each in res:
            # print(res)
        # self.Add(row)
            self.f1_log.insertRow(line)
            self.past_validate_date = each[2]
            self.f1_log.setItem(line, 0, QTableWidgetItem(str(each[0]) + '명'))
            self.f1_log.setItem(line, 1, QTableWidgetItem(self.inout[each[1]]))
            self.f1_log.setItem(line, 2, QTableWidgetItem(each[2]))
            self.f1_log.setItem(line, 3, QTableWidgetItem(self.mode[each[3]]))
            self.f1_log.setItem(line, 4, QTableWidgetItem(each[4]))

    def searchFile(self):
        try:
            file = QFileDialog.getOpenFileName(filter='Image (*.*)')
            if file[0][-3:] == 'avi':
                self.cap = cv2.VideoCapture(file[0])
                if not self.cap.isOpened():
                    return
                self.timer.start(1000//self.fps)
            elif file[0][-3:] == 'png' or file[0][-3:] == 'jpg': # 사진
                file = QFileDialog.getOpenFileName(filter='Image (*.*)')
                image = cv2.imread(file[0])
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                h,w,c = image.shape
                qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)

                self.pixmap1 = self.pixmap1.fromImage(qimage)
                self.pixmap1 = self.pixmap1.scaled(self.log_frame.width(), self.log_frame.height())

                self.log_frame.setPixmap(self.pixmap1)            
            else:
                QFileDialog.close()
        except Exception as e:
            pass

    def Question_f1(self):
        retval = QMessageBox.question(self, "DB 및 테이블 전체 삭제",
                             '정말 삭제하시겠습니까? - 복구 불가능!', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if retval == QMessageBox.Yes:
            self.resetdb_f1()
        # else:
            # QMessageBox.close()   

    def Question_f2(self):
        retval = QMessageBox.question(self, "DB 및 테이블 전체 삭제",
                             '정말 삭제하시겠습니까? - 복구 불가능!', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if retval == QMessageBox.Yes:
            self.resetdb_f2()

    def resetdb_f1(self):
        self.conn = self.dbmonitor.create_mysql_connection()
        cursor = self.conn.cursor()
        cursor.execute("delete from iot_project_f1")
        self.conn.commit()
        self.f1_log.setRowCount(0)

    def resetdb_f2(self):
        self.conn = self.dbmonitor.create_mysql_connection()
        cursor = self.conn.cursor()
        cursor.execute("delete from iot_project_f2")
        self.conn.commit()
        self.f2_log.setRowCount(0)

    def update_frame(self):
        if self.cap is not None:
                    # self.isCameraOn = False
                    ret, frame = self.cap.read()
                    if ret:
                        height, width, channel = frame.shape
                        bytes_per_line = 3 * width
                        qt_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

                        self.pixmap1 = QPixmap.fromImage(qt_image)
                        self.log_frame.setPixmap(self.pixmap1)
        else:
            self.cap.release()

    def openFile_camera(self):
        file = QFileDialog.getOpenFileName(filter='Image (*.*)')
        image = cv2.imread(file[0])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h,w,c = image.shape
        qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)

        self.pixmap2 = self.pixmap2.fromImage(qimage)
        self.pixmap2 = self.pixmap2.scaled(self.log_frame.width(), self.log_frame.height())

        self.log_frame.setPixmap(self.pixmap2)

    def capture(self):
        self.now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.now + '.png'
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(filename, image)

    def updateRecording(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.writer.write(image)

    def clickRecord(self):
        if self.isRecStart == False:
            # self.btnRecord.setText('Rec RecordStop')
            self.RecordStop.show()
            self.RecordStart.hide()
            self.isRecStart = True

            self.recordingStart()

        else:
            # self.btnRecord.setText('Rec RecordStart')
            self.RecordStop.hide()
            self.RecordStart.show()
            self.isRecStart = False

            # self.cameraStop()
            self.recordingStop()

    def recordingStart(self):
        self.record.running = True
        self.record.start()

        self.now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.now + '.avi'
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

        w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.writer = cv2.VideoWriter(filename, self.fourcc, 20.0, (w, h))

    def clickCamera(self):
                if self.isCameraOn == False:
                    self.Camonoff.setText('Cam off')
                    self.isCameraOn = True
                    self.RecordStart.show()
                    self.RecordStop.hide()
                    self.shot.show()

                    self.cameraStart()
                else:
                    self.Camonoff.setText('Cam on')
                    self.isCameraOn = False
                    self.RecordStart.hide()
                    self.RecordStop.hide()
                    self.shot.hide()

                    self.cameraStop()
                    self.recordingStop()

    def recordingStop(self):
        self.record.running = False

        if self.isRecStart == True:
            self.writer.release()

    def cameraStart(self):
        self.camera.running = True
        self.camera.start()
        self.video = cv2.VideoCapture(-1)

    def cameraStop(self):
        self.camera.running = False
        self.camera.stop()
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        h,w,c = image.shape
        
        self.qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)
        self.qimage.fill(QColor(0, 0, 0))
        self.pixmap2 = self.pixmap2.fromImage(self.qimage)
        self.qimage.fill(QColor(0, 0, 0))
        self.now_frame.setPixmap(self.pixmap2)
        # self.count = 0
        
        self.video.release()

    def updateCamera(self):
        # self.label.setText('Camera Running : ' + str(self.count))
        # self.count += 1

        retval, image = self.video.read()

        if retval:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            h,w,c = image.shape
            self.qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)
            
            self.image = image
            self.pixmap2 = self.pixmap2.fromImage(self.qimage)
            self.pixmap2 = self.pixmap2.scaled(self.now_frame.width(), self.now_frame.height())

            self.now_frame.setPixmap(self.pixmap2)

    def stop(self):
        self.running = False

    def f1_select(self):
        if self.f1_log.rowCount() == 0:
            self.logsave_f1.hide()
            self.logsave_f2.hide()
            self.resetDB_f1.show()
        else:
            self.logsave_f1.show()
            self.resetDB_f2.hide()
        self.f1_log.show()
        self.f2_log.hide()
        self.Search_f1.show()
        self.Search_f2.hide()

    def f2_select(self):
        if self.f2_log.rowCount() == 0:
            self.logsave_f1.hide()
            self.logsave_f2.hide()
            self.resetDB_f2.show()
        else:
            self.logsave_f2.show()
            self.resetDB_f1.hide()
        self.f2_log.show()
        self.f1_log.hide()
        self.Search_f2.show()
        self.Search_f1.hide()

        # if self.f1_log.rowCount() == 0:
        #     self.logsave_f1.hide()
        # else:
        #     if self.f2_log.rowCount() == 0:
        #         self.logsave_f2.hide()
        #     else:
        #         self.logsave_f2.show()
        
def main():
    app = QApplication(sys.argv)
    window = VideoStreamGUI()
    window.show()
    sys.exit(app.exec_())
    # while True:
    #     ret, frame = cap.read()
    #     if not ret:
    #         break

    #     # frame을 PyQt GUI에 업데이트
    #     window.set_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


if __name__ == '__main__':
    main()

