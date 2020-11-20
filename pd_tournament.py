#!/usr/bin/env python

import axelrod as axl
import matplotlib.pyplot as plt
import pprint
from itertools import combinations_with_replacement 
import numpy as np
import pandas as pd
import argparse

# To parse command-line argument
parser = argparse.ArgumentParser()
parser.add_argument("sample_size", help="Size of samples to run", type=int)
args = parser.parse_args()
SUBSET_SIZE = args.sample_size
print("Subset size: ", SUBSET_SIZE)

# Filter to extract all deterministic and memory-one strategies
filterset = {
        'stochastic': False,
        'min_memory_depth': 0,
        'max_memory_depth': 1
        }

strategies = axl.filtered_strategies(filterset)

# Create a list of players that correspond to each of the strategies
one_mem_players = [s() for s in strategies]
print('Number of players: ', len(one_mem_players))

def run_tournaments(sample_size, list_of_strategies):
    subsets = list(combinations_with_replacement(one_mem_players, sample_size))

    results = dict()

    for num, i in enumerate(subsets,1):
    # Instantiate tournament object
        tournament = axl.Tournament(
                players=i,
                prob_end=0.1,
                turns=100,
                repetitions=1,
                seed=1,
                )

        sorted_list = sorted([n.name for n in i])
        names = ','.join(sorted_list)
        results[f'{i}'] = tournament.play(processes=0)
        
        # Collect Group Outcome Metrics
        avg_norm_score =  np.average(results[f'{i}'].normalised_scores)
        avg_norm_coop = np.average(results[f'{i}'].normalised_cooperation)
        data = [names, avg_norm_score, avg_norm_coop]
        col = ['Tournament_Members', 'Avg_Norm_Score', 'Avg_Norm_Cooperation_Rate']
        
        # List manipulation to identify individual players in separate columns
        pl_list = list()
        for num, p in enumerate(sorted_list,1):
            pl_list.append(f'Player{num}')
        data = [data[0]]+sorted_list+data[1:]
        col = [col[0]]+pl_list+col[1:]
        # print(data)
        # print(col)

        # Store data in pandas dataframe
        data_row = pd.DataFrame([data], columns=col)
        if i == subsets[0]:
            run_data = data_row
        else:
            run_data = pd.concat([run_data,data_row])
        if num % 25 == 0:
            print(num, ' out of ', len(subsets), ' completed.')
    run_data.to_csv(f'Data/tournament_data_sample_size_{sample_size!r}.csv', index=False)


run_tournaments(SUBSET_SIZE, one_mem_players)

    
