# -*- coding: utf-8 -*-
import datetime
import pymysql
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from blogwindow import *


class blogWindow(QMainWindow, Ui_blogwindow):
    def __init__(self):
        super(blogWindow, self).__init__()
        self.setupUi(self)
        self.conn = pymysql.connect("localhost", "root", "199659", "blog")
        self.conn.set_charset('utf8')
        self.cur = self.conn.cursor()
        self.conn.close()
        self.cur.close()
        self.sqlstring = "select * from blogcontent where "

    def selectblog_click(self):
        self.selectblog.clicked.connect(self.selectblog_click)
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
                temp_sqlstring += "author = '" + self.authortext.text() + "'"
            else:
                temp_sqlstring += "author like '" + self.authortext.text() + "'"
        if self.titlecheck.isChecked():
            mystr = self.titletext.text()
            if not is_first:
                temp_sqlstring += "and "
            else:
                is_first = False
            if mystr.find("%") == -1:
                temp_sqlstring += "title = '" + self.titletext.text() + "'"
            else:
                temp_sqlstring += "title like '" + self.titletext.text() + "'"
        if self.tagcheck.isChecked():
            mystr = self.tagtext.text()
            if not is_first:
                temp_sqlstring += "and "
            else:
                is_first = False
            if mystr.find("%") == -1:
                temp_sqlstring += "tag = '" + self.tagtext.text() + "'"
            else:
                temp_sqlstring += "tag like '" + self.tagtext.text() + "'"
        if self.classcheck.isChecked():
            mystr = self.classtext.text()
            if not is_first:
                temp_sqlstring += "and "
            else:
                is_first = False
            if mystr.find("%") == -1:
                temp_sqlstring += "class = '" + self.classtext.text() + "'"
            else:
                temp_sqlstring += "class like '" + self.classtext.text() + "'"
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
        self.blog.clearContents()
        self.blog.setRowCount(0)
        if not (is_first):
            self.cur.execute(temp_sqlstring)
            k = 0
            for i in self.cur:
                self.blog.setRowCount(k + 1)
                w = 0
                for j in i:
                    if (type(j) == int) | (type(j) == datetime.datetime):
                        newItem = QTableWidgetItem(str(j))
                    else:
                        newItem = QTableWidgetItem(j)
                    self.blog.setItem(k, w, newItem)
                    w += 1
                k += 1
            self.blog.setColumnWidth(7, 300)

        self.conn.close()
        self.cur.close()
        self.selectblog.clicked.disconnect(self.selectblog_click)

