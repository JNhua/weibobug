# -*- coding: utf-8 -*-
import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from mainwindow import *
from PyQt5 import QtWidgets
import pymysql
import datetime
from blogform import *
from commentform import *

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.conn = pymysql.connect("localhost", "root", "199659", "blog")
        self.conn.set_charset('utf8')
        self.cur = self.conn.cursor()
        self.sql1 = "select * from blog.blogcontent"
        self.sql2 = "select * from blog.comment"
        # 为博文信息创建表blogcontent
        sql = "\
            CREATE TABLE if not exists blogcontent(\
                bid INT(4) AUTO_INCREMENT,\
                author VARCHAR(20),\
                title VARCHAR(50),\
                tag VARCHAR(50),\
                class VARCHAR(20) DEFAULT NULL,\
                pubtime DATETIME,\
                comment_total_num INT,\
                content LONGTEXT,\
                PRIMARY KEY (bid)\
            )  AUTO_INCREMENT=1 , ENGINE=INNODB DEFAULT CHARSET=UTF8;"
        self.cur.execute(sql)
        # 为每篇博文建立评论表comment
        sql = "\
            CREATE TABLE if not exists comment(\
                cid BIGINT AUTO_INCREMENT,\
                bid INT(4),\
                user VARCHAR(20),\
                pubtime DATETIME,\
                content LONGTEXT,\
                PRIMARY KEY (cid),\
                FOREIGN KEY (bid)\
                    REFERENCES blogcontent (bid)\
                    ON DELETE CASCADE ON UPDATE CASCADE\
            )AUTO_INCREMENT=1 , ENGINE=INNODB DEFAULT CHARSET=UTF8;"
        self.cur.execute(sql)
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        self.blogwindow = blogWindow()
        self.commentwindow = commentWindow()


    def blogspider_click(self):
        self.blogspider.clicked.connect(self.blogspider_click)
        # 测试网络
        try:
            test = requests.get('https://www.baidu.com/')
        except Exception as e:
            print(Exception, ':', e)
            QtWidgets.QMessageBox.warning(self, "警告", '网络不好！')
            self.blogspider.clicked.disconnect(self.blogspider_click)
            return 1
        except requests.exceptions.ConnectTimeout as e:
            print(Exception, ':', e)
            QtWidgets.QMessageBox.warning(self, "警告", '网络不好！')
            self.blogspider.clicked.disconnect(self.blogspider_click)
            return 1
        except requests.exceptions.Timeout as e:
            print(Exception, ':', e)
            QtWidgets.QMessageBox.warning(self, "警告", '网络不好！')
            self.blogspider.clicked.disconnect(self.blogspider_click)
            return 1
        except requests.exceptions.ReadTimeout as e:
            print(Exception, ':', e)
            QtWidgets.QMessageBox.warning(self, "警告", '网络不好！')
            self.blogspider.clicked.disconnect(self.blogspider_click)
            return 1
        # 获取要爬取的博主主页地址
        mainurl = self.blogmainurl.toPlainText().replace(' ', '').strip()
        mainurl = mainurl.split('\n')
        if (len(mainurl) == 1) & (mainurl[0] == ''):
            QtWidgets.QMessageBox.warning(self, "警告", '博客主页不能为空！')
        else:
            # 获取要爬取的每个博主的博文数量
            maxcount = self.maxcount.text().replace(' ', '').strip()
            if maxcount == '':
                QtWidgets.QMessageBox.warning(self, "警告", '博客数量不能为空！')
            else:
                maxcount = int(maxcount)

                self.blogspider.setText('爬取中...')
                self.blogspider.setEnabled(False)
                self.showblog.setEnabled(False)
                self.commentspider.setEnabled(False)
                self.commentwindow.selectcomment.setEnabled(False)
                self.blogwindow.selectblog.setEnabled(False)
                from threads import BigWorkThread
                if self.img.isChecked():
                    self.bwthread = BigWorkThread(mainurl, maxcount, 1)
                else:
                    self.bwthread = BigWorkThread(mainurl, maxcount, 0)
                self.bwthread.start()
                self.bwthread.finishSignal.connect(self.workend)
        self.blogspider.clicked.disconnect(self.blogspider_click)

    def workend(self):
        self.blogspider.setText('爬取完成')
        self.blogspider.setEnabled(True)
        self.showblog.setEnabled(True)
        self.commentspider.setEnabled(True)
        self.commentwindow.selectcomment.setEnabled(True)
        self.blogwindow.selectblog.setEnabled(True)
        self.bwthread.finishSignal.disconnect(self.workend)

    def mainurl_change(self):
        self.blogmainurl.textChanged.connect(self.mainurl_change)
        self.blogspider.setText('爬取博客')
        self.blogmainurl.textChanged.disconnect(self.mainurl_change)

    def count_change(self):
        self.maxcount.textChanged['QString'].connect(self.count_change)
        self.blogspider.setText('爬取博客')
        self.maxcount.textChanged['QString'].disconnect(self.count_change)

    def showblogs(self):
        sql1 = self.sql1
        # 每一次查询时清除表格中信息
        self.blog.clearContents()
        self.cur.execute(sql1)
        k = 0
        for i in self.cur:
            self.blog.setRowCount(k+1)
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

    def showblog_click(self):
        self.showblog.clicked.connect(self.showblog_click)
        self.conn = pymysql.connect("localhost", "root", "199659", "blog")
        self.conn.set_charset('utf8')
        self.cur = self.conn.cursor()
        self.showblogs()
        self.cur.close()
        self.conn.close()
        self.showblog.clicked.disconnect(self.showblog_click)

    def commentspider_click(self):
        self.commentspider.clicked.connect(self.commentspider_click)
        self.conn = pymysql.connect("localhost", "root", "199659", "blog")
        self.conn.set_charset('utf8')
        self.cur = self.conn.cursor()
        sql2 = self.sql2
        # 每一次查询时清除表格中信息
        self.comment.clearContents()
        self.cur.execute(sql2)
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
        self.comment.setColumnWidth(4, 300)
        self.cur.close()
        self.conn.close()
        self.commentspider.clicked.disconnect(self.commentspider_click)

    def showblogwindow_click(self):
        self.showblogwindow.clicked.connect(self.showblogwindow_click)
        self.blogwindow.show()
        self.showblogwindow.clicked.disconnect(self.showblogwindow_click)

    def showcommentwindow_click(self):
        self.showcommentwindow.clicked.connect(self.showcommentwindow_click)
        self.commentwindow.show()
        self.showcommentwindow.clicked.disconnect(self.showcommentwindow_click)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MyWindow()
    mainWindow.show()
    sys.exit(app.exec_())
