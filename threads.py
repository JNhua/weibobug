# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from sinablog import *

#继承 QThread 类
class BigWorkThread(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal()
    def __init__(self, mainurl, maxcount, needimg, parent=None):
        super(BigWorkThread, self).__init__(parent)
        self.mainurl = mainurl
        self.maxcount = maxcount
        self.needimg = needimg

    def run(self):
        spiderwork(self.mainurl, self.maxcount, self.needimg)
        self.finishSignal.emit()
