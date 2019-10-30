class AutomaticCascader():
    def __init__(self):
        self.poles = []
        self.zeros = []
        self.total_gain = 0

        self.stages = []


    def separate_in_stages(self):
        if self.poles:
            # Checking that there is at least one pole
            fp_list = [pole['fp'] for pole in self.poles]
            f0_list = [zero['f0'] for zero in self.zeros]

            best_combination = []
            if len(fp_list) > len(f0_list):
                # Completing zeros list so that they are the same size
                aux_zeros = list(f0_list)
                aux_zeros.extend([None] * (len(fp_list) - len(f0_list)))
                min_dist, best_combination = self.recursive_shortest_sum_of_distances(fp_list, aux_zeros)

            for pole_zero_couple in best_combination:
                # Creating cell block
                new_stage_data = {
                    'pole': None,
                    'zero': None,
                    'gain': 0,
                    'type': ''
                }

                aux_poles = list(self.poles)
                aux_zeros = list(self.zeros)
                
                for pole in self.poles:
                    if pole['fp'] == pole_zero_couple[0]:
                        #Finding matching pole
                        new_stage_data['pole'] = pole
                        self.poles.remove(pole)
                        
                        if pole_zero_couple[1] is not None:
                            for zero in self.zeros:
                                if zero['f0'] == pole_zero_couple[1]:
                                    #Finding matching zero
                                    new_stage_data['zero'] = zero
                                    self.zeros.remove(zero)
                
                self.stages.append(new_stage_data)


    def recursive_shortest_sum_of_distances(self, poles : list, zeros : list) -> int:
        combinations = {}

        if len(poles) > 2:
            for zero in zeros:
                if zero is None:
                    dist_from_pole_to_zero = 0
                else:
                    dist_from_pole_to_zero = abs(poles[0] - zero)
                remaining_poles = list(poles)
                remaining_poles.remove(remaining_poles[0])
                remaining_zeros = list(zeros)
                remaining_zeros.remove(zero)

                min_distance, min_combination = self.recursive_shortest_sum_of_distances(remaining_poles, remaining_zeros)
                new_distance = dist_from_pole_to_zero + min_distance
                new_combinations = list(min_combination)
                new_combinations.append([poles[0], zero])

                combinations[new_distance] = new_combinations
            
        else:
            if zeros[0] is None:
                dist_0_0 = dist_1_0 = 0
            else:
                dist_0_0 = abs(poles[0] - zeros[0])
                dist_1_0 = abs(poles[1] - zeros[0])

            if zeros[1] is None:
                dist_0_1 = dist_1_1 = 0
            else:
                dist_0_1 = abs(poles[0] - zeros[1])
                dist_1_1 = abs(poles[1] - zeros[1])
                
            combinations[dist_0_0 + dist_1_1] = [[poles[0], zeros[0]], [poles[1], zeros[1]]]
            combinations[dist_0_1 + dist_1_0] = [[poles[0], zeros[1]], [poles[1], zeros[0]]]

        min_distance = min(combinations.keys())

        return min_distance, combinations[min_distance]
