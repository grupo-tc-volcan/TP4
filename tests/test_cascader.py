# filters-tool project modules
from app.cascader.cascader import AutomaticCascader

def test_recursion():
    cascader = AutomaticCascader()
    # assert(cascader.recursive_shortest_sum_of_distances([4, 2, 1], [3, 5, None]), [2, [[2, 3], [4, 5], [1, None]]])
    # assert(cascader.recursive_shortest_sum_of_distances([4, 2, 1, 10, 15], [3, 5, None, 12.5, None]), [4.5, [[4, 5], [2, 3], [15, 12.5], [1, None], [10, None]]])
    # assert(cascader.recursive_shortest_sum_of_distances([4, 2, 1], [None, 5, None]), 1)
    # assert(cascader.recursive_shortest_sum_of_distances([4, 2, 1], [None, None, None]), 0)

    poles = [{'fp': 3, 'q': 7, 'n': 2}, 
    {'fp': 2, 'q': 0.5, 'n': 2}, 
    {'fp': 1, 'q': 12, 'n': 'low-pass'}, 
    {'fp': 10, 'q': 1, 'n': 'band-pass'}, 
    {'fp': 15, 'q': 2, 'n': 'high-pass'}]
    zeros = [{'f0': 3, 'q': 0.1}, 
    {'f0': 5, 'q': 13}, 
    {'f0': 12.5, 'q': 4}]

    cascader.set_zeros_poles_gain(zeros, poles, 0)
    cascader.separate_in_stages()
    cascader.sort_stages()