import axelrod as axl
import matplotlib.pyplot as plt
import pprint
from itertools import combinations_with_replacement 
import numpy as np

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

SUBSET_SIZE = 3

subsets = list(combinations_with_replacement(one_mem_players, SUBSET_SIZE))

results = dict()

for i in subsets:
    print(i)

# Instantiate tournament object
    tournament = axl.Tournament(
            players=i,
            prob_end=0.1,
            turns=100,
            repetitions=1,
            seed=1,
            )

    name = f"{i}".replace(',','_').replace(' ','').strip('()')
    results[f'{i}'] = tournament.play(filename=f"{name}.csv")
    print(name, 'Avg Normalised Score: ', np.average(results[f'{i}'].normalised_scores))

#print('RANKED NAMES by Median Score: ')
#for name in results.ranked_names:
#    print(name)

#print('Match lengths: ')
#pprint.pprint( results.match_lengths)

#for name, norm_score in zip(one_mem_players,results.normalised_scores):
#    print(name, ' | Normalized Score: ', norm_score)

#plot = axl.Plot(results)
#p = plot.payoff()
#p.savefig(f'test_plot.png')
#p.show()
