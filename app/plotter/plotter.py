# Third-party modules
import scipy.signal as ss
import numpy as np

from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

# filters-tool project modules
from app.auxiliary_calculators.wp_w0_q import SecondOrderAuxCalc

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
        w, mag, self.phase = ss.bode(self.tf, n=10000)
        self.f_att = [ang_freq/(2*np.pi) for ang_freq in w]
        self.attenuation = [-magnitude for magnitude in mag]

        # Plotting attenuation
        self.axes.clear()
        self.axes.plot(self.f_att, self.attenuation)
        self.axes.set_xscale('log')
        self.axes.grid(which='major')
        self.axes.grid(which='minor')
        self.axes.set_xlabel('Frequency (Hz)')
        self.axes.set_ylabel('Attenuation (dB)')

        self.canvas.draw()


    def plot_template(self, template = {}):
        '''
        This should only be called after plotting attenuation
        When a plot of the template is needed, the template argument should be a dictionary with the following information:
            low_pass_or_high_pass_or_group_delay_template = {
                'G' : ...,
                'fp' : ...,
                'fa' : ...,
                'Ap' : ...,
                'Aa' : ...
            }
            band_pass_template = {
                'G' : ...,
                'fpl' : ...,
                'fpr' : ...,
                'fal' : ...,
                'far' : ...,
                'Ap' : ...,
                'Aal' : ...,
                'Aar' : ...
            }
            band_stop_template = {
                'G' : ...,
                'fpl' : ...,
                'fpr' : ...,
                'fal' : ...,
                'far' : ...,
                'Apl' : ...,
                'Apr' : ...,
                'Aa' : ...
            }
        '''
        if self.type == 'low-pass':
            width = abs(template['fp'] - min(self.f_att))
            height = abs((max(self.attenuation) - template['Ap'] + template['G']) * 1.3)
            x_start = min(self.f_att)
            y_start = template['Ap'] - template['G']
            pass_band_rect = patches.Rectangle((x_start, y_start), width, height, hatch='///', color='r', alpha=0.2)

            width = abs((max(self.f_att) - template['fa']) * 1.3)
            height = abs(template['Aa'] + template['G'])
            x_start = template['fa']
            y_start = - template['G']
            stop_band_rect = patches.Rectangle((x_start, y_start), width, height, hatch='///', color='r', alpha=0.2)

            self.axes.add_patch(pass_band_rect)
            self.axes.add_patch(stop_band_rect)

        elif self.type == 'group-delay':
            width = abs((max(self.f_att) - template['fa']) * 1.3)
            height = abs(template['Aa'] + template['G'])
            x_start = template['fa']
            y_start = - template['G']
            stop_band_rect = patches.Rectangle((x_start, y_start), width, height, hatch='///', color='r', alpha=0.2)

            self.axes.add_patch(stop_band_rect)

        elif self.type == 'high-pass':
            width = abs((max(self.f_att) - template['fp']) * 1.3)
            height = abs((max(self.attenuation) - template['Ap'] + template['G']) * 1.3)
            x_start = template['fp']
            y_start = template['Ap'] - template['G']
            pass_band_rect = patches.Rectangle((x_start, y_start), width, height, hatch='///', color='r', alpha=0.2)

            width = abs(template['fa'] - min(self.f_att))
            height = abs(template['Aa'] + template['G'])
            x_start = min(self.f_att)
            y_start = - template['G']
            stop_band_rect = patches.Rectangle((x_start, y_start), width, height, hatch='///', color='r', alpha=0.2)

            self.axes.add_patch(pass_band_rect)
            self.axes.add_patch(stop_band_rect)

        elif self.type == 'band-pass':
            width = abs(template['fpr'] - template['fpl'])
            height = abs(max(self.attenuation) - template['Ap'] + template['G'])
            x_start = template['fpl']
            y_start = template['Ap'] - template['G']
            pass_band_rect = patches.Rectangle((x_start, y_start), width, height, hatch='///', color='r', alpha=0.2)

            width = abs(template['fal'] - min(self.f_att))
            height = abs(template['Aal'] + template['G'])
            x_start = min(self.f_att)
            y_start = - template['G']
            stop_band_l_rect = patches.Rectangle((x_start, y_start), width, height, hatch='///', color='r', alpha=0.2)

            width = abs((max(self.f_att) - template['far']) * 1.3)
            height = abs(template['Aar'] + template['G'])
            x_start = template['far']
            y_start = - template['G']
            stop_band_r_rect = patches.Rectangle((x_start, y_start), width, height, hatch='///', color='r', alpha=0.2)

            self.axes.add_patch(pass_band_rect)
            self.axes.add_patch(stop_band_l_rect)
            self.axes.add_patch(stop_band_r_rect)

        elif self.type == 'band-stop':
            width = abs(template['fpl'] - min(self.f_att))
            height = abs((max(self.attenuation) - template['Apl'] + template['G']) * 1.3)
            x_start = min(self.f_att)
            y_start = template['Apl'] - template['G']
            pass_band_l_rect = patches.Rectangle((x_start, y_start), width, height, hatch='///', color='r', alpha=0.2)

            width = abs((max(self.f_att) - template['fpr']) * 1.3)
            height = abs((max(self.attenuation) - template['Apr'] + template['G']) * 1.3)
            x_start = template['fpr']
            y_start = template['Apr'] - template['G']
            pass_band_r_rect = patches.Rectangle((x_start, y_start), width, height, hatch='///', color='r', alpha=0.2)

            width = abs(template['far'] - template['fal'])
            height = abs(template['Aa'] + template['G'])
            x_start = template['fal']
            y_start = - template['G']
            stop_band_rect = patches.Rectangle((x_start, y_start), width, height, hatch='///', color='r', alpha=0.2)

            self.axes.add_patch(pass_band_l_rect)
            self.axes.add_patch(pass_band_r_rect)
            self.axes.add_patch(stop_band_rect)

        self.canvas.draw()


    def plot_phase(self):
        # Calculating plot points
        w, mag, self.phase = ss.bode(self.tf)
        self.f_phase = [ang_freq/(2*np.pi) for ang_freq in w]

        # Plotting phase
        self.axes.clear()
        self.axes.plot(self.f_phase, self.phase)
        self.axes.set_xscale('log')
        self.axes.grid(which='major')
        self.axes.grid(which='minor')
        self.axes.set_xlabel('Frequency (Hz)')
        self.axes.set_ylabel('Phase (°)')

        self.canvas.draw()


    def plot_group_delay(self):
        # Calculating plot points
        tf_as_num_and_den = ss.TransferFunction(self.tf)
        w, h = ss.freqs(tf_as_num_and_den.num, tf_as_num_and_den.den)
        self.group_delay = -np.diff(np.unwrap(np.angle(h))) / np.diff(w)
        self.f_gd = [ang_freq/(2*np.pi) for ang_freq in w]
        # Forcing both arrays to same size
        self.f_gd.pop()

        # Plotting group delay
        self.axes.clear()
        self.axes.plot(self.f_gd, self.group_delay)
        self.axes.set_xscale('log')
        self.axes.grid(which='major')
        self.axes.grid(which='minor')
        self.axes.set_xlabel('Frequency (Hz)')
        self.axes.set_ylabel('Group Delay (s)')

        self.canvas.draw()


    def plot_gd_template(self, template = {}):
        '''
        When a plot of the template is needed, the template argument should be a dictionary with the following information:
            group_delay_template = {
                'ft' : ...,
                'group_delay' : ...,
                'tol' : ...
            }
        '''
        width = abs(template['ft'] - min(self.f_gd))
        height = abs(template['group_delay'] * (100 - template['tol']) / 100) * 1e-3
        x_start = min(self.f_gd)
        y_start = 0
        group_delay_rect = patches.Rectangle((x_start, y_start), width, height, hatch='///', color='r', alpha=0.2)

        self.axes.add_patch(group_delay_rect)
        self.canvas.draw()


    def plot_poles_and_zeros(self):
        poles = {}
        zeros = {}

        for pole in self.tf.poles:
            if pole not in poles.keys():
                poles[pole] = 1
            else:
                poles[pole] += 1

        for zero in self.tf.zeros:
            if zero not in zeros.keys():
                zeros[zero] = 1
            else:
                zeros[zero] += 1

        x_poles = [pole.real for pole in self.tf.poles]
        y_poles = [pole.imag for pole in self.tf.poles]
        x_zeros = [zero.real for zero in self.tf.zeros]
        y_zeros = [zero.imag for zero in self.tf.zeros]

        self.axes.clear()
        self.axes.scatter(x_poles, y_poles, marker='x', s=80, c='red')
        self.axes.scatter(x_zeros, y_zeros, marker='o', s=80, c='blue')
        for pole in poles.keys():
            self.axes.text(pole.real, pole.imag, '  {} ({:.3E}, {:.3E})'.format(poles[pole], pole.real, pole.imag))
        for zero in zeros.keys():
            self.axes.text(zero.real, zero.imag, '  {} ({:.3E}, {:.3E})'.format(zeros[zero], zero.real, zero.imag))
        self.axes.grid(which='major')
        self.axes.grid(which='minor')
        self.axes.set_xlabel('Real part σ (Np)')
        self.axes.set_ylabel('Imaginary part jω (Hz)')
        self.axes.axvline(c='black')
        self.axes.axhline(c='black')

        self.canvas.draw()


    def plot_q(self):
        second_order_calculator = SecondOrderAuxCalc(self.tf)
        # Calculating plot points
        x = second_order_calculator.get_second_order_wp_poles()
        y = second_order_calculator.get_q_poles()

        # Plotting Q factors
        self.axes.clear()
        self.axes.plot(x, y, marker='o')
        for i_x, i_y in zip(x, y):
            self.axes.text(i_x, i_y, '  fp={:.3E}, Q={:.3E}'.format(i_x, i_y))
        self.axes.grid(which='major')
        self.axes.grid(which='minor')
        self.axes.set_xlabel('Frequency (Hz)')
        self.axes.set_ylabel('Q factors')

        self.canvas.draw()


    def plot_impulse_response(self):
        # Calculating plot points
        self.t_imp_res, self.impulse_response = ss.impulse(self.tf)

        # Plotting impulse response
        self.axes.clear()
        self.axes.plot(self.t_imp_res, self.impulse_response)
        self.axes.grid(which='major')
        self.axes.grid(which='minor')
        self.axes.set_xlabel('Time (s)')
        self.axes.set_ylabel('Impulse Response (V)')

        self.canvas.draw()


    def plot_step_response(self):
        # Calculating plot points
        self.t_step_res, self.step_response = ss.step(self.tf)

        # Plotting impulse response
        self.axes.clear()
        self.axes.plot(self.t_step_res, self.step_response)
        self.axes.grid(which='major')
        self.axes.grid(which='minor')
        self.axes.set_xlabel('Time (s)')
        self.axes.set_ylabel('Step Response (V)')

        self.canvas.draw()