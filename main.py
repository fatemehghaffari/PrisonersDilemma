#!/usr/bin/env python

import axelrod as axl
from axelrod.action import Action
import matplotlib.pyplot as plt
import pprint
from itertools import combinations_with_replacement, combinations 
import numpy as np
import pandas as pd
import argparse
from pd_tournament import PdTournament 
from helper_funcs import partitions


# To parse command-line argument
#parser = argparse.ArgumentParser()
#parser.add_argument("sample_size", help="Size of samples to run", type=int)
#args = parser.parse_args()
#SUBSET_SIZE = args.sample_size
#print("Subset size: ", SUBSET_SIZE)

# Filter to extract all deterministic and memory-one strategies
filterset = {
        'stochastic': False,
       # 'memory_depth': 1
        'min_memory_depth': 0,
        'max_memory_depth': 1
        }

strategies = axl.filtered_strategies(filterset)

# Create a list of players that correspond to each of the strategies
one_mem_players = [s() for s in strategies]
print('Number of players: ', len(one_mem_players))
print('Player list: ')
print([p.name for p in one_mem_players])

C, D = Action.C, Action.D

stag = axl.game.Game(r=5, s=0, t=3, p=1)
high_t = axl.game.Game(r=3, s=0, t=7, p=1)

#run_tournaments(SUBSET_SIZE, one_mem_players, high_t)  # Games: None, stag, and high_t
print('creating tournament')
test_run = PdTournament(tuple(one_mem_players[:4]))
print('running tournament')
test_run.run_tournament()
print('saving tournament data')
test_run.save_data('delete_this_file')
    
