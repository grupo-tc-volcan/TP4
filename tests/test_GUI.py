# third-party modules
import PyQt5.QtWidgets as QtWid

import scipy.signal as ss
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

# filters-tool project modules
from app.designer.main_view.main_view_imp import MainView
from app.plotter.plotter import FilterPlotter

def test_main_view():
    app = QtWid.QApplication([])
    view = MainView()
    view.show()
    app.exec()

def test_plot_attenuation():
    tf = ss.ZerosPolesGain([2*np.pi * 10, 2*np.pi * 20], [2*np.pi * 30, 2*np.pi * 40], 10)
    norm_tf = ss.ZerosPolesGain([2*np.pi, 2*np.pi * 2], [2*np.pi * 3, 2*np.pi * 4], 1)
    my_plotter = FilterPlotter(tf, norm_tf, 'low-pass')
    my_plotter.plot_attenuation()
    my_plotter.canvas.draw()