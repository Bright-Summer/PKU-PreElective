# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\VSCode\VSCode-Python\PKU-PreElective\ui\form_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(602, 333)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.CourseTable = QtWidgets.QTableView(self.centralwidget)
        self.CourseTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.CourseTable.setObjectName("CourseTable")
        self.CourseTable.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.CourseTable)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.CourseNameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.CourseNameEdit.setObjectName("CourseNameEdit")
        self.horizontalLayout_3.addWidget(self.CourseNameEdit)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.CollegeEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.CollegeEdit.setObjectName("CollegeEdit")
        self.horizontalLayout_3.addWidget(self.CollegeEdit)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.TypeEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.TypeEdit.setObjectName("TypeEdit")
        self.horizontalLayout_3.addWidget(self.TypeEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.SelectedTable = QtWidgets.QTableView(self.centralwidget)
        self.SelectedTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.SelectedTable.setObjectName("SelectedTable")
        self.SelectedTable.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.SelectedTable)
        self.CreditLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.CreditLabel.setFont(font)
        self.CreditLabel.setObjectName("CreditLabel")
        self.verticalLayout.addWidget(self.CreditLabel)
        self.DisableColumn = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.DisableColumn.setFont(font)
        self.DisableColumn.setObjectName("DisableColumn")
        self.verticalLayout.addWidget(self.DisableColumn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.TimeTableLayout = QtWidgets.QVBoxLayout()
        self.TimeTableLayout.setObjectName("TimeTableLayout")
        self.ScrollFig = QtWidgets.QScrollArea(self.centralwidget)
        self.ScrollFig.setWidgetResizable(True)
        self.ScrollFig.setObjectName("ScrollFig")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 63, 159))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.ScrollFig.setWidget(self.scrollAreaWidgetContents)
        self.TimeTableLayout.addWidget(self.ScrollFig)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.TimeTableLayout.addWidget(self.label_6)
        self.CrashLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.CrashLabel.setFont(font)
        self.CrashLabel.setText("")
        self.CrashLabel.setObjectName("CrashLabel")
        self.TimeTableLayout.addWidget(self.CrashLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.TimeTableLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.TimeTableLayout)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 602, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PKU-PreElective-v1.0"))
        self.label_2.setText(_translate("MainWindow", "未选课程列表：（双击选课）"))
        self.label_3.setText(_translate("MainWindow", "课名："))
        self.label_4.setText(_translate("MainWindow", "开课单位："))
        self.label_5.setText(_translate("MainWindow", "课程类型："))
        self.label.setText(_translate("MainWindow", "已选列表：（双击退课）"))
        self.CreditLabel.setText(_translate("MainWindow", "当前总学分：0"))
        self.DisableColumn.setText(_translate("MainWindow", "隐藏课号、班号、起止周"))
        self.label_6.setText(_translate("MainWindow", "冲突选课："))
