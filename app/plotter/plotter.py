# Third-party modules
import scipy.signal as ss
import matplotlib as mlib

class FilterPlotter():
    def __init__(self, transfer_function : ss.ZerosPolesGain, filter_type):
        '''
        filter_type should be one of the following:
            'low-pass', 'high-pass', 'band-pass', 'band-stop' or 'group_delay'.
        '''
        self.tf = transfer_function
        self.type = filter_type

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


    def plot_attenuation(self, template = {}):
        '''
        When a plot of the template is needed, the template argument should be a dictionary with the following information:
            low_pass_or_high_pass_template = {
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
            band_pass_template = {
                'fpl' = ...,
                'fpr' = ...,
                'fal' = ...,
                'far' = ...,
                'Apl' = ...,
                'Apr' = ...,
                'Aa' = ...
            }
            group_delay_template = {
                'fa' = ...,
                'Aa' = ...
            }
        '''
        pass


    def plot_norm_attenuation(self, template = {}):
        '''
        When a plot of the template is needed, the template argument should be a dictionary with the following information:
            low_pass_or_high_pass_template = {
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
            band_pass_template = {
                'fpl' = ...,
                'fpr' = ...,
                'fal' = ...,
                'far' = ...,
                'Apl' = ...,
                'Apr' = ...,
                'Aa' = ...
            }
            group_delay_template = {
                'fa' = ...,
                'Aa' = ...
            }
        '''
        pass


    def plot_phase(self):
        pass


    def plot_group_delay(self, template={}):
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