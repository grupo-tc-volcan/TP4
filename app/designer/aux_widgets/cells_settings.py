# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cells_settings.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 463)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.cell_selector = QtWidgets.QComboBox(Form)
        self.cell_selector.setMaximumSize(QtCore.QSize(300, 16777215))
        self.cell_selector.setObjectName("cell_selector")
        self.cell_selector.addItem("")
        self.cell_selector.addItem("")
        self.cell_selector.addItem("")
        self.cell_selector.addItem("")
        self.cell_selector.addItem("")
        self.cell_selector.addItem("")
        self.cell_selector.addItem("")
        self.gridLayout.addWidget(self.cell_selector, 0, 0, 1, 1)
        self.cell_components = QtWidgets.QListView(Form)
        self.cell_components.setMaximumSize(QtCore.QSize(300, 16777215))
        self.cell_components.setDragEnabled(True)
        self.cell_components.setDragDropOverwriteMode(True)
        self.cell_components.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.cell_components.setObjectName("cell_components")
        self.gridLayout.addWidget(self.cell_components, 1, 0, 1, 1)
        self.cell_sensitivities = QtWidgets.QListView(Form)
        self.cell_sensitivities.setMaximumSize(QtCore.QSize(300, 16777215))
        self.cell_sensitivities.setDragEnabled(True)
        self.cell_sensitivities.setDragDropOverwriteMode(True)
        self.cell_sensitivities.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.cell_sensitivities.setObjectName("cell_sensitivities")
        self.gridLayout.addWidget(self.cell_sensitivities, 2, 0, 1, 1)
        self.report_button = QtWidgets.QPushButton(Form)
        self.report_button.setMaximumSize(QtCore.QSize(300, 16777215))
        self.report_button.setObjectName("report_button")
        self.gridLayout.addWidget(self.report_button, 3, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.cell_selector.setItemText(0, _translate("Form", "Sallen-Key"))
        self.cell_selector.setItemText(1, _translate("Form", "Rauch"))
        self.cell_selector.setItemText(2, _translate("Form", "Sedra-Ghorab-Martin"))
        self.cell_selector.setItemText(3, _translate("Form", "Kerwin-Huelsman-Newcom"))
        self.cell_selector.setItemText(4, _translate("Form", "Tow-Thomas"))
        self.cell_selector.setItemText(5, _translate("Form", "Ackerberg-Mossber"))
        self.cell_selector.setItemText(6, _translate("Form", "Fleischer-Tow"))
        self.report_button.setText(_translate("Form", "HTML Report"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
