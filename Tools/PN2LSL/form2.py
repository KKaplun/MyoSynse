# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import numpy as np


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        # PySide's QTime() initialiser fails miserably and dismisses args/kwargs
        return [QtCore.QTime().addMSecs(value).toString('mm:ss') for value in values]


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1350, 750)

        self.plot_1 = pg.PlotWidget(Form)
        self.plot_1.setGeometry(QtCore.QRect(50,50,400,200))
        self.plot_2 = pg.PlotWidget(Form)
        self.plot_2.setGeometry(QtCore.QRect(475, 50, 400, 200))
        self.plot_3 = pg.PlotWidget(Form)
        self.plot_3.setGeometry(QtCore.QRect(900, 50, 400, 200))
        self.plot_4 = pg.PlotWidget(Form)
        self.plot_4.setGeometry(QtCore.QRect(475, 275, 400, 200))

        self.plot_1.axisItems = {'bottom': TimeAxisItem(orientation='bottom')}
        self.plot_2.axisItems = {'bottom': TimeAxisItem(orientation='bottom')}
        self.plot_3.axisItems = {'bottom': TimeAxisItem(orientation='bottom')}
        self.plot_4.axisItems = {'bottom': TimeAxisItem(orientation='bottom')}

        #self.plot_1.setXRange()
        #self.plot_2.setXRange(-10, 0)
        #self.plot_3.setXRange(-10, 0)

        self.plot_1.setYRange(-180, 180)
        self.plot_2.setYRange(-180, 180)
        self.plot_3.setYRange(-180, 180)

        self.p1 = self.plot_1.plot()
        #self.p1.setPen(200, 200, 100)
        self.p2 = self.plot_2.plot()
        #self.p2.setPen(200, 200, 100)
        self.p3 = self.plot_3.plot()
        #self.p3.setPen(200, 200, 100)
        self.p4 = self.plot_4.plot()
        self.p4.setPen(200,200,100)

        #self.plot_1.enableAutoRange('x', True)
        #self.plot_2.enableAutoRange('x', True)
        #self.plot_3.enableAutoRange('x', True)
        #self.plot_4.enableAutoRange('x', True)

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(600, 550, 120, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(600, 600, 120, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(570, 650, 80, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(670, 650, 80, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(600, 700, 80, 25))
        self.pushButton_3.setObjectName("pushButton_3")

        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(600, 500, 120, 20))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setItemText(59, "")


        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(570, 550, 50, 15))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(570, 600, 50, 15))
        self.label_8.setObjectName("label_8")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))



        self.lineEdit.setInputMask(_translate("Form", "000.000.000.000"))
        self.lineEdit_2.setInputMask(_translate("Form", "00000"))
        self.pushButton.setText(_translate("Form", "Connect"))
        self.pushButton_2.setText(_translate("Form", "Stop"))
        self.pushButton_3.setText(_translate("Form", "Refresh"))

        self.comboBox.setItemText(0, _translate("Form", "Hips"))
        self.comboBox.setItemText(1, _translate("Form", "RightUpLeg"))
        self.comboBox.setItemText(2, _translate("Form", "RightLeg"))
        self.comboBox.setItemText(3, _translate("Form", "RightFoot"))
        self.comboBox.setItemText(4, _translate("Form", "LeftUpLeg"))
        self.comboBox.setItemText(5, _translate("Form", "LeftLeg"))
        self.comboBox.setItemText(6, _translate("Form", "LeftFoot"))
        self.comboBox.setItemText(7, _translate("Form", "Spine"))
        self.comboBox.setItemText(8, _translate("Form", "Spine1"))
        self.comboBox.setItemText(9, _translate("Form", "Spine2"))
        self.comboBox.setItemText(10, _translate("Form", "Spine3"))
        self.comboBox.setItemText(11, _translate("Form", "Neck"))
        self.comboBox.setItemText(12, _translate("Form", "Head"))
        self.comboBox.setItemText(13, _translate("Form", "RightShoulder"))
        self.comboBox.setItemText(14, _translate("Form", "RightArm"))
        self.comboBox.setItemText(15, _translate("Form", "RightForeArm"))
        self.comboBox.setItemText(16, _translate("Form", "RightHand"))
        self.comboBox.setItemText(17, _translate("Form", "RightHandThumb1"))
        self.comboBox.setItemText(18, _translate("Form", "RightHandThumb2"))
        self.comboBox.setItemText(19, _translate("Form", "RightHandThumb3"))
        self.comboBox.setItemText(20, _translate("Form", "RightInHandIndex"))
        self.comboBox.setItemText(21, _translate("Form", "RightHandIndex1"))
        self.comboBox.setItemText(22, _translate("Form", "RightHandIndex2"))
        self.comboBox.setItemText(23, _translate("Form", "RightHandIndex3"))
        self.comboBox.setItemText(24, _translate("Form", "RightInHandMiddle"))
        self.comboBox.setItemText(25, _translate("Form", "RightHandMiddle1"))
        self.comboBox.setItemText(26, _translate("Form", "RightHandMiddle2"))
        self.comboBox.setItemText(27, _translate("Form", "RightHandMiddle3"))
        self.comboBox.setItemText(28, _translate("Form", "RightInHandRing"))
        self.comboBox.setItemText(29, _translate("Form", "RightHandRing1"))
        self.comboBox.setItemText(30, _translate("Form", "RightHandRing2"))
        self.comboBox.setItemText(31, _translate("Form", "RightHandRing3"))
        self.comboBox.setItemText(32, _translate("Form", "RightInHandPinky"))
        self.comboBox.setItemText(33, _translate("Form", "RightHandPinky1"))
        self.comboBox.setItemText(34, _translate("Form", "RightHandPinky2"))
        self.comboBox.setItemText(35, _translate("Form", "RightHandPinky3"))
        self.comboBox.setItemText(36, _translate("Form", "LeftShoulder"))
        self.comboBox.setItemText(37, _translate("Form", "LeftArm"))
        self.comboBox.setItemText(38, _translate("Form", "LeftForeArm"))
        self.comboBox.setItemText(39, _translate("Form", "LeftHand"))
        self.comboBox.setItemText(40, _translate("Form", "LeftHandThumb1"))
        self.comboBox.setItemText(41, _translate("Form", "LeftHandThumb2"))
        self.comboBox.setItemText(42, _translate("Form", "LeftHandThumb3"))
        self.comboBox.setItemText(43, _translate("Form", "LeftInHandIndex"))
        self.comboBox.setItemText(44, _translate("Form", "LeftHandIndex1"))
        self.comboBox.setItemText(45, _translate("Form", "LeftHandIndex2"))
        self.comboBox.setItemText(46, _translate("Form", "LeftHandIndex3"))
        self.comboBox.setItemText(47, _translate("Form", "LeftInHandMiddle"))
        self.comboBox.setItemText(48, _translate("Form", "LeftHandMiddle1"))
        self.comboBox.setItemText(49, _translate("Form", "LeftHandMiddle2"))
        self.comboBox.setItemText(50, _translate("Form", "LeftHandMiddle3"))
        self.comboBox.setItemText(51, _translate("Form", "LeftInHandRing"))
        self.comboBox.setItemText(52, _translate("Form", "LeftHandRing1"))
        self.comboBox.setItemText(53, _translate("Form", "LeftHandRing2"))
        self.comboBox.setItemText(54, _translate("Form", "LeftHandRing3"))
        self.comboBox.setItemText(55, _translate("Form", "LeftInHandPinky"))
        self.comboBox.setItemText(56, _translate("Form", "LeftHandPinky1"))
        self.comboBox.setItemText(57, _translate("Form", "LeftHandPinky2"))
        self.comboBox.setItemText(58, _translate("Form", "LeftHandPinky3"))
        self.label_7.setText(_translate("Form", "IP"))
        self.label_8.setText(_translate("Form", "Port"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

