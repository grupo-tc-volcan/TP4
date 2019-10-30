# filters-tool project modules
from app.cascader.cascader import AutomaticCascader

def test_recursion():
    cascader = AutomaticCascader()
    # assert(cascader.recursive_shortest_sum_of_distances([4, 2, 1], [3, 5, None]), [2, [[2, 3], [4, 5], [1, None]]])
    # assert(cascader.recursive_shortest_sum_of_distances([4, 2, 1, 10, 15], [3, 5, None, 12.5, None]), [4.5, [[4, 5], [2, 3], [15, 12.5], [1, None], [10, None]]])
    # assert(cascader.recursive_shortest_sum_of_distances([4, 2, 1], [None, 5, None]), 1)
    # assert(cascader.recursive_shortest_sum_of_distances([4, 2, 1], [None, None, None]), 0)

    cascader.poles = [{'fp': 3}, {'fp': 2}, {'fp': 1}, {'fp': 10}, {'fp': 15}]
    cascader.zeros = [{'f0': 3}, {'f0': 5}, {'f0': 12.5}]
    cascader.separate_in_stages()