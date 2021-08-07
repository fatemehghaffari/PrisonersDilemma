import random
from itertools import combinations

def partitions(set_array, subset_size):
    """
    Generates partition sets of the input list with the given subset_size.
    
        Parameters:
            set_array (list): list of elements, or set, to be partitioned
            subset_size (int): size (k) of uniform partitions
        
        Returns:
            (iterator) : yields a partition set of k-sized subsets
    """
    if len(set_array) == 0:
        yield []
    else:
        random_strategy = random.choice(set_array)
        set_A = set(set_array)
        singleton = {random_strategy}  
        
        for S in list(combinations(set_A-singleton, subset_size-1)):
            X = set(S) | singleton  # X is a 'partition set'  
            for P in partitions(list(set_A - X), subset_size):
                yield P+[tuple(X)]
