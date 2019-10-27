# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pole_block.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PoleBlock(object):
    def setupUi(self, PoleBlock):
        PoleBlock.setObjectName("PoleBlock")
        PoleBlock.resize(200, 70)
        self.gridLayout = QtWidgets.QGridLayout(PoleBlock)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(PoleBlock)
        self.frame.setAutoFillBackground(False)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLineWidth(1)
        self.frame.setMidLineWidth(1)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 4, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.q_val = QtWidgets.QLabel(self.frame)
        self.q_val.setObjectName("q_val")
        self.gridLayout_2.addWidget(self.q_val, 0, 5, 1, 1)
        self.fp = QtWidgets.QLabel(self.frame)
        self.fp.setObjectName("fp")
        self.gridLayout_2.addWidget(self.fp, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 2, 1, 1)
        self.order = QtWidgets.QLabel(self.frame)
        self.order.setObjectName("order")
        self.gridLayout_2.addWidget(self.order, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(PoleBlock)
        QtCore.QMetaObject.connectSlotsByName(PoleBlock)

    def retranslateUi(self, PoleBlock):
        _translate = QtCore.QCoreApplication.translate
        PoleBlock.setWindowTitle(_translate("PoleBlock", "Form"))
        self.label_4.setText(_translate("PoleBlock", "<html><head/><body><p align=\"right\"><span style=\" font-size:10pt;\">Q:</span></p></body></html>"))
        self.label_3.setText(_translate("PoleBlock", "<html><head/><body><p align=\"right\"><span style=\" font-size:10pt;\">f</span><span style=\" font-size:10pt; vertical-align:sub;\">p</span><span style=\" font-size:10pt;\">:</span></p></body></html>"))
        self.q_val.setText(_translate("PoleBlock", "<html><head/><body><p><span style=\" font-size:10pt;\">...</span></p></body></html>"))
        self.fp.setText(_translate("PoleBlock", "<html><head/><body><p>...</p></body></html>"))
        self.label.setText(_translate("PoleBlock", "<html><head/><body><p align=\"right\"><span style=\" font-size:10pt;\">n:</span></p></body></html>"))
        self.order.setText(_translate("PoleBlock", "<html><head/><body><p><span style=\" font-size:10pt;\">...</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PoleBlock = QtWidgets.QWidget()
    ui = Ui_PoleBlock()
    ui.setupUi(PoleBlock)
    PoleBlock.show()
    sys.exit(app.exec_())
