# Third-party modules
import math
import numpy as np
import scipy.signal as ss
from itertools import combinations

Q_MAX_FOR_FIRST_STAGE = 1.5
Q_MIN_FOR_LAST_STAGE = 1.5
MIN_GAIN_PER_STAGE = 5
GAIN_RESOLUTION = 1

class AutomaticCascader():
    def __init__(self):
        self.poles = []
        self.zeros = []
        self.total_gain = 0
        self.total_dynamic_range = 0

        self.stages = []


    def set_zeros_poles_gain(self, z, p, g):
        self.poles = p
        self.zeros = z
        self.total_gain = g


    def separate_in_stages(self):
        self.stages.clear()
        if self.poles:
            # Checking that there is at least one pole
            fp_list = [pole['fp'] for pole in self.poles]
            f0_list = [zero['f0'] for zero in self.zeros]

            best_combination = []
            if len(fp_list) > len(f0_list):
                # Completing zeros list so that they are the same size
                aux_f0_list = list(f0_list)
                aux_f0_list.extend([None] * (len(fp_list) - len(f0_list)))
                min_dist, best_combination = self.recursive_shortest_sum_of_distances(fp_list, aux_f0_list)

            elif len(fp_list) < len(f0_list):
                # This will only happen when there are a lot of simple zeros in the origin, like in a high-pass
                for i in range(len(fp_list)):
                    if i < (len(fp_list) - 1):
                        best_combination.append([fp_list[i], [f0_list[2*i], f0_list[2*i+1]]])
                    else:
                        best_combination.append([fp_list[i], [f0_list[2*i]]])

            else:
                min_dist, best_combination = self.recursive_shortest_sum_of_distances(fp_list, f0_list)

            for pair in best_combination:
                # Creating cell block
                new_stage_data = {
                    'pole': {},
                    'zero': {},
                    'gain_data': 0,
                    'type': '',
                    'v_min_data': 0.01,
                    'v_max_data': 15
                }
                for pole in self.poles:
                    if pole['fp'] == pair[0] and not pole['used']:
                        #Finding matching pole
                        new_stage_data['pole'] = pole
                        
                        if pair[1][0] is not None:
                            if len(pair[1]) == 1:
                                for zero in self.zeros:
                                    if zero['f0'] == pair[1][0]  and not zero['used']:
                                        #Finding matching zero
                                        new_stage_data['zero'] = zero
                                        new_stage_data['zero']['used'] = True
                                        break

                            elif len(pair[1]) == 2:
                                for zero in self.zeros:
                                    if zero['f0'] == pair[1][0] and not zero['used']:
                                        #Finding matching zero
                                        new_stage_data['zero'] = zero
                                        new_stage_data['zero']['used'] = True
                                        break
                                
                                for zero in self.zeros:
                                    if zero['f0'] == pair[1][1] and not zero['used']:
                                        #Finding matching zero
                                        new_stage_data['zero']['n'] = 2
                                        new_stage_data['zero']['zeros'].append(zero['zeros'][0])
                                        new_stage_data['zero']['zero_attached'] = zero

                                        zero['used'] = True
                                        break

                        else:
                            new_stage_data['zero'] = None

                        new_stage_data['pole']['used'] = True
                        break

                self.what_am_i(new_stage_data)
                
                self.stages.append(new_stage_data)


    def sort_stages(self):
        # Sorting by Q of the poles
        self.stages = quicksort(self.stages)

        # If available, putting a low pass-stage or band-pass at the beginning and a high-pass stage at the end
        for stage in self.stages:
            if stage['pole']['q'] < Q_MAX_FOR_FIRST_STAGE and (stage['type'] == 'low-pass' or stage['type'] == 'band-pass'):
                self.stages.insert(0, self.stages.pop(self.stages.index(stage)))
                break

        rev_stages = list(self.stages)
        # This way, the cells with higher Q are going to be looked at first
        rev_stages.reverse()
        for stage in rev_stages:
            if stage['pole']['q'] > Q_MIN_FOR_LAST_STAGE and (stage['type'] == 'high-pass' or stage['type'] == 'band-pass'):
                self.stages.insert(len(self.stages) - 1, self.stages.pop(self.stages.index(stage)))
                break


    def assign_gains(self):
        # It will be considered that all stages have a minimum gain in dB of MIN_GAIN_PER_STAGE
        # Then there is a total of:
        gain_to_distribute = MIN_GAIN_PER_STAGE * len(self.stages) + self.total_gain
        # To distribute in k stages
        # Considering a resolution of the gain for each stage of GAIN_RESOLUTION
        gain_to_distribute /= GAIN_RESOLUTION
        # Finding all ways to sum gain_to_distribute with k integers
        dynamic_ranges = []
        ways = multichoose(len(self.stages), gain_to_distribute)

        # Reducing ways so that it doesn't take too long to calculate
        if len(ways) > 20:
            ways = ways[math.floor(len(ways) / 2) - 10 : math.floor(len(ways) / 2) + 10]

        for way in ways:
            aux_stages = list(self.stages)
            dynamic_ranges.append(self.calculate_total_dynamic_range(aux_stages, way))

        best_way = ways[dynamic_ranges.index(max(dynamic_ranges))]
        best_way = [way - MIN_GAIN_PER_STAGE for way in best_way]

        for i in range(len(self.stages)):
            self.stages[i]['gain_data'] = best_way[i]


    def calculate_total_dynamic_range(self, stages, gains):
        v_max = stages[-1]['v_max_data']
        v_min = stages[-1]['v_min_data']

        rev_stages = list(stages)
        # This way, the cells with higher Q are going to be looked at first
        rev_stages.reverse()
        for i in range(len(rev_stages)):
            aux_stage = dict(rev_stages[i])
            aux_stage['gain_data'] = gains[-i-1]
            aux_stage['v_max_data'] = v_max
            aux_stage['v_min_data'] = v_min
            v_max, v_min = self.calculate_v_min_v_max(aux_stage, self.max_gain_for_stage(aux_stage))

        dr = 20 * np.log10(v_max / v_min)
        return dr


    def calculate_v_min_v_max(self, stage, max_gain_in_db):
        if stage['v_max_data'] and stage['v_min_data']:
            gain = 10**(max_gain_in_db/20)

            if max_gain_in_db > 0:
                v_max = stage['v_max_data'] / gain
                v_min = stage['v_min_data']
            else:
                v_max = stage['v_max_data']
                v_min = stage['v_min_data'] / gain
            
        return v_max, v_min


    def max_gain_for_stage(self, stage):
        if stage['zero'] is None:
            zeros = []
        else:
            zeros = stage['zero']['zeros']
        poles = stage['pole']['poles']
        transfer_function = ss.ZerosPolesGain(zeros, poles, stage['gain_data'])
        w, mag, phase = ss.bode(transfer_function, n=1000)

        dmag = np.diff(mag)/np.diff(w)

        frequencies_to_check = 10
        zero_condition = 1.0e-4
        gain_needed = 0
        for i in range(len(dmag) - frequencies_to_check):
            values_checked = []
            for j in range(frequencies_to_check):
                values_checked.append(dmag[i + j])
            
            if all([value < zero_condition for value in values_checked]):
                frequency_to_evaluate = math.floor(i + frequencies_to_check/2)
                useless_1, gain_in_passband, useless_2 = ss.bode(transfer_function, [w[frequency_to_evaluate]])
                gain_in_passband = 10**(gain_in_passband/20)
                gain_needed = stage['gain_data']**2/gain_in_passband

        transfer_function == ss.ZerosPolesGain(zeros, poles, gain_needed)
        w, mag, phase = ss.bode(transfer_function, n=1000)
        return max(mag)


    def recursive_shortest_sum_of_distances(self, poles : list, zeros : list) -> int:
        combinations = {}

        if len(poles) > 2:
            for zero in zeros:
                if zero is None or poles[0] is None:
                    dist_from_pole_to_zero = np.inf
                else:
                    dist_from_pole_to_zero = abs(poles[0] - zero)
                remaining_poles = list(poles)
                remaining_poles.remove(remaining_poles[0])
                remaining_zeros = list(zeros)
                remaining_zeros.remove(zero)

                min_distance, min_combination = self.recursive_shortest_sum_of_distances(remaining_poles, remaining_zeros)
                new_distance = dist_from_pole_to_zero + min_distance
                new_combinations = list(min_combination)
                new_combinations.append([poles[0], [zero]])

                combinations[new_distance] = new_combinations
            
        else:
            if zeros[0] is None:
                dist_0_0 = dist_1_0 = np.inf
            else:
                dist_0_0 = abs(poles[0] - zeros[0])
                dist_1_0 = abs(poles[1] - zeros[0])

            if zeros[1] is None:
                dist_0_1 = dist_1_1 = np.inf
            else:
                dist_0_1 = abs(poles[0] - zeros[1])
                dist_1_1 = abs(poles[1] - zeros[1])
                
            combinations[dist_0_0 + dist_1_1] = [[poles[0], [zeros[0]]], [poles[1], [zeros[1]]]]
            combinations[dist_0_1 + dist_1_0] = [[poles[0], [zeros[1]]], [poles[1], [zeros[0]]]]

        min_distance = min(combinations.keys())

        return min_distance, combinations[min_distance]


    def what_am_i(self, stage_data):
        if stage_data['pole']['n'] == 1:
            # If it is a first degree cell, it can only be a low-pass or a high-pass
            if stage_data['zero'] is None:
                # If it doesn't have any zeros, it's a low-pass
                stage_data['type'] = 'low-pass'
            elif stage_data['zero']['n'] == 1:
                # If it has a zero, it's a high-pass
                stage_data['type'] = 'high-pass'

        elif stage_data['pole']['n'] == 2:
            # A second degree cell can either be a low-pass with no zeros, band-pass, high-pass with zeros in the origin, a notch, or low-pass and high-pass with 2 imaginary zeros
            if stage_data['zero'] is None:
                stage_data['type'] = 'low-pass'
            elif stage_data['zero']['n'] == 1:
                stage_data['type'] = 'band-pass'
            elif stage_data['zero']['n'] == 2:
                # If the zeros are both in the origin, then it's a high-pass
                if stage_data['zero']['zeros'][0] == stage_data['zero']['zeros'][1]:
                    stage_data['type'] = 'high-pass'
                else:
                    # If the zeros are not the same, it should be checked which comes first in terms of frequency, the pole or the zero
                    if np.isclose(stage_data['zero']['f0'], stage_data['pole']['fp']):
                        stage_data['type'] = 'notch'
                    elif stage_data['zero']['f0'] > stage_data['pole']['fp']:
                        stage_data['type'] = 'low-pass'
                    elif stage_data['zero']['f0'] < stage_data['pole']['fp']:
                        stage_data['type'] = 'high-pass'


def multichoose(n,k):
    if k < 0 or n < 0: return "Error"
    if not k: return [[0]*n]
    if not n: return []
    if n == 1: return [[k]]
    return [[0]+val for val in multichoose(n-1,k)] + \
        [[val[0]+1]+val[1:] for val in multichoose(n,k-1)]


def quicksort(cells_array):
    # We define our 3 arrays
    less = []
    equal = []
    greater = []

    # If the length of our cells_array is greater than 1, we perform a sort
    if len(cells_array) > 1:
        # Select our pivot, which doesn't have to be the first element of our cells_array
        pivot = cells_array[math.floor(len(cells_array)/2)]

        # Recursively go through every element of the cells_array passed in and sort appropriately
        for cell in cells_array:
            if cell['pole']['q'] < pivot['pole']['q']:
                less.append(cell)
            if cell['pole']['q'] == pivot['pole']['q']:
                equal.append(cell)
            if cell['pole']['q'] > pivot['pole']['q']:
                greater.append(cell)

        # Recursively call quicksort on gradually smaller and smaller cells_arrays until we have a sorted list.
        return quicksort(less)+equal+quicksort(greater)

    else:
        return cells_array