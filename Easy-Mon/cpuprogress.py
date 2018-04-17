#!/usr/bin/python3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from emailconf import*
import sys
import easymon
import sysinfo
import genm
import time
import sqlite3
class MainUiClass(QtWidgets.QMainWindow,easymon.Ui_CPUinfo):
    def __init__(self, parent = None):
        super(MainUiClass, self).__init__(parent)
        self.setupUi(self)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda : self.cpu.setValue(sysinfo.GetCpu_usage()))
        self.timer.timeout.connect(lambda : self.memory.setValue(sysinfo.memory_usage_psutil()))
        self.timer.start(1000)
        self.threadclass = ThreadClass()
        self.threadclass.start()
        self.notifybutton.clicked.connect(self.emlopen)

    def emlopen(self):
        self.empwindow = QtWidgets.QWidget()
        self.ui = Ui_configuration()
        self.ui.setupUi(self.empwindow)
        self.empwindow.show()

class ThreadClass(QtCore.QThread):
    def __init__(self, parent = None):
        super(ThreadClass, self).__init__(parent)

    connection = sqlite3.connect("EASY.db", timeout=10)
    targt = connection.execute("SELECT * FROM TARGET")
    for elemnts in targt:
        target = elemnts[0]
        threshold = elemnts[1]
        sleep = elemnts[2]

    def run(self):
        self.memchk()

    def memchk(self):
        while 1:
            memval = sysinfo.memory_usage_psutil()
            if memval >= self.threshold:
                genm.SendMail()
                time.sleep(self.sleep)
            memval = sysinfo.memory_usage_psutil()
            cpval = sysinfo.GetCpu_usage()
            if cpval >= self.threshold:
                genm.SendMail()
                time.sleep(self.sleep)
            cpval = sysinfo.GetCpu_usage()

    def errormsg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Plese Configure Host and Target Information Properly")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()



if __name__ == '__main__':
    a = QtWidgets.QApplication(sys.argv)
    app = MainUiClass()
    app.show()
    a.exec_()
