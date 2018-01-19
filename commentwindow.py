# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'commentwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_commentwindow(object):
    def setupUi(self, commentwindow):
        commentwindow.setObjectName("commentwindow")
        commentwindow.resize(585, 438)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/image/insect_128px_1168368_easyicon.net.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(":/image/image/insect_128px_1168368_easyicon.net.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        commentwindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(commentwindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.authorcheck = QtWidgets.QCheckBox(self.centralwidget)
        self.authorcheck.setObjectName("authorcheck")
        self.horizontalLayout_7.addWidget(self.authorcheck)
        self.authortext = QtWidgets.QLineEdit(self.centralwidget)
        self.authortext.setObjectName("authortext")
        self.horizontalLayout_7.addWidget(self.authortext)
        self.gridLayout_2.addLayout(self.horizontalLayout_7, 0, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.bidcheck = QtWidgets.QCheckBox(self.centralwidget)
        self.bidcheck.setObjectName("bidcheck")
        self.horizontalLayout_8.addWidget(self.bidcheck)
        self.bidtext = QtWidgets.QLineEdit(self.centralwidget)
        self.bidtext.setObjectName("bidtext")
        self.horizontalLayout_8.addWidget(self.bidtext)
        self.gridLayout_2.addLayout(self.horizontalLayout_8, 0, 1, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.contentcheck = QtWidgets.QCheckBox(self.centralwidget)
        self.contentcheck.setObjectName("contentcheck")
        self.horizontalLayout_11.addWidget(self.contentcheck)
        self.contenttext = QtWidgets.QLineEdit(self.centralwidget)
        self.contenttext.setObjectName("contenttext")
        self.horizontalLayout_11.addWidget(self.contenttext)
        self.gridLayout_2.addLayout(self.horizontalLayout_11, 1, 0, 1, 1)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.timecheck = QtWidgets.QCheckBox(self.centralwidget)
        self.timecheck.setObjectName("timecheck")
        self.horizontalLayout_12.addWidget(self.timecheck)
        self.timebegin = QtWidgets.QLineEdit(self.centralwidget)
        self.timebegin.setObjectName("timebegin")
        self.horizontalLayout_12.addWidget(self.timebegin)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_12.addWidget(self.label_2)
        self.timeend = QtWidgets.QLineEdit(self.centralwidget)
        self.timeend.setObjectName("timeend")
        self.horizontalLayout_12.addWidget(self.timeend)
        self.gridLayout_2.addLayout(self.horizontalLayout_12, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem)
        self.selectcomment = QtWidgets.QPushButton(self.centralwidget)
        self.selectcomment.setObjectName("selectcomment")
        self.horizontalLayout_13.addWidget(self.selectcomment)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_13)
        self.comment = QtWidgets.QTableWidget(self.centralwidget)
        self.comment.setObjectName("comment")
        self.comment.setColumnCount(5)
        self.comment.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.comment.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.comment.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.comment.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.comment.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.comment.setHorizontalHeaderItem(4, item)
        self.verticalLayout.addWidget(self.comment)
        commentwindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(commentwindow)
        self.selectcomment.clicked.connect(commentwindow.selectcomment_click)
        QtCore.QMetaObject.connectSlotsByName(commentwindow)

    def retranslateUi(self, commentwindow):
        _translate = QtCore.QCoreApplication.translate
        commentwindow.setWindowTitle(_translate("commentwindow", "评论_数据库"))
        self.authorcheck.setText(_translate("commentwindow", "用户名  "))
        self.bidcheck.setText(_translate("commentwindow", "博客编号"))
        self.contentcheck.setText(_translate("commentwindow", "评论内容"))
        self.timecheck.setText(_translate("commentwindow", "评论时间"))
        self.label_2.setText(_translate("commentwindow", "到"))
        self.selectcomment.setText(_translate("commentwindow", "查询"))
        item = self.comment.horizontalHeaderItem(0)
        item.setText(_translate("commentwindow", "评论编号"))
        item = self.comment.horizontalHeaderItem(1)
        item.setText(_translate("commentwindow", "博客编号"))
        item = self.comment.horizontalHeaderItem(2)
        item.setText(_translate("commentwindow", "作者"))
        item = self.comment.horizontalHeaderItem(3)
        item.setText(_translate("commentwindow", "评论时间"))
        item = self.comment.horizontalHeaderItem(4)
        item.setText(_translate("commentwindow", "评论内容"))

import res_rc