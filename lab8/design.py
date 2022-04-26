# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2200, 1500)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 200, 441, 161))
        self.groupBox.setObjectName("groupBox")
        self.box_color_segment = QtWidgets.QComboBox(self.groupBox)
        self.box_color_segment.setGeometry(QtCore.QRect(10, 50, 391, 71))
        self.box_color_segment.setObjectName("box_color_segment")
        self.box_color_segment.addItem("")
        self.box_color_segment.addItem("")
        self.box_color_segment.addItem("")
        self.box_color_segment.addItem("")
        self.box_color_segment.addItem("")
        self.box_color_segment.addItem("")
        self.box_color_segment.addItem("")
        self.box_color_segment.addItem("")
        self.graph = QtWidgets.QGraphicsView(self.centralwidget)
        self.graph.setGeometry(QtCore.QRect(530, 30, 1600, 1100))
        self.graph.setObjectName("graph")
        self.table_segments = QtWidgets.QTableWidget(self.centralwidget)
        self.table_segments.setGeometry(QtCore.QRect(580, 1190, 791, 151))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.table_segments.setFont(font)
        self.table_segments.setColumnCount(4)
        self.table_segments.setObjectName("table_segments")
        self.table_segments.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_segments.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_segments.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_segments.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_segments.setHorizontalHeaderItem(3, item)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(560, 1150, 841, 201))
        self.groupBox_4.setObjectName("groupBox_4")
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(20, 30, 441, 161))
        self.groupBox_5.setObjectName("groupBox_5")
        self.box_color_cutter = QtWidgets.QComboBox(self.groupBox_5)
        self.box_color_cutter.setGeometry(QtCore.QRect(10, 50, 391, 71))
        self.box_color_cutter.setObjectName("box_color_cutter")
        self.box_color_cutter.addItem("")
        self.box_color_cutter.addItem("")
        self.box_color_cutter.addItem("")
        self.box_color_cutter.addItem("")
        self.box_color_cutter.addItem("")
        self.box_color_cutter.addItem("")
        self.box_color_cutter.addItem("")
        self.box_color_cutter.addItem("")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 380, 441, 241))
        self.groupBox_2.setObjectName("groupBox_2")
        self.box_color_result = QtWidgets.QComboBox(self.groupBox_2)
        self.box_color_result.setGeometry(QtCore.QRect(10, 50, 391, 71))
        self.box_color_result.setObjectName("box_color_result")
        self.box_color_result.addItem("")
        self.box_color_result.addItem("")
        self.box_color_result.addItem("")
        self.box_color_result.addItem("")
        self.box_color_result.addItem("")
        self.box_color_result.addItem("")
        self.box_color_result.addItem("")
        self.box_color_result.addItem("")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(20, 160, 181, 41))
        self.label_10.setObjectName("label_10")
        self.box_width = QtWidgets.QSpinBox(self.groupBox_2)
        self.box_width.setGeometry(QtCore.QRect(240, 160, 111, 41))
        self.box_width.setMinimum(1)
        self.box_width.setMaximum(10000)
        self.box_width.setSingleStep(1)
        self.box_width.setProperty("value", 1)
        self.box_width.setObjectName("box_width")
        self.but_connect = QtWidgets.QPushButton(self.centralwidget)
        self.but_connect.setGeometry(QtCore.QRect(20, 950, 441, 61))
        self.but_connect.setObjectName("but_connect")
        self.but_cut = QtWidgets.QPushButton(self.centralwidget)
        self.but_cut.setGeometry(QtCore.QRect(20, 1160, 441, 61))
        self.but_cut.setObjectName("but_cut")
        self.but_clean = QtWidgets.QPushButton(self.centralwidget)
        self.but_clean.setGeometry(QtCore.QRect(20, 1240, 441, 61))
        self.but_clean.setObjectName("but_clean")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(560, 1360, 2161, 111))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 720, 441, 211))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(20, 60, 47, 41))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(230, 60, 47, 41))
        self.label_4.setObjectName("label_4")
        self.box_x = QtWidgets.QSpinBox(self.groupBox_3)
        self.box_x.setGeometry(QtCore.QRect(60, 60, 111, 41))
        self.box_x.setMinimum(-10000)
        self.box_x.setMaximum(10000)
        self.box_x.setSingleStep(100)
        self.box_x.setProperty("value", 200)
        self.box_x.setObjectName("box_x")
        self.box_y = QtWidgets.QSpinBox(self.groupBox_3)
        self.box_y.setGeometry(QtCore.QRect(280, 60, 111, 41))
        self.box_y.setMinimum(-10000)
        self.box_y.setMaximum(10000)
        self.box_y.setSingleStep(100)
        self.box_y.setProperty("value", 200)
        self.box_y.setObjectName("box_y")
        self.but_input_point_segment = QtWidgets.QPushButton(self.groupBox_3)
        self.but_input_point_segment.setGeometry(QtCore.QRect(230, 140, 201, 51))
        self.but_input_point_segment.setObjectName("but_input_point_segment")
        self.but_input_point_cutter = QtWidgets.QPushButton(self.groupBox_3)
        self.but_input_point_cutter.setGeometry(QtCore.QRect(10, 140, 201, 51))
        self.but_input_point_cutter.setObjectName("but_input_point_cutter")
        self.table_cutter = QtWidgets.QTableWidget(self.centralwidget)
        self.table_cutter.setGeometry(QtCore.QRect(1440, 1190, 471, 151))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.table_cutter.setFont(font)
        self.table_cutter.setColumnCount(2)
        self.table_cutter.setObjectName("table_cutter")
        self.table_cutter.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_cutter.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_cutter.setHorizontalHeaderItem(1, item)
        self.groupBox_6 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_6.setGeometry(QtCore.QRect(1420, 1150, 521, 201))
        self.groupBox_6.setObjectName("groupBox_6")
        self.groupBox_6.raise_()
        self.groupBox_4.raise_()
        self.groupBox.raise_()
        self.graph.raise_()
        self.table_segments.raise_()
        self.groupBox_5.raise_()
        self.groupBox_2.raise_()
        self.but_connect.raise_()
        self.but_cut.raise_()
        self.but_clean.raise_()
        self.label.raise_()
        self.groupBox_3.raise_()
        self.table_cutter.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Алгоритм отсечения отрезка произвольным выпуклым отсекателем (Алгоритм Кируса—Бека)"))
        self.groupBox.setTitle(_translate("MainWindow", "Цвет отрезков"))
        self.box_color_segment.setItemText(0, _translate("MainWindow", "Черный"))
        self.box_color_segment.setItemText(1, _translate("MainWindow", "Синий"))
        self.box_color_segment.setItemText(2, _translate("MainWindow", "Зеленый"))
        self.box_color_segment.setItemText(3, _translate("MainWindow", "Красный"))
        self.box_color_segment.setItemText(4, _translate("MainWindow", "Розовый"))
        self.box_color_segment.setItemText(5, _translate("MainWindow", "Бирюзовый"))
        self.box_color_segment.setItemText(6, _translate("MainWindow", "Голубой"))
        self.box_color_segment.setItemText(7, _translate("MainWindow", "Желтый"))
        item = self.table_segments.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "X1"))
        item = self.table_segments.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Y1"))
        item = self.table_segments.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "X2"))
        item = self.table_segments.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Y2"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Введенные отрезки"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Цвет отсекателя"))
        self.box_color_cutter.setItemText(0, _translate("MainWindow", "Красный"))
        self.box_color_cutter.setItemText(1, _translate("MainWindow", "Черный"))
        self.box_color_cutter.setItemText(2, _translate("MainWindow", "Зеленый"))
        self.box_color_cutter.setItemText(3, _translate("MainWindow", "Розовый"))
        self.box_color_cutter.setItemText(4, _translate("MainWindow", "Бирюзовый"))
        self.box_color_cutter.setItemText(5, _translate("MainWindow", "Голубой"))
        self.box_color_cutter.setItemText(6, _translate("MainWindow", "Синий"))
        self.box_color_cutter.setItemText(7, _translate("MainWindow", "Желтый"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Цвет и толщина результата"))
        self.box_color_result.setItemText(0, _translate("MainWindow", "Зеленый"))
        self.box_color_result.setItemText(1, _translate("MainWindow", "Черный"))
        self.box_color_result.setItemText(2, _translate("MainWindow", "Розовый"))
        self.box_color_result.setItemText(3, _translate("MainWindow", "Бирюзовый"))
        self.box_color_result.setItemText(4, _translate("MainWindow", "Голубой"))
        self.box_color_result.setItemText(5, _translate("MainWindow", "Красный"))
        self.box_color_result.setItemText(6, _translate("MainWindow", "Синий"))
        self.box_color_result.setItemText(7, _translate("MainWindow", "Желтый"))
        self.label_10.setText(_translate("MainWindow", "Толщина:"))
        self.but_connect.setText(_translate("MainWindow", "Замнкнуть отсекатель"))
        self.but_cut.setText(_translate("MainWindow", "Отсечь"))
        self.but_clean.setText(_translate("MainWindow", "Очистить экран"))
        self.label.setText(_translate("MainWindow", "Левая кнопка мыши - ввод вершины отрезка; правая - ввод вершины отсекателя."))
        self.groupBox_3.setTitle(_translate("MainWindow", "Ввод вершины"))
        self.label_3.setText(_translate("MainWindow", "X:"))
        self.label_4.setText(_translate("MainWindow", "Y:"))
        self.but_input_point_segment.setText(_translate("MainWindow", "Отрезок"))
        self.but_input_point_cutter.setText(_translate("MainWindow", "Отсекатель"))
        item = self.table_cutter.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "X1"))
        item = self.table_cutter.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Y1"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Введенные вершины отсекателя"))
