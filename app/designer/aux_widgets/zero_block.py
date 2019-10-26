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
        ZeroBlock.resize(200, 70)
        self.gridLayout = QtWidgets.QGridLayout(ZeroBlock)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(ZeroBlock)
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
        self.wp = QtWidgets.QLabel(self.frame)
        self.wp.setObjectName("wp")
        self.gridLayout_2.addWidget(self.wp, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 4, 1, 1)
        self.q_val = QtWidgets.QLabel(self.frame)
        self.q_val.setObjectName("q_val")
        self.gridLayout_2.addWidget(self.q_val, 0, 5, 1, 1)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        self.retranslateUi(ZeroBlock)
        QtCore.QMetaObject.connectSlotsByName(ZeroBlock)

    def retranslateUi(self, ZeroBlock):
        _translate = QtCore.QCoreApplication.translate
        ZeroBlock.setWindowTitle(_translate("ZeroBlock", "Form"))
        self.label_3.setText(_translate("ZeroBlock", "<html><head/><body><p align=\"right\"><span style=\" font-size:10pt;\">f</span><span style=\" font-size:10pt; vertical-align:sub;\">0</span><span style=\" font-size:10pt;\">:</span></p></body></html>"))
        self.wp.setText(_translate("ZeroBlock", "<html><head/><body><p><span style=\" font-size:10pt;\">...</span></p></body></html>"))
        self.label.setText(_translate("ZeroBlock", "<html><head/><body><p align=\"right\"><span style=\" font-size:10pt;\">n:</span></p></body></html>"))
        self.label_2.setText(_translate("ZeroBlock", "<html><head/><body><p><span style=\" font-size:10pt;\">...</span></p></body></html>"))
        self.label_4.setText(_translate("ZeroBlock", "<html><head/><body><p align=\"right\"><span style=\" font-size:10pt;\">Q:</span></p></body></html>"))
        self.q_val.setText(_translate("ZeroBlock", "<html><head/><body><p><span style=\" font-size:10pt;\">...</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ZeroBlock = QtWidgets.QWidget()
    ui = Ui_ZeroBlock()
    ui.setupUi(ZeroBlock)
    ZeroBlock.show()
    sys.exit(app.exec_())
