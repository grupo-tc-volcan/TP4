# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zero_block.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ZeroBlock(object):
    def setupUi(self, ZeroBlock):
        ZeroBlock.setObjectName("ZeroBlock")
        ZeroBlock.resize(230, 70)
        ZeroBlock.setMaximumSize(QtCore.QSize(270, 16777215))
        self.gridLayout = QtWidgets.QGridLayout(ZeroBlock)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(ZeroBlock)
        self.frame.setMaximumSize(QtCore.QSize(270, 16777215))
        self.frame.setAutoFillBackground(False)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLineWidth(1)
        self.frame.setMidLineWidth(1)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.f0 = QtWidgets.QLabel(self.frame)
        self.f0.setObjectName("f0")
        self.gridLayout_2.addWidget(self.f0, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 2, 1, 1)
        self.order = QtWidgets.QLabel(self.frame)
        self.order.setObjectName("order")
        self.gridLayout_2.addWidget(self.order, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        self.retranslateUi(ZeroBlock)
        QtCore.QMetaObject.connectSlotsByName(ZeroBlock)

    def retranslateUi(self, ZeroBlock):
        _translate = QtCore.QCoreApplication.translate
        ZeroBlock.setWindowTitle(_translate("ZeroBlock", "Form"))
        self.label_3.setText(_translate("ZeroBlock", "<html><head/><body><p align=\"right\"><span style=\" font-size:10pt; font-weight:600;\">f</span><span style=\" font-size:10pt; font-weight:600; vertical-align:sub;\">0</span><span style=\" font-size:10pt; font-weight:600;\">:</span></p></body></html>"))
        self.f0.setText(_translate("ZeroBlock", "<html><head/><body><p><span style=\" font-size:10pt;\">...</span></p></body></html>"))
        self.label.setText(_translate("ZeroBlock", "<html><head/><body><p align=\"right\"><span style=\" font-size:10pt; font-weight:600;\">n:</span></p></body></html>"))
        self.order.setText(_translate("ZeroBlock", "<html><head/><body><p><span style=\" font-size:10pt;\">...</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ZeroBlock = QtWidgets.QWidget()
    ui = Ui_ZeroBlock()
    ui.setupUi(ZeroBlock)
    ZeroBlock.show()
    sys.exit(app.exec_())
