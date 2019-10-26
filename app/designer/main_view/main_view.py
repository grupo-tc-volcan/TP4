# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_view.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainView(object):
    def setupUi(self, MainView):
        MainView.setObjectName("MainView")
        MainView.setEnabled(True)
        MainView.resize(1211, 778)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainView.sizePolicy().hasHeightForWidth())
        MainView.setSizePolicy(sizePolicy)
        MainView.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        MainView.setTabShape(QtWidgets.QTabWidget.Triangular)
        MainView.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainView)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.process_tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.process_tabs.setTabPosition(QtWidgets.QTabWidget.West)
        self.process_tabs.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.process_tabs.setDocumentMode(False)
        self.process_tabs.setMovable(False)
        self.process_tabs.setObjectName("process_tabs")
        self.tab_approx = QtWidgets.QWidget()
        self.tab_approx.setObjectName("tab_approx")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_approx)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.filter_selector = QtWidgets.QComboBox(self.tab_approx)
        self.filter_selector.setMaximumSize(QtCore.QSize(311, 16777215))
        self.filter_selector.setObjectName("filter_selector")
        self.filter_selector.addItem("")
        self.filter_selector.addItem("")
        self.filter_selector.addItem("")
        self.filter_selector.addItem("")
        self.filter_selector.addItem("")
        self.gridLayout_2.addWidget(self.filter_selector, 0, 0, 1, 1)
        self.template_pic = QtWidgets.QStackedWidget(self.tab_approx)
        self.template_pic.setMaximumSize(QtCore.QSize(311, 230))
        self.template_pic.setObjectName("template_pic")
        self.lp_pic = QtWidgets.QWidget()
        self.lp_pic.setObjectName("lp_pic")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.lp_pic)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.label_66 = QtWidgets.QLabel(self.lp_pic)
        self.label_66.setAlignment(QtCore.Qt.AlignCenter)
        self.label_66.setObjectName("label_66")
        self.gridLayout_12.addWidget(self.label_66, 0, 0, 1, 1)
        self.template_pic.addWidget(self.lp_pic)
        self.hp_pic = QtWidgets.QWidget()
        self.hp_pic.setObjectName("hp_pic")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.hp_pic)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.label_67 = QtWidgets.QLabel(self.hp_pic)
        self.label_67.setAlignment(QtCore.Qt.AlignCenter)
        self.label_67.setObjectName("label_67")
        self.gridLayout_13.addWidget(self.label_67, 0, 0, 1, 1)
        self.template_pic.addWidget(self.hp_pic)
        self.bp_pic = QtWidgets.QWidget()
        self.bp_pic.setObjectName("bp_pic")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.bp_pic)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.label_65 = QtWidgets.QLabel(self.bp_pic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_65.sizePolicy().hasHeightForWidth())
        self.label_65.setSizePolicy(sizePolicy)
        self.label_65.setAlignment(QtCore.Qt.AlignCenter)
        self.label_65.setObjectName("label_65")
        self.gridLayout_11.addWidget(self.label_65, 0, 0, 1, 1)
        self.template_pic.addWidget(self.bp_pic)
        self.bs_pic = QtWidgets.QWidget()
        self.bs_pic.setObjectName("bs_pic")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.bs_pic)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.label_68 = QtWidgets.QLabel(self.bs_pic)
        self.label_68.setAlignment(QtCore.Qt.AlignCenter)
        self.label_68.setObjectName("label_68")
        self.gridLayout_14.addWidget(self.label_68, 1, 0, 1, 1)
        self.template_pic.addWidget(self.bs_pic)
        self.gd_pic = QtWidgets.QWidget()
        self.gd_pic.setObjectName("gd_pic")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.gd_pic)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.label_69 = QtWidgets.QLabel(self.gd_pic)
        self.label_69.setAlignment(QtCore.Qt.AlignCenter)
        self.label_69.setObjectName("label_69")
        self.gridLayout_15.addWidget(self.label_69, 1, 0, 1, 1)
        self.template_pic.addWidget(self.gd_pic)
        self.gridLayout_2.addWidget(self.template_pic, 2, 0, 1, 2)
        self.filter_data = QtWidgets.QStackedWidget(self.tab_approx)
        self.filter_data.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filter_data.sizePolicy().hasHeightForWidth())
        self.filter_data.setSizePolicy(sizePolicy)
        self.filter_data.setMaximumSize(QtCore.QSize(311, 16777215))
        self.filter_data.setFrameShape(QtWidgets.QFrame.Panel)
        self.filter_data.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.filter_data.setObjectName("filter_data")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.filter_data.addWidget(self.page_1)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.filter_data.addWidget(self.page_3)
        self.gridLayout_2.addWidget(self.filter_data, 3, 0, 1, 2)
        self.approx_selector = QtWidgets.QComboBox(self.tab_approx)
        self.approx_selector.setMaximumSize(QtCore.QSize(311, 16777215))
        self.approx_selector.setObjectName("approx_selector")
        self.approx_selector.addItem("")
        self.approx_selector.addItem("")
        self.approx_selector.addItem("")
        self.approx_selector.addItem("")
        self.approx_selector.addItem("")
        self.approx_selector.addItem("")
        self.approx_selector.addItem("")
        self.gridLayout_2.addWidget(self.approx_selector, 0, 1, 1, 1)
        self.approx_plot = QtWidgets.QTabWidget(self.tab_approx)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.approx_plot.sizePolicy().hasHeightForWidth())
        self.approx_plot.setSizePolicy(sizePolicy)
        self.approx_plot.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.approx_plot.setAcceptDrops(False)
        self.approx_plot.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.approx_plot.setDocumentMode(False)
        self.approx_plot.setTabBarAutoHide(False)
        self.approx_plot.setObjectName("approx_plot")
        self.attenuation = QtWidgets.QWidget()
        self.attenuation.setObjectName("attenuation")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.attenuation)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.plot_1 = QtWidgets.QStackedWidget(self.attenuation)
        self.plot_1.setObjectName("plot_1")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.plot_1.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.plot_1.addWidget(self.page_2)
        self.gridLayout_3.addWidget(self.plot_1, 1, 0, 1, 1)
        self.toolbar_1 = QtWidgets.QStackedWidget(self.attenuation)
        self.toolbar_1.setMinimumSize(QtCore.QSize(0, 40))
        self.toolbar_1.setMaximumSize(QtCore.QSize(16777215, 40))
        self.toolbar_1.setObjectName("toolbar_1")
        self.toolbar_1Page1_2 = QtWidgets.QWidget()
        self.toolbar_1Page1_2.setObjectName("toolbar_1Page1_2")
        self.toolbar_1.addWidget(self.toolbar_1Page1_2)
        self.gridLayout_3.addWidget(self.toolbar_1, 2, 0, 1, 1)
        self.approx_plot.addTab(self.attenuation, "")
        self.norm_att = QtWidgets.QWidget()
        self.norm_att.setObjectName("norm_att")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.norm_att)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.plot_2 = QtWidgets.QStackedWidget(self.norm_att)
        self.plot_2.setObjectName("plot_2")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.plot_2.addWidget(self.page_4)
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.plot_2.addWidget(self.page_5)
        self.gridLayout_4.addWidget(self.plot_2, 0, 0, 1, 2)
        self.toolbar_2 = QtWidgets.QStackedWidget(self.norm_att)
        self.toolbar_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.toolbar_2.setObjectName("toolbar_2")
        self.page_16 = QtWidgets.QWidget()
        self.page_16.setObjectName("page_16")
        self.toolbar_2.addWidget(self.page_16)
        self.page_17 = QtWidgets.QWidget()
        self.page_17.setObjectName("page_17")
        self.toolbar_2.addWidget(self.page_17)
        self.gridLayout_4.addWidget(self.toolbar_2, 1, 0, 1, 1)
        self.approx_plot.addTab(self.norm_att, "")
        self.phase = QtWidgets.QWidget()
        self.phase.setObjectName("phase")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.phase)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.plot_3 = QtWidgets.QStackedWidget(self.phase)
        self.plot_3.setObjectName("plot_3")
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setObjectName("page_6")
        self.plot_3.addWidget(self.page_6)
        self.page_7 = QtWidgets.QWidget()
        self.page_7.setObjectName("page_7")
        self.plot_3.addWidget(self.page_7)
        self.gridLayout_5.addWidget(self.plot_3, 0, 0, 1, 2)
        self.toolbar_3 = QtWidgets.QStackedWidget(self.phase)
        self.toolbar_3.setMaximumSize(QtCore.QSize(16777215, 40))
        self.toolbar_3.setObjectName("toolbar_3")
        self.page_18 = QtWidgets.QWidget()
        self.page_18.setObjectName("page_18")
        self.toolbar_3.addWidget(self.page_18)
        self.page_19 = QtWidgets.QWidget()
        self.page_19.setObjectName("page_19")
        self.toolbar_3.addWidget(self.page_19)
        self.gridLayout_5.addWidget(self.toolbar_3, 1, 0, 1, 1)
        self.approx_plot.addTab(self.phase, "")
        self.group_delay = QtWidgets.QWidget()
        self.group_delay.setObjectName("group_delay")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.group_delay)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.plot_4 = QtWidgets.QStackedWidget(self.group_delay)
        self.plot_4.setObjectName("plot_4")
        self.page_8 = QtWidgets.QWidget()
        self.page_8.setObjectName("page_8")
        self.plot_4.addWidget(self.page_8)
        self.page_9 = QtWidgets.QWidget()
        self.page_9.setObjectName("page_9")
        self.plot_4.addWidget(self.page_9)
        self.gridLayout_6.addWidget(self.plot_4, 0, 0, 1, 2)
        self.toolbar_4 = QtWidgets.QStackedWidget(self.group_delay)
        self.toolbar_4.setMaximumSize(QtCore.QSize(16777215, 40))
        self.toolbar_4.setObjectName("toolbar_4")
        self.page_20 = QtWidgets.QWidget()
        self.page_20.setObjectName("page_20")
        self.toolbar_4.addWidget(self.page_20)
        self.page_21 = QtWidgets.QWidget()
        self.page_21.setObjectName("page_21")
        self.toolbar_4.addWidget(self.page_21)
        self.gridLayout_6.addWidget(self.toolbar_4, 1, 0, 1, 1)
        self.approx_plot.addTab(self.group_delay, "")
        self.poles_zeros = QtWidgets.QWidget()
        self.poles_zeros.setObjectName("poles_zeros")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.poles_zeros)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.plot_5 = QtWidgets.QStackedWidget(self.poles_zeros)
        self.plot_5.setObjectName("plot_5")
        self.page_10 = QtWidgets.QWidget()
        self.page_10.setObjectName("page_10")
        self.plot_5.addWidget(self.page_10)
        self.page_11 = QtWidgets.QWidget()
        self.page_11.setObjectName("page_11")
        self.plot_5.addWidget(self.page_11)
        self.gridLayout_7.addWidget(self.plot_5, 0, 0, 1, 2)
        self.toolbar_5 = QtWidgets.QStackedWidget(self.poles_zeros)
        self.toolbar_5.setMaximumSize(QtCore.QSize(16777215, 40))
        self.toolbar_5.setObjectName("toolbar_5")
        self.page_22 = QtWidgets.QWidget()
        self.page_22.setObjectName("page_22")
        self.toolbar_5.addWidget(self.page_22)
        self.page_23 = QtWidgets.QWidget()
        self.page_23.setObjectName("page_23")
        self.toolbar_5.addWidget(self.page_23)
        self.gridLayout_7.addWidget(self.toolbar_5, 1, 0, 1, 1)
        self.approx_plot.addTab(self.poles_zeros, "")
        self.q_factor = QtWidgets.QWidget()
        self.q_factor.setObjectName("q_factor")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.q_factor)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.plot_6 = QtWidgets.QStackedWidget(self.q_factor)
        self.plot_6.setObjectName("plot_6")
        self.page_24 = QtWidgets.QWidget()
        self.page_24.setObjectName("page_24")
        self.plot_6.addWidget(self.page_24)
        self.page_25 = QtWidgets.QWidget()
        self.page_25.setObjectName("page_25")
        self.plot_6.addWidget(self.page_25)
        self.gridLayout_8.addWidget(self.plot_6, 0, 0, 1, 2)
        self.toolbar_6 = QtWidgets.QStackedWidget(self.q_factor)
        self.toolbar_6.setMaximumSize(QtCore.QSize(16777215, 40))
        self.toolbar_6.setObjectName("toolbar_6")
        self.page_30 = QtWidgets.QWidget()
        self.page_30.setObjectName("page_30")
        self.toolbar_6.addWidget(self.page_30)
        self.page_31 = QtWidgets.QWidget()
        self.page_31.setObjectName("page_31")
        self.toolbar_6.addWidget(self.page_31)
        self.gridLayout_8.addWidget(self.toolbar_6, 1, 0, 1, 1)
        self.approx_plot.addTab(self.q_factor, "")
        self.impulse_res = QtWidgets.QWidget()
        self.impulse_res.setObjectName("impulse_res")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.impulse_res)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.plot_7 = QtWidgets.QStackedWidget(self.impulse_res)
        self.plot_7.setObjectName("plot_7")
        self.page_26 = QtWidgets.QWidget()
        self.page_26.setObjectName("page_26")
        self.plot_7.addWidget(self.page_26)
        self.page_27 = QtWidgets.QWidget()
        self.page_27.setObjectName("page_27")
        self.plot_7.addWidget(self.page_27)
        self.gridLayout_9.addWidget(self.plot_7, 0, 0, 1, 2)
        self.toolbar_7 = QtWidgets.QStackedWidget(self.impulse_res)
        self.toolbar_7.setMaximumSize(QtCore.QSize(16777215, 40))
        self.toolbar_7.setObjectName("toolbar_7")
        self.page_32 = QtWidgets.QWidget()
        self.page_32.setObjectName("page_32")
        self.toolbar_7.addWidget(self.page_32)
        self.page_33 = QtWidgets.QWidget()
        self.page_33.setObjectName("page_33")
        self.toolbar_7.addWidget(self.page_33)
        self.gridLayout_9.addWidget(self.toolbar_7, 1, 0, 1, 1)
        self.approx_plot.addTab(self.impulse_res, "")
        self.step_res = QtWidgets.QWidget()
        self.step_res.setObjectName("step_res")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.step_res)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.plot_8 = QtWidgets.QStackedWidget(self.step_res)
        self.plot_8.setObjectName("plot_8")
        self.page_28 = QtWidgets.QWidget()
        self.page_28.setObjectName("page_28")
        self.plot_8.addWidget(self.page_28)
        self.page_29 = QtWidgets.QWidget()
        self.page_29.setObjectName("page_29")
        self.plot_8.addWidget(self.page_29)
        self.gridLayout_10.addWidget(self.plot_8, 0, 0, 1, 2)
        self.toolbar_8 = QtWidgets.QStackedWidget(self.step_res)
        self.toolbar_8.setMaximumSize(QtCore.QSize(16777215, 40))
        self.toolbar_8.setObjectName("toolbar_8")
        self.page_34 = QtWidgets.QWidget()
        self.page_34.setObjectName("page_34")
        self.toolbar_8.addWidget(self.page_34)
        self.page_35 = QtWidgets.QWidget()
        self.page_35.setObjectName("page_35")
        self.toolbar_8.addWidget(self.page_35)
        self.gridLayout_10.addWidget(self.toolbar_8, 1, 0, 1, 1)
        self.approx_plot.addTab(self.step_res, "")
        self.gridLayout_2.addWidget(self.approx_plot, 0, 4, 5, 1)
        self.calculate_button = QtWidgets.QPushButton(self.tab_approx)
        self.calculate_button.setObjectName("calculate_button")
        self.gridLayout_2.addWidget(self.calculate_button, 4, 0, 1, 1)
        self.plot_template_1 = QtWidgets.QCheckBox(self.tab_approx)
        self.plot_template_1.setChecked(True)
        self.plot_template_1.setObjectName("plot_template_1")
        self.gridLayout_2.addWidget(self.plot_template_1, 4, 1, 1, 1)
        self.process_tabs.addTab(self.tab_approx, "")
        self.tab_stages = QtWidgets.QWidget()
        self.tab_stages.setObjectName("tab_stages")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.tab_stages)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.label_78 = QtWidgets.QLabel(self.tab_stages)
        self.label_78.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_78.setObjectName("label_78")
        self.gridLayout_16.addWidget(self.label_78, 0, 0, 1, 1)
        self.label_x_stages = QtWidgets.QTextEdit(self.tab_stages)
        self.label_x_stages.setMaximumSize(QtCore.QSize(100, 26))
        self.label_x_stages.setObjectName("label_x_stages")
        self.gridLayout_16.addWidget(self.label_x_stages, 0, 1, 1, 3)
        self.label_76 = QtWidgets.QLabel(self.tab_stages)
        self.label_76.setMaximumSize(QtCore.QSize(93, 16777215))
        self.label_76.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_76.setObjectName("label_76")
        self.gridLayout_16.addWidget(self.label_76, 0, 4, 1, 2)
        self.stage_plot = QtWidgets.QStackedWidget(self.tab_stages)
        self.stage_plot.setObjectName("stage_plot")
        self.page_12 = QtWidgets.QWidget()
        self.page_12.setObjectName("page_12")
        self.stage_plot.addWidget(self.page_12)
        self.page_13 = QtWidgets.QWidget()
        self.page_13.setObjectName("page_13")
        self.stage_plot.addWidget(self.page_13)
        self.gridLayout_16.addWidget(self.stage_plot, 0, 9, 7, 6)
        self.min_x_stages = QtWidgets.QDoubleSpinBox(self.tab_stages)
        self.min_x_stages.setMaximumSize(QtCore.QSize(93, 16777215))
        self.min_x_stages.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.min_x_stages.setSuffix("")
        self.min_x_stages.setDecimals(3)
        self.min_x_stages.setObjectName("min_x_stages")
        self.gridLayout_16.addWidget(self.min_x_stages, 0, 6, 1, 3)
        self.label_72 = QtWidgets.QLabel(self.tab_stages)
        self.label_72.setMaximumSize(QtCore.QSize(93, 16777215))
        self.label_72.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_72.setObjectName("label_72")
        self.gridLayout_16.addWidget(self.label_72, 1, 4, 1, 2)
        self.label_75 = QtWidgets.QLabel(self.tab_stages)
        self.label_75.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_75.setObjectName("label_75")
        self.gridLayout_16.addWidget(self.label_75, 1, 0, 1, 1)
        self.scale_x_stages = QtWidgets.QComboBox(self.tab_stages)
        self.scale_x_stages.setMaximumSize(QtCore.QSize(100, 16777215))
        self.scale_x_stages.setObjectName("scale_x_stages")
        self.scale_x_stages.addItem("")
        self.scale_x_stages.addItem("")
        self.gridLayout_16.addWidget(self.scale_x_stages, 1, 1, 1, 3)
        self.label_79 = QtWidgets.QLabel(self.tab_stages)
        self.label_79.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_79.setObjectName("label_79")
        self.gridLayout_16.addWidget(self.label_79, 2, 0, 1, 1)
        self.min_y_stages = QtWidgets.QDoubleSpinBox(self.tab_stages)
        self.min_y_stages.setMaximumSize(QtCore.QSize(93, 16777215))
        self.min_y_stages.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.min_y_stages.setSuffix("")
        self.min_y_stages.setDecimals(3)
        self.min_y_stages.setObjectName("min_y_stages")
        self.gridLayout_16.addWidget(self.min_y_stages, 2, 6, 1, 3)
        self.max_x_stages = QtWidgets.QDoubleSpinBox(self.tab_stages)
        self.max_x_stages.setMaximumSize(QtCore.QSize(93, 16777215))
        self.max_x_stages.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.max_x_stages.setSuffix("")
        self.max_x_stages.setDecimals(3)
        self.max_x_stages.setObjectName("max_x_stages")
        self.gridLayout_16.addWidget(self.max_x_stages, 1, 6, 1, 3)
        self.label_77 = QtWidgets.QLabel(self.tab_stages)
        self.label_77.setMaximumSize(QtCore.QSize(93, 16777215))
        self.label_77.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_77.setObjectName("label_77")
        self.gridLayout_16.addWidget(self.label_77, 2, 4, 1, 2)
        self.label_y_stages = QtWidgets.QTextEdit(self.tab_stages)
        self.label_y_stages.setMaximumSize(QtCore.QSize(100, 26))
        self.label_y_stages.setObjectName("label_y_stages")
        self.gridLayout_16.addWidget(self.label_y_stages, 2, 1, 1, 3)
        self.scale_y_stages = QtWidgets.QComboBox(self.tab_stages)
        self.scale_y_stages.setMaximumSize(QtCore.QSize(100, 16777215))
        self.scale_y_stages.setObjectName("scale_y_stages")
        self.scale_y_stages.addItem("")
        self.scale_y_stages.addItem("")
        self.gridLayout_16.addWidget(self.scale_y_stages, 3, 1, 1, 3)
        self.label_74 = QtWidgets.QLabel(self.tab_stages)
        self.label_74.setMaximumSize(QtCore.QSize(93, 16777215))
        self.label_74.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_74.setObjectName("label_74")
        self.gridLayout_16.addWidget(self.label_74, 3, 4, 1, 2)
        self.label_73 = QtWidgets.QLabel(self.tab_stages)
        self.label_73.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_73.setObjectName("label_73")
        self.gridLayout_16.addWidget(self.label_73, 3, 0, 1, 1)
        self.max_y_stages = QtWidgets.QDoubleSpinBox(self.tab_stages)
        self.max_y_stages.setMaximumSize(QtCore.QSize(93, 16777215))
        self.max_y_stages.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.max_y_stages.setSuffix("")
        self.max_y_stages.setDecimals(3)
        self.max_y_stages.setObjectName("max_y_stages")
        self.gridLayout_16.addWidget(self.max_y_stages, 3, 6, 1, 3)
        self.auto_scale_stages = QtWidgets.QPushButton(self.tab_stages)
        self.auto_scale_stages.setObjectName("auto_scale_stages")
        self.gridLayout_16.addWidget(self.auto_scale_stages, 4, 0, 1, 4)
        self.accumulative_plot = QtWidgets.QCheckBox(self.tab_stages)
        self.accumulative_plot.setObjectName("accumulative_plot")
        self.gridLayout_16.addWidget(self.accumulative_plot, 4, 4, 1, 2)
        self.label_70 = QtWidgets.QLabel(self.tab_stages)
        self.label_70.setObjectName("label_70")
        self.gridLayout_16.addWidget(self.label_70, 5, 0, 1, 1)
        self.poles_list = QtWidgets.QListView(self.tab_stages)
        self.poles_list.setMaximumSize(QtCore.QSize(200, 16777215))
        self.poles_list.setObjectName("poles_list")
        self.gridLayout_16.addWidget(self.poles_list, 6, 0, 1, 4)
        self.label_71 = QtWidgets.QLabel(self.tab_stages)
        self.label_71.setObjectName("label_71")
        self.gridLayout_16.addWidget(self.label_71, 5, 4, 1, 1)
        self.label_83 = QtWidgets.QLabel(self.tab_stages)
        self.label_83.setObjectName("label_83")
        self.gridLayout_16.addWidget(self.label_83, 8, 0, 1, 2)
        self.zeros_list = QtWidgets.QListView(self.tab_stages)
        self.zeros_list.setMaximumSize(QtCore.QSize(200, 16777215))
        self.zeros_list.setObjectName("zeros_list")
        self.gridLayout_16.addWidget(self.zeros_list, 6, 4, 1, 3)
        self.stages_list = QtWidgets.QColumnView(self.tab_stages)
        self.stages_list.setDragEnabled(True)
        self.stages_list.setDragDropOverwriteMode(True)
        self.stages_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.stages_list.setObjectName("stages_list")
        self.gridLayout_16.addWidget(self.stages_list, 7, 0, 1, 15)
        self.label_80 = QtWidgets.QLabel(self.tab_stages)
        self.label_80.setMaximumSize(QtCore.QSize(93, 16777215))
        self.label_80.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_80.setObjectName("label_80")
        self.gridLayout_16.addWidget(self.label_80, 8, 8, 1, 2)
        self.min_x_stages_3 = QtWidgets.QDoubleSpinBox(self.tab_stages)
        self.min_x_stages_3.setMaximumSize(QtCore.QSize(93, 16777215))
        self.min_x_stages_3.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.min_x_stages_3.setSuffix("")
        self.min_x_stages_3.setDecimals(2)
        self.min_x_stages_3.setObjectName("min_x_stages_3")
        self.gridLayout_16.addWidget(self.min_x_stages_3, 8, 10, 1, 1)
        self.max_x_stages_3 = QtWidgets.QDoubleSpinBox(self.tab_stages)
        self.max_x_stages_3.setMaximumSize(QtCore.QSize(93, 16777215))
        self.max_x_stages_3.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.max_x_stages_3.setSuffix("")
        self.max_x_stages_3.setDecimals(2)
        self.max_x_stages_3.setObjectName("max_x_stages_3")
        self.gridLayout_16.addWidget(self.max_x_stages_3, 8, 12, 1, 1)
        self.label_82 = QtWidgets.QLabel(self.tab_stages)
        self.label_82.setMaximumSize(QtCore.QSize(93, 16777215))
        self.label_82.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_82.setObjectName("label_82")
        self.gridLayout_16.addWidget(self.label_82, 8, 11, 1, 1)
        self.label_81 = QtWidgets.QLabel(self.tab_stages)
        self.label_81.setObjectName("label_81")
        self.gridLayout_16.addWidget(self.label_81, 8, 13, 1, 1)
        self.order_2 = QtWidgets.QLabel(self.tab_stages)
        self.order_2.setObjectName("order_2")
        self.gridLayout_16.addWidget(self.order_2, 8, 14, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_16.addItem(spacerItem, 8, 7, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.tab_stages)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout_16.addWidget(self.comboBox, 8, 2, 1, 1)
        self.automatic_cascade = QtWidgets.QPushButton(self.tab_stages)
        self.automatic_cascade.setObjectName("automatic_cascade")
        self.gridLayout_16.addWidget(self.automatic_cascade, 8, 4, 1, 3)
        self.process_tabs.addTab(self.tab_stages, "")
        self.tab_cells = QtWidgets.QWidget()
        self.tab_cells.setObjectName("tab_cells")
        self.gridLayout_17 = QtWidgets.QGridLayout(self.tab_cells)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.stages_list_cells = QtWidgets.QColumnView(self.tab_cells)
        self.stages_list_cells.setMaximumSize(QtCore.QSize(16777215, 233))
        self.stages_list_cells.setDragEnabled(True)
        self.stages_list_cells.setDragDropOverwriteMode(True)
        self.stages_list_cells.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.stages_list_cells.setObjectName("stages_list_cells")
        self.gridLayout_17.addWidget(self.stages_list_cells, 2, 0, 1, 2)
        self.circuits_list = QtWidgets.QColumnView(self.tab_cells)
        self.circuits_list.setDragEnabled(True)
        self.circuits_list.setDragDropOverwriteMode(True)
        self.circuits_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.circuits_list.setObjectName("circuits_list")
        self.gridLayout_17.addWidget(self.circuits_list, 0, 0, 2, 1)
        self.cells_settings = QtWidgets.QStackedWidget(self.tab_cells)
        self.cells_settings.setMaximumSize(QtCore.QSize(300, 16777215))
        self.cells_settings.setObjectName("cells_settings")
        self.page_14 = QtWidgets.QWidget()
        self.page_14.setObjectName("page_14")
        self.cells_settings.addWidget(self.page_14)
        self.page_15 = QtWidgets.QWidget()
        self.page_15.setObjectName("page_15")
        self.cells_settings.addWidget(self.page_15)
        self.gridLayout_17.addWidget(self.cells_settings, 0, 1, 1, 1)
        self.process_tabs.addTab(self.tab_cells, "")
        self.gridLayout.addWidget(self.process_tabs, 0, 1, 1, 1)
        MainView.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainView)
        self.statusbar.setObjectName("statusbar")
        MainView.setStatusBar(self.statusbar)

        self.retranslateUi(MainView)
        self.process_tabs.setCurrentIndex(0)
        self.template_pic.setCurrentIndex(0)
        self.filter_data.setCurrentIndex(0)
        self.approx_plot.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainView)

    def retranslateUi(self, MainView):
        _translate = QtCore.QCoreApplication.translate
        MainView.setWindowTitle(_translate("MainView", "Filters Tool"))
        self.filter_selector.setItemText(0, _translate("MainView", "Low-Pass"))
        self.filter_selector.setItemText(1, _translate("MainView", "High-Pass"))
        self.filter_selector.setItemText(2, _translate("MainView", "Band-Pass"))
        self.filter_selector.setItemText(3, _translate("MainView", "Band-Stop"))
        self.filter_selector.setItemText(4, _translate("MainView", "Group-Delay"))
        self.label_66.setText(_translate("MainView", "<html><head/><body><p><img src=\":/lp_template/LP_template.jpg\"/></p></body></html>"))
        self.label_67.setText(_translate("MainView", "<html><head/><body><p><img src=\":/hp_template/HP_template.jpg\"/></p></body></html>"))
        self.label_65.setText(_translate("MainView", "<html><head/><body><p><img src=\":/bp_template/BP_template.jpg\"/></p></body></html>"))
        self.label_68.setText(_translate("MainView", "<html><head/><body><p><img src=\":/bs_template/bs_template.png\"/></p></body></html>"))
        self.label_69.setText(_translate("MainView", "<html><head/><body><p><img src=\":/lp_template/LP_template.jpg\"/></p></body></html>"))
        self.approx_selector.setItemText(0, _translate("MainView", "Butterworth"))
        self.approx_selector.setItemText(1, _translate("MainView", "Chebyshev I"))
        self.approx_selector.setItemText(2, _translate("MainView", "Chebyshev II"))
        self.approx_selector.setItemText(3, _translate("MainView", "Legendre"))
        self.approx_selector.setItemText(4, _translate("MainView", "Bessel"))
        self.approx_selector.setItemText(5, _translate("MainView", "Gauss"))
        self.approx_selector.setItemText(6, _translate("MainView", "Cauer"))
        self.approx_plot.setTabText(self.approx_plot.indexOf(self.attenuation), _translate("MainView", "Attenuation"))
        self.approx_plot.setTabText(self.approx_plot.indexOf(self.norm_att), _translate("MainView", "Normalised Att."))
        self.approx_plot.setTabText(self.approx_plot.indexOf(self.phase), _translate("MainView", "Phase"))
        self.approx_plot.setTabText(self.approx_plot.indexOf(self.group_delay), _translate("MainView", "Group Delay"))
        self.approx_plot.setTabText(self.approx_plot.indexOf(self.poles_zeros), _translate("MainView", "Poles and Zeros"))
        self.approx_plot.setTabText(self.approx_plot.indexOf(self.q_factor), _translate("MainView", "Q factor"))
        self.approx_plot.setTabText(self.approx_plot.indexOf(self.impulse_res), _translate("MainView", "Impulse Response"))
        self.approx_plot.setTabText(self.approx_plot.indexOf(self.step_res), _translate("MainView", "Step Response"))
        self.calculate_button.setText(_translate("MainView", "Calculate Approximation"))
        self.plot_template_1.setText(_translate("MainView", "Plot filter\'s template"))
        self.process_tabs.setTabText(self.process_tabs.indexOf(self.tab_approx), _translate("MainView", "Filter and Approximation"))
        self.label_78.setText(_translate("MainView", "Label X"))
        self.label_76.setText(_translate("MainView", "Minimum X"))
        self.label_72.setText(_translate("MainView", "Maximum X"))
        self.label_75.setText(_translate("MainView", "Scale X"))
        self.scale_x_stages.setItemText(0, _translate("MainView", "Linear"))
        self.scale_x_stages.setItemText(1, _translate("MainView", "Logarithmic"))
        self.label_79.setText(_translate("MainView", "Label Y"))
        self.label_77.setText(_translate("MainView", "Minimum Y"))
        self.scale_y_stages.setItemText(0, _translate("MainView", "Linear"))
        self.scale_y_stages.setItemText(1, _translate("MainView", "Logarithmic"))
        self.label_74.setText(_translate("MainView", "Maximum Y"))
        self.label_73.setText(_translate("MainView", "Scale Y"))
        self.auto_scale_stages.setText(_translate("MainView", "Auto Scale"))
        self.accumulative_plot.setText(_translate("MainView", "Acumulative"))
        self.label_70.setText(_translate("MainView", "<html><head/><body><p><span style=\" font-size:14pt;\">Poles:</span></p></body></html>"))
        self.label_71.setText(_translate("MainView", "<html><head/><body><p><span style=\" font-size:14pt;\">Zeros:</span></p></body></html>"))
        self.label_83.setText(_translate("MainView", "Input signal type:"))
        self.label_80.setText(_translate("MainView", "<html><head/><body><p align=\"right\"><span style=\" font-size:10pt;\">V</span><span style=\" font-size:10pt; vertical-align:sub;\">min</span></p></body></html>"))
        self.label_82.setText(_translate("MainView", "<html><head/><body><p align=\"right\"><span style=\" font-size:10pt;\">V</span><span style=\" font-size:10pt; vertical-align:sub;\">max</span></p></body></html>"))
        self.label_81.setText(_translate("MainView", "<html><head/><body><p align=\"right\"><span style=\" font-size:10pt;\">DR</span><span style=\" font-size:10pt; vertical-align:sub;\">TOTAL</span><span style=\" font-size:10pt;\">:</span></p></body></html>"))
        self.order_2.setText(_translate("MainView", "<html><head/><body><p><span style=\" font-size:10pt;\">40dB</span></p></body></html>"))
        self.comboBox.setItemText(0, _translate("MainView", "Standard"))
        self.comboBox.setItemText(1, _translate("MainView", "High"))
        self.comboBox.setItemText(2, _translate("MainView", "Low"))
        self.automatic_cascade.setText(_translate("MainView", "Automatic Cascade"))
        self.process_tabs.setTabText(self.process_tabs.indexOf(self.tab_stages), _translate("MainView", "Stages"))
        self.process_tabs.setTabText(self.process_tabs.indexOf(self.tab_cells), _translate("MainView", "Cells"))
from app.designer.resources import BP_template
from app.designer.resources import BS_template
from app.designer.resources import HP_template
from app.designer.resources import LP_template


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainView = QtWidgets.QMainWindow()
    ui = Ui_MainView()
    ui.setupUi(MainView)
    MainView.show()
    sys.exit(app.exec_())
