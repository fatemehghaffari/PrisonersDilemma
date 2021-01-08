#!/usr/bin/env python

import axelrod as axl
from axelrod.action import Action
import matplotlib.pyplot as plt
import pprint
from itertools import combinations_with_replacement, combinations 
from itertools import zip_longest
import numpy as np
import pandas as pd
import argparse
from pd_tournament import PdTournament 

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

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def avg_normalised_state(results_obj, state_tupl):
    norm_state_dist = results_obj.normalised_state_distribution
    num_of_players = len(norm_state_dist)

    grd_ttl = 0
    for x in norm_state_dist:
        for bunch in grouper(x,num_of_players):
            totl = 0
            for pl in range(num_of_players):
                i = bunch[pl]
                totl += i[state_tupl]
            Ttl=totl/(num_of_players-1)
        grd_ttl += Ttl
    return grd_ttl/num_of_players

def run_tournaments(sample_size, list_of_strategies, game=None):
    subsets = list(combinations(list_of_strategies, sample_size))

    results = dict()

    for num, i in enumerate(subsets,1):
    # Instantiate tournament object
        print('Instantiating tournament object with these players: ', i)
        tournament = axl.Tournament(
                players=i,
                game=game,
                prob_end=0.1,
                turns=30,
                repetitions=1,
                seed=1,
                )

        sorted_list = sorted([n.name for n in i])
        names = ','.join(sorted_list)
        results[f'{i}'] = tournament.play(processes=0)
        
        # Collect Group Outcome Metrics
        avg_norm_score = np.average(results[f'{i}'].normalised_scores)
        min_norm_score = np.amin(results[f'{i}'].normalised_scores)
        avg_norm_cc_distribution = avg_normalised_state(results[f'{i}'], (C,C))
        data = [names, 
                avg_norm_score,
                min_norm_score,
                avg_norm_cc_distribution]
        
        col = ['Tournament_Members', 
                'Avg_Norm_Score',
                'Min_Norm_Score',
                'Avg_Norm_CC_Distribution']
        
        if game is None:
            R,P,S,T = axl.game.Game().RPST()
        else:
            R,P,S,T = game.RPST()

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
    run_data.to_csv(f'Data/tournament_data_sample_size_{sample_size!r}_gameRPST_{R!r}_{P!r}_{S!r}_{T!r}.csv', index=False)


#run_tournaments(SUBSET_SIZE, one_mem_players, high_t)  # Games: None, stag, and high_t
print('creating tournament')
test_run = PdTournament(tuple(one_mem_players[:4]))
print('running tournament')
test_run.run_tournament()
print('saving tournament data')
test_run.save_data('delete_this_file')
    
