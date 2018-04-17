#!/usr/bin/python
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import psutil
def GetCpu_usage():
    cpuv = psutil.cpu_percent()
    return cpuv

def memory_usage_psutil():
    mem = psutil.virtual_memory()
    used = mem.percent
    return used



