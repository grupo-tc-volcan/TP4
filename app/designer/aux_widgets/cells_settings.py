# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cells_settings.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CellsSettings(object):
    def setupUi(self, CellsSettings):
        CellsSettings.setObjectName("CellsSettings")
        CellsSettings.resize(300, 463)
        self.gridLayout = QtWidgets.QGridLayout(CellsSettings)
        self.gridLayout.setObjectName("gridLayout")
        self.cell_selector = QtWidgets.QComboBox(CellsSettings)
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
        self.cell_components = QtWidgets.QListView(CellsSettings)
        self.cell_components.setMaximumSize(QtCore.QSize(300, 16777215))
        self.cell_components.setDragEnabled(True)
        self.cell_components.setDragDropOverwriteMode(True)
        self.cell_components.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.cell_components.setObjectName("cell_components")
        self.gridLayout.addWidget(self.cell_components, 1, 0, 1, 1)
        self.cell_sensitivities = QtWidgets.QListView(CellsSettings)
        self.cell_sensitivities.setMaximumSize(QtCore.QSize(300, 16777215))
        self.cell_sensitivities.setDragEnabled(True)
        self.cell_sensitivities.setDragDropOverwriteMode(True)
        self.cell_sensitivities.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.cell_sensitivities.setObjectName("cell_sensitivities")
        self.gridLayout.addWidget(self.cell_sensitivities, 2, 0, 1, 1)
        self.report_button = QtWidgets.QPushButton(CellsSettings)
        self.report_button.setMaximumSize(QtCore.QSize(300, 16777215))
        self.report_button.setObjectName("report_button")
        self.gridLayout.addWidget(self.report_button, 3, 0, 1, 1)

        self.retranslateUi(CellsSettings)
        QtCore.QMetaObject.connectSlotsByName(CellsSettings)

    def retranslateUi(self, CellsSettings):
        _translate = QtCore.QCoreApplication.translate
        CellsSettings.setWindowTitle(_translate("CellsSettings", "Form"))
        self.cell_selector.setItemText(0, _translate("CellsSettings", "Sallen-Key"))
        self.cell_selector.setItemText(1, _translate("CellsSettings", "Rauch"))
        self.cell_selector.setItemText(2, _translate("CellsSettings", "Sedra-Ghorab-Martin"))
        self.cell_selector.setItemText(3, _translate("CellsSettings", "Kerwin-Huelsman-Newcom"))
        self.cell_selector.setItemText(4, _translate("CellsSettings", "Tow-Thomas"))
        self.cell_selector.setItemText(5, _translate("CellsSettings", "Ackerberg-Mossber"))
        self.cell_selector.setItemText(6, _translate("CellsSettings", "Fleischer-Tow"))
        self.report_button.setText(_translate("CellsSettings", "HTML Report"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CellsSettings = QtWidgets.QWidget()
    ui = Ui_CellsSettings()
    ui.setupUi(CellsSettings)
    CellsSettings.show()
    sys.exit(app.exec_())