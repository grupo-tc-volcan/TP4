# Third-party modules
import scipy.signal as ss

from sympy.solvers import solve
from sympy import Symbol

import math

class SecondOrderAuxCalc():
    def __init__(self, transfer_function : ss.ZerosPolesGain = ss.ZerosPolesGain()):
        self.tf = transfer_function

        # Obtaining real and imaginary part of all zeros and poles in the transfer function
        self.poles_real_part = [pole.real for pole in self.tf.poles]
        self.poles_imag_part = [pole.imag for pole in self.tf.poles]
        self.zeros_real_part = [zero.real for zero in self.tf.zeros]
        self.zeros_imag_part = [zero.imag for zero in self.tf.zeros]

        # Obtaining wp and q for poles, and w0 and Q for zeros, the aux is because some will be repeated since there should be conjugated complex roots
        q = Symbol('q')
        aux_q_poles = [abs(solve((self.poles_real_part[i]*2*q) * (1 - (1/(2*q)**2)**(1/2) - self.poles_imag_part[i], q))) for i in range(len(self.poles_real_part))]
        aux_wp_poles = [2*self.poles_real_part[i]*aux_q_poles[i] for i in range(len(self.poles_real_part))]
        aux_q_zeros = [abs(solve((self.zeros_real_part[i]*2*q) * (1 - (1/(2*q)**2)**(1/2) - self.zeros_imag_part[i], q))) for i in range(len(self.zeros_real_part))]
        aux_w0_zeros = [2*self.zeros_real_part[i]*aux_q_zeros[i] for i in range(len(self.zeros_real_part))]

        # Now repeated Q and wp or w0 will be deleted, and all of them will be loaded in second order cells
        self.pole_blocks = []
        for i in range(aux_wp_poles):
            if all(not math.isclose(aux_wp_poles[i], other_wp) for other_wp in aux_wp_poles):
                # If there are no matches, it means this Q belongs to a first order pole
                new_first_order_block = {
                    'wp' : aux_wp_poles[i],
                    'n' : 1
                }
                self.pole_blocks.append(new_first_order_block)
            else:
                # If there is a match, it means this Q belongs to a second order pole
                if all(not math.isclose(aux_wp_poles[i], self.pole_blocks[j]['q']) for j in range(len(self.pole_blocks))):
                    # If this Q has not been added already
                    new_second_order_block = {
                        'wp' : aux_wp_poles[i],
                        'q' : aux_q_poles[i],
                        'n' : 2
                    }
                    self.pole_blocks.append(new_second_order_block)

        self.zero_blocks = []
        for i in range(aux_w0_zeros):
            if all(not math.isclose(aux_w0_zeros[i], other_wp) for other_wp in aux_w0_zeros):
                # If there are no matches, it means this Q belongs to a first order zero
                new_first_order_block = {
                    'w0' : aux_w0_zeros[i],
                    'n' : 1
                }
                self.zero_blocks.append(new_first_order_block)
            else:
                # If there is a match, it means this Q belongs to a second order zero
                if all(not math.isclose(aux_w0_zeros[i], self.zero_blocks[j]['q']) for j in range(len(self.zero_blocks))):
                    # If this Q has not been added already
                    new_second_order_block = {
                        'w0' : aux_w0_zeros[i],
                        'q' : aux_q_zeros[i],
                        'n' : 2
                    }
                    self.zero_blocks.append(new_second_order_block)
    

    def get_wp_poles(self):
        return [self.pole_blocks[i]['wp'] for i in range(len(self.pole_blocks))]


    def get_first_order_wp_poles(self):
        ret = []
        for pole_block in self.pole_blocks:
            if pole_block['n'] == 1:
                ret.append(pole_block['wp'])

        return ret


    def get_second_order_wp_poles(self):
        ret = []
        for pole_block in self.pole_blocks:
            if pole_block['n'] == 2:
                ret.append(pole_block['wp'])

        return ret


    def get_q_poles(self):
        ret = []
        for pole_block in self.pole_blocks:
            if pole_block['n'] == 2:
                ret.append(pole_block['q'])

        return ret


    def get_w0_zeros(self):
        return [self.zero_blocks[i]['w0'] for i in range(len(self.zero_blocks))]


    def get_first_order_w0_zeros(self):
        ret = []
        for zero_block in self.zero_blocks:
            if zero_block['n'] == 1:
                ret.append(zero_block['w0'])

        return ret


    def get_second_order_w0_zeros(self):
        ret = []
        for zero_block in self.zero_blocks:
            if zero_block['n'] == 2:
                ret.append(zero_block['w0'])

        return ret


    def get_q_zeros(self):
        ret = []
        for zero_block in self.zero_blocks:
            if zero_block['n'] == 2:
                ret.append(zero_block['q'])

        return ret