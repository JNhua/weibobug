# -*- coding: utf-8 -*-
import pymysql
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from commentwindow import *
import datetime


class commentWindow(QMainWindow, Ui_commentwindow):
    def __init__(self):
        super(commentWindow, self).__init__()
        self.setupUi(self)
        self.conn = pymysql.connect("localhost", "root", "199659", "blog")
        self.conn.set_charset('utf8')
        self.cur = self.conn.cursor()
        self.conn.close()
        self.cur.close()
        self.sqlstring = "select * from comment where "

    def selectcomment_click(self):
        self.selectcomment.clicked.connect(self.selectcomment_click)
        self.conn = pymysql.connect("localhost", "root", "199659", "blog")
        self.conn.set_charset('utf8')
        self.cur = self.conn.cursor()
        temp_sqlstring = self.sqlstring
        is_first = True
        if self.authorcheck.isChecked():
            mystr = self.authortext.text()
            if not is_first:
                temp_sqlstring += "and "
            else:
                is_first = False
            if mystr.find("%") == -1:
                temp_sqlstring += "user = '" + self.authortext.text() + "'"
            else:
                temp_sqlstring += "user like '" + self.authortext.text() + "'"
        if self.bidcheck.isChecked():
            mystr = self.bidtext.text()
            if not is_first:
                temp_sqlstring += "and "
            else:
                is_first = False
            if mystr.find("%") == -1:
                temp_sqlstring += "bid = '" + self.bidtext.text() + "'"
            else:
                temp_sqlstring += "bid like '" + self.bidtext.text() + "'"
        if self.contentcheck.isChecked():
            mystr = self.contenttext.text()
            if not is_first:
                temp_sqlstring += "and "
            else:
                is_first = False
            if mystr.find("%") == -1:
                temp_sqlstring += "content = '" + self.contenttext.text() + "'"
            else:
                temp_sqlstring += "content like '" + self.contenttext.text() + "'"
        if self.timecheck.isChecked():
            if is_first:
                is_first = False
                temp_sqlstring += "pubtime between '" + self.timebegin.text() + "'" + \
                                  " and '" + self.timeend.text() + "'"
            else:
                temp_sqlstring += " and pubtime between '" + self.timebegin.text() + "'" + \
                                  " and '" + self.timeend.text() + "'"
        # 每一次查询时清除表格中信息
        self.comment.clearContents()
        self.comment.setRowCount(0)
        if not (is_first):
            self.cur.execute(temp_sqlstring)
            k = 0
            for i in self.cur:
                self.comment.setRowCount(k + 1)
                w = 0
                for j in i:
                    if (type(j) == int) | (type(j) == datetime.datetime):
                        newItem = QTableWidgetItem(str(j))
                    else:
                        newItem = QTableWidgetItem(j)
                    self.comment.setItem(k, w, newItem)
                    w += 1
                k += 1
            self.comment.setColumnWidth(7, 300)

        self.conn.close()
        self.cur.close()
        self.selectcomment.clicked.disconnect(self.selectcomment_click)