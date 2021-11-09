import random
from itertools import combinations, permutations

# def partitions(set_array, subset_size):
#     """
#     Generates partition sets of the input list with the given subset_size.
    
#         Parameters:
#             set_array (list): list of elements, or set, to be partitioned
#             subset_size (int): size (k) of uniform partitions
        
#         Returns:
#             (iterator) : yields a partition set of k-sized subsets
#     """
#     print("sdfgfg")
#     if len(set_array) == 0:
#         yield []
#     else:
#         random_strategy = random.choice(set_array)
#         set_A = set(set_array)
#         singleton = {random_strategy}  
#         print(list(combinations(set_A-singleton, subset_size-1)))
#         for S in list(combinations(set_A-singleton, subset_size-1)):
#             X = set(S) | singleton  # X is a 'partition set'  
#             print("This is X:", X)
#             for P in partitions(list(set_A - X), subset_size):
#                 yield P+[tuple(X)]

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
        set_A = set_array
        singleton = random_strategy 
        set_A.remove(singleton)
        print(list(combinations(set_A, subset_size-1)))
        for S in list(combinations(set_A, subset_size-1)):
            X = list(S) + [singleton]  # X is a 'partition set' 
            print("Set_A: ", set_A) 
            print("This is X:", X)
            for s in S:
                if s in set_A:
                    set_A.remove(s)
            # set_A = [x for x in set_A if x not in X]
            for P in partitions(set_A, subset_size):
                yield P+[tuple(X)]

# very inefficient but work just fine
# def partitions(set_array, subset_size):
#     permuts = permutations(set_array)
#     all_parts = []
#     all_sets = []
#     for p in permuts:
#         split_points = [i for i in range(0, len(set_array), subset_size)]
#         part_list = [p[ind:ind+subset_size] for ind in split_points]
#         part_set = [frozenset(p) for p in part_list]
#         # print(part_set)
#         if set(part_set) not in all_sets:
#             all_parts.append(part_list)
#             all_sets.append(set(part_set))
#     return (all_parts)
from time import sleep
a = [1, 1, 1, 2, 2, 2]
for p in partitions(a, 2):
    print()
    sleep(3)
