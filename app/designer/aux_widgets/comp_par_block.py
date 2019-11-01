# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'comp_par_block.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CompParBlock(object):
    def setupUi(self, CompParBlock):
        CompParBlock.setObjectName("CompParBlock")
        CompParBlock.resize(230, 70)
        CompParBlock.setMaximumSize(QtCore.QSize(270, 16777215))
        self.gridLayout = QtWidgets.QGridLayout(CompParBlock)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(CompParBlock)
        self.frame.setMaximumSize(QtCore.QSize(270, 16777215))
        self.frame.setAutoFillBackground(False)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLineWidth(1)
        self.frame.setMidLineWidth(1)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.comp = QtWidgets.QLabel(self.frame)
        self.comp.setObjectName("comp")
        self.gridLayout_2.addWidget(self.comp, 0, 0, 1, 1)
        self.val = QtWidgets.QDoubleSpinBox(self.frame)
        self.val.setAlignment(QtCore.Qt.AlignCenter)
        self.val.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.val.setDecimals(4)
        self.val.setMaximum(1000000000000000.0)
        self.val.setObjectName("val")
        self.gridLayout_2.addWidget(self.val, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        self.retranslateUi(CompParBlock)
        QtCore.QMetaObject.connectSlotsByName(CompParBlock)

    def retranslateUi(self, CompParBlock):
        _translate = QtCore.QCoreApplication.translate
        CompParBlock.setWindowTitle(_translate("CompParBlock", "Form"))
        self.comp.setText(_translate("CompParBlock", "<html><head/><body><p align=\"right\"><span style=\" font-size:10pt; font-weight:600;\">Comp:</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CompParBlock = QtWidgets.QWidget()
    ui = Ui_CompParBlock()
    ui.setupUi(CompParBlock)
    CompParBlock.show()
    sys.exit(app.exec_())
