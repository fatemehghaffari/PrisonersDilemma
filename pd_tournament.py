import axelrod as axl
import matplotlib.pyplot as plt
import pprint

# Filter to extract all 32 memory-one strategies
filterset = {
        'stochastic': False,
        'memory_depth': 1
        }


strategies = axl.filtered_strategies(filterset)

# Create a list of players that correspond to each of the strategies
one_mem_players = [s() for s in strategies]
print('Number of players: ', len(one_mem_players))

tournament = axl.Tournament(
        players=one_mem_players,
        prob_end=0.1,
        turns=100,
        repetitions=1,
        seed=1,
        )

results = tournament.play()

for name in results.ranked_names:
    print(name)

print('Match lengths: ')
pprint.pprint( results.match_lengths)

plot = axl.Plot(results)
p = plot.payoff()
p.savefig(f'test_plot.png')
p.show()
