# Third-party modules
import scipy.signal as ss

import numpy as np

import math

class SecondOrderAuxCalc():
    def __init__(self, transfer_function : ss.ZerosPolesGain = ss.ZerosPolesGain([],[],1)):
        self.tf = transfer_function

        # Obtaining real and imaginary part of all zeros and poles in the transfer function
        self.poles_real_part = [pole.real for pole in self.tf.poles]
        self.poles_imag_part = [pole.imag for pole in self.tf.poles]
        self.zeros_real_part = [zero.real for zero in self.tf.zeros]
        self.zeros_imag_part = [zero.imag for zero in self.tf.zeros]

        # Obtaining wp and q for poles, and w0 and Q for zeros, the aux is because some will be repeated since there should be conjugated complex roots
        aux_q_poles = []
        aux_wp_poles = []
        aux_q_zeros = []
        aux_w0_zeros = []
        for i in range(len(self.poles_real_part)):
            if self.poles_real_part[i] == 0:
                aux_q_poles.append(0)   # This is just to put a comparable value, actual Q is inf
                aux_wp_poles.append(abs(self.poles_imag_part[i]))
            elif self.poles_imag_part[i] == 0:
                aux_q_poles.append(0.5)
                aux_wp_poles.append(abs(self.poles_real_part[i]))
            else:
                self.calculate_xi(self.tf.poles[i])
                aux_q_poles.append(abs(self.calculate_selectivity(self.tf.poles[i])))
                aux_wp_poles.append(abs(self.calculate_frequency(self.tf.poles[i])))
        
        for i in range(len(self.zeros_real_part)):
            if self.zeros_real_part[i] == 0:
                aux_q_zeros.append(0)   # This is just to put a comparable value, actual Q is inf
                aux_w0_zeros.append(abs(self.zeros_imag_part[i]))
            elif self.zeros_imag_part[i] == 0:
                aux_q_zeros.append(0.5)
                aux_w0_zeros.append(abs(self.zeros_real_part[i]))
            else:
                self.calculate_xi(self.tf.zeros[i])
                aux_q_poles.append(abs(self.calculate_selectivity(self.tf.zeros[i])))
                aux_wp_poles.append(abs(self.calculate_frequency(self.tf.zeros[i])))

        # Now repeated Q and wp or w0 will be deleted, and all of them will be loaded in second order cells
        self.pole_blocks = []
        for i in range(len(aux_wp_poles)):
            list_wp_without_i = list(aux_wp_poles)
            list_wp_without_i.remove(aux_wp_poles[i])
            list_q_without_i = list(aux_q_poles)
            list_q_without_i.remove(aux_q_poles[i])
            if all([(not math.isclose(aux_wp_poles[i], other_wp)) for other_wp in list_wp_without_i]) or all([(not math.isclose(aux_q_poles[i], other_wp)) for other_wp in list_q_without_i]):
                # If there are no matches, it means this Q and wp belong to a first order pole
                new_first_order_block = {
                    'fp' : aux_wp_poles[i] / (2*math.pi),
                    'q' : 0.5,
                    'n' : 1,
                    'poles': [self.tf.poles[i]],
                    'used': False,
                    'type': 'pole'
                }
                self.pole_blocks.append(new_first_order_block)
            else:
                # If there is a match, it means this Q and wp belong to a second order pole
                if all([(not math.isclose(aux_wp_poles[i]/(2*math.pi), self.pole_blocks[j]['fp'])) for j in range(len(self.pole_blocks))]) or all([(not math.isclose(aux_q_poles[i], self.pole_blocks[j]['q'])) for j in range(len(self.pole_blocks))]):
                    # If this Q and wp have not been added already
                    new_second_order_block = {
                        'fp' : aux_wp_poles[i] / (2*math.pi),
                        'q' : aux_q_poles[i],
                        'n' : 2,
                        'poles': [self.tf.poles[i]],
                        'used': False,
                        'type': 'pole'
                    }
                    self.pole_blocks.append(new_second_order_block)
                else:
                    # Finding matching Q and wp and adding second pole
                    for pole_block in self.pole_blocks:
                        if math.isclose(aux_wp_poles[i]/(2*math.pi), pole_block['fp']) and math.isclose(aux_q_poles[i], pole_block['q']):
                            pole_block['poles'].append(self.tf.poles[i])


        self.zero_blocks = []
        for i in range(len(aux_w0_zeros)):
            if aux_w0_zeros[i]:
                # If the zero is not in the origin, it's because it's a purely imaginary zero with multiplicity greater or equal than 2
                if all([(not math.isclose(aux_w0_zeros[i]/(2*math.pi), self.zero_blocks[j]['f0'])) for j in range(len(self.zero_blocks))]) or all([(not math.isclose(aux_q_zeros[i], self.zero_blocks[j]['q'])) for j in range(len(self.zero_blocks))]):
                    # If this Q and w0 have not been added already
                    new_second_order_block = {
                        'f0' : aux_w0_zeros[i] / (2*math.pi),
                        'q' : aux_q_zeros[i],
                        'n' : 2,
                        'zeros': [self.tf.zeros[i]],
                        'used': False,
                        'type': 'zero',
                        'zero_attached': None
                    }
                    self.zero_blocks.append(new_second_order_block)
                else:
                    # Finding matching Q and w0 and adding second zero
                    for zero_block in self.zero_blocks:
                        if math.isclose(aux_w0_zeros[i]/(2*math.pi), zero_block['f0']) and math.isclose(aux_q_zeros[i], zero_block['q']):
                            if len(zero_block['zeros']) > 1:
                                # If this block already has both conjugated zeros, a new block is created
                                new_second_order_block = {
                                    'f0' : aux_w0_zeros[i] / (2*math.pi),
                                    'q' : aux_q_zeros[i],
                                    'n' : 2,
                                    'zeros': [self.tf.zeros[i]],
                                    'used': False,
                                    'type': 'zero',
                                    'zero_attached': None
                                }
                                self.zero_blocks.append(new_second_order_block)
                            else:
                                # Adding conjugated zero
                                zero_block['zeros'].append(self.tf.zeros[i])

            else:
                # If it is in the origin, it's a first degree zero.\
                new_first_order_block = {
                    'f0' : aux_w0_zeros[i] / (2*math.pi),
                    'q' : 0.5,
                    'n' : 1,
                    'zeros': [self.tf.zeros[i]],
                    'used': False,
                    'type': 'zero',
                    'zero_attached': None
                }
                self.zero_blocks.append(new_first_order_block)


    def get_wp_poles(self):
        return [self.pole_blocks[i]['fp'] for i in range(len(self.pole_blocks))]


    def get_first_order_wp_poles(self):
        ret = []
        for pole_block in self.pole_blocks:
            if pole_block['n'] == 1:
                ret.append(pole_block['fp'])

        return ret


    def get_second_order_wp_poles(self):
        ret = []
        for pole_block in self.pole_blocks:
            if pole_block['n'] == 2:
                ret.append(pole_block['fp'])

        return ret


    def get_q_poles(self):
        ret = []
        for pole_block in self.pole_blocks:
            if pole_block['n'] == 2:
                ret.append(pole_block['q'])

        return ret


    def get_w0_zeros(self):
        return [self.zero_blocks[i]['f0'] for i in range(len(self.zero_blocks))]


    def get_first_order_w0_zeros(self):
        ret = []
        for zero_block in self.zero_blocks:
            if zero_block['n'] == 1:
                ret.append(zero_block['f0'])

        return ret


    def get_second_order_w0_zeros(self):
        ret = []
        for zero_block in self.zero_blocks:
            if zero_block['n'] == 2:
                ret.append(zero_block['f0'])

        return ret


    def get_q_zeros(self):
        ret = []
        for zero_block in self.zero_blocks:
            if zero_block['n'] == 2:
                ret.append(zero_block['q'])

        return ret


    def adjust_gain(self, tf : ss.ZerosPolesGain, filter_type):
        pass
        

    @staticmethod
    def calculate_xi(root):
        k = (root.imag / root.real) ** 2
        return np.sqrt(1 / (1 + k))


    @staticmethod
    def calculate_frequency(root):
        xi = SecondOrderAuxCalc.calculate_xi(root)
        return root.real / (xi * 2 * np.pi)


    @staticmethod
    def calculate_selectivity(root):
        xi = SecondOrderAuxCalc.calculate_xi(root)
        return 1 / (2 * xi)