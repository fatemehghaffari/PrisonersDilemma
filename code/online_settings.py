# Online_settings.py
# Revised configuration to be compatible with original Axelrod Library
#

import axelrod as axl

# Filter to extract all deterministic and memory-one strategies
filterset = {
        'stochastic': False,
       # 'memory_depth': 1
        'min_memory_depth': 0,
        'max_memory_depth': 1
        }

strategies = axl.filtered_strategies(filterset)


# Create a list of players that correspond to each of the strategies
one_mem_players = [s() for s in strategies]  # list of strategy types - change out list for different 
                                             # experiments: strategies (full list)
    
player_names = [n.name for n in one_mem_players]  # list of strings - names

name_strategy_dict = dict()  # dictionary that maps string names to corresponding
                             # strategy
for name, player in zip(player_names, one_mem_players):
    name_strategy_dict[name]=player

# Dictionary that maps string names to decimal
name_dec_dict = dict()
for num, name in enumerate(player_names,1):
    name_dec_dict[name] = str(num)

# Game type declarations
stag = axl.game.Game(r=5, s=0, t=3, p=1)
high_t = axl.game.Game(r=3, s=0, t=7, p=1)