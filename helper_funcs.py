import random
from itertools import combinations

def partitions(set_array, subset_size):
    """
    Generator function that takes an array and integer as input and outputs an iterator
    object that yields a list of partition sets of the elements in the given list of the given size.
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
