# Third-party modules
import scipy.signal as ss
import numpy as np

from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

class FilterPlotter():
    def __init__(self):
        self.tf = 0
        self.type = 'low-pass'
        
        # Variables to interact with Qt
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        # Arrays of data to plot:
        self.f_att = []
        self.attenuation = []
        self.f_norm_att = []
        self.norm_attenuation = []
        self.f_phase = []
        self.phase = []
        self.f_gd = []
        self.group_delay = []
        self.zeros = []
        self.poles = []
        self.f_q = []
        self.q = []
        self.t_imp_res = []
        self.impulse_response = []
        self.t_step_res = []
        self.step_response = []


    def set_transfer_function(self, transfer_function : ss.ZerosPolesGain):
        self.tf = transfer_function


    def set_filter_type(self, filter_type):
        '''
        filter_type should be one of the following:
            'low-pass', 'high-pass', 'band-pass', 'band-stop' or 'group_delay'.
        '''
        self.type = filter_type


    def plot_attenuation(self):
        # Calculating plot points
        w, mag, self.phase = ss.bode(self.tf)
        self.f_att = [2*np.pi * ang_freq for ang_freq in w]
        self.attenuation = [-magnitude for magnitude in mag]

        # Plotting attenuation
        self.axes.clear()
        self.axes.plot(self.f_att, self.attenuation)
        self.axes.set_xscale('log')
        self.axes.grid(which='major')
        self.axes.grid(which='minor')


    def plot_template(self, template = {}):
        '''
        This should only be called after plotting attenuation
        When a plot of the template is needed, the template argument should be a dictionary with the following information:
            low_pass_or_high_pass_or_group_delay_template = {
                'fp' = ...,
                'fa' = ...,
                'Ap' = ...,
                'Aa' = ...
            }
            band_pass_template = {
                'fpl' = ...,
                'fpr' = ...,
                'fal' = ...,
                'far' = ...,
                'Ap' = ...,
                'Aal' = ...,
                'Aar' = ...
            }
            band_stop_template = {
                'fpl' = ...,
                'fpr' = ...,
                'fal' = ...,
                'far' = ...,
                'Apl' = ...,
                'Apr' = ...,
                'Aa' = ...
            }
        '''
        if self.type == 'low-pass' or self.type =='group-delay':
            width = template['fp'] - min(self.f_att)
            height = max(self.attenuation) - template['Ap']
            x_start = min(self.f_att)
            y_start = template['Ap']
            pass_band_rect = patches.Rectangle((x_start, y_start), width, height, hatch='/', color='r', alpha=0.2)

            width = max(self.f_att) - template['fa']
            height = template['Aa']
            x_start = template['fa']
            y_start = 0
            stop_band_rect = patches.Rectangle((x_start, y_start), width, height, hatch='/', color='r', alpha=0.2)

            self.axes.add_patch(pass_band_rect)
            self.axes.add_patch(stop_band_rect)

        elif self.type == 'high-pass':
            width = max(self.f_att) - template['fp']
            height = max(self.attenuation) - template['Ap']
            x_start = template['fp']
            y_start = template['Ap']
            pass_band_rect = patches.Rectangle((x_start, y_start), width, height, hatch='/', color='r', alpha=0.2)

            width = template['fa'] - min(self.f_att) 
            height = template['Aa']
            x_start = min(self.f_att)
            y_start = 0
            stop_band_rect = patches.Rectangle((x_start, y_start), width, height, hatch='/', color='r', alpha=0.2)

            self.axes.add_patch(pass_band_rect)
            self.axes.add_patch(stop_band_rect)

        elif self.type == 'band-pass':
            width = template['fpr'] - template['fpl']
            height = max(self.attenuation) - template['Ap']
            x_start = template['fpl']
            y_start = template['Ap']
            pass_band_rect = patches.Rectangle((x_start, y_start), width, height, hatch='/', color='r', alpha=0.2)

            width = template['fal'] - min(self.f_att) 
            height = template['Aal']
            x_start = min(self.f_att)
            y_start = 0
            stop_band_l_rect = patches.Rectangle((x_start, y_start), width, height, hatch='/', color='r', alpha=0.2)

            width = max(self.f_att) - template['far']
            height = template['Aar']
            x_start = template['far']
            y_start = 0
            stop_band_r_rect = patches.Rectangle((x_start, y_start), width, height, hatch='/', color='r', alpha=0.2)

            self.axes.add_patch(pass_band_rect)
            self.axes.add_patch(stop_band_l_rect)
            self.axes.add_patch(stop_band_r_rect)

        elif self.type == 'band-stop':
            width = template['fpl'] - min(self.f_att)
            height = max(self.attenuation) - template['Apl']
            x_start = min(self.f_att)
            y_start = template['Apl']
            pass_band_l_rect = patches.Rectangle((x_start, y_start), width, height, hatch='/', color='r', alpha=0.2)

            width = max(self.f_att) - template['fpr']
            height = max(self.attenuation) - template['Apr']
            x_start = template['fpr']
            y_start = template['Apr']
            pass_band_r_rect = patches.Rectangle((x_start, y_start), width, height, hatch='/', color='r', alpha=0.2)

            width = template['far'] - template['fal']
            height = template['Aa']
            x_start = template['fal']
            y_start = 0
            stop_band_rect = patches.Rectangle((x_start, y_start), width, height, hatch='/', color='r', alpha=0.2)

            self.axes.add_patch(pass_band_l_rect)
            self.axes.add_patch(pass_band_r_rect)
            self.axes.add_patch(stop_band_rect)
            self.canvas.draw()


    def plot_phase(self):
        pass


    def plot_group_delay(self):
        pass


    def plot_gd_template(self, template = {}):
        '''
        When a plot of the template is needed, the template argument should be a dictionary with the following information:
            group_delay_template = {
                'ft' = ...,
                'group_delay' = ...,
                'tol' = ...
            }
        '''
        pass


    def plot_poles_and_zeros(self):
        pass


    def plot_q(self):
        pass


    def plot_impulse_response(self):
        pass


    def plot_step_response(self):
        pass