import axelrod as axl
from axelrod.action import Action
# Filter to extract all deterministic and memory-one strategies
filterset = {
        'stochastic': False,
       # 'memory_depth': 1
        'min_memory_depth': 0,
        'max_memory_depth': 1
        }

strategies = axl.filtered_strategies(filterset)

# Reduce 30 strategies down to 12 - pre-selected 
# If using original library - strategy_list and common_strategies will have to 
# be adjusted to match original library (these listsare designed for modified 
# library).
# strategy_list = strategies[:3] + strategies[4:6] + strategies[10:12] + [strategies[14]] \
#                 + [strategies[18],  strategies[23],  strategies[26], strategies[28]]

# New list of just popular strategies - Defector, Stubborn Coop (aka GRIM),
#  Suspicious Tit for Tat, and Tit For Tat 
# common_strategies = [strategies[11], strategies[14], strategies[18], strategies[23]] 

# Create a list of players that correspond to each of the strategies
one_mem_players = [s() for s in strategies]  # list of strategy types - change out list for different 
                                                    # experiments: strategies (full list), strategy_list (12 strats)
                                                    # common_strategies (4 strategies)
player_names = [n.name for n in one_mem_players]  # list of strings - names

name_strategy_dict = dict()  # dictionary that maps string names to corresponding
                             # strategy
for name, player in zip(player_names, one_mem_players):
    name_strategy_dict[name]=player

C,D = Action.C, Action.D
action_map={0: D, 1: C}

# Cooperators
bitter_coop = axl.MemoryOnePlayer(tuple([1,0,1,1]),action_map[1])
coop = axl.MemoryOnePlayer(tuple([1, 1, 1, 1]),action_map[1])
fourteen_coop = axl.MemoryOnePlayer(tuple([1,1,1,0]),action_map[1])
grim_trigger = axl.MemoryOnePlayer(tuple([1,0,0,0]),action_map[1])
thirteen_coop = axl.MemoryOnePlayer(tuple([1,1,0,1]),action_map[1])
tit_for_tat = axl.MemoryOnePlayer(tuple([1,0,1,0]),action_map[1])
win_stay_lose_shift = axl.MemoryOnePlayer(tuple([1,0,0,1]),action_map[1])

Coop_strategy_dict = {'Bitter Cooperator' : bitter_coop, 'Cooperator' : coop, 'Fourteen Coop' : fourteen_coop, 'Grim Trigger' : grim_trigger,
              'Thirteen Coop' : thirteen_coop, 'Tit For Tat' : tit_for_tat, 'Win-Stay Lose-Shift' : win_stay_lose_shift}

player_names = list(Coop_strategy_dict.keys())
defector = axl.MemoryOnePlayer(tuple([0, 0, 0, 0]),action_map[0])
fourteen_defect = axl.MemoryOnePlayer(tuple([1,1,1,0]),action_map[0])
stubborn_defect = axl.MemoryOnePlayer(tuple([1,0,0,0]),action_map[0])
suspicious_tit_for_tat = axl.MemoryOnePlayer(tuple([1,0,1,0]),action_map[0])
sucker_defect = axl.MemoryOnePlayer(tuple([0,1,0,0]),action_map[0])
two_defect = axl.MemoryOnePlayer(tuple([0,0,1,0]),action_map[0])
win_shift_lose_stay = axl.MemoryOnePlayer(tuple([0,1,1,0]),action_map[0])
def_strategy_dict = {'Defector' : defector, 'Fourteen Defect' : fourteen_defect, 'Stubborn Defect' : stubborn_defect, 
            'Suspicious Tit For Tat' :  suspicious_tit_for_tat, 'Sucker Defect' : sucker_defect, 'Two Defect' : two_defect, 'Win-Shift Lose-Stay' : win_shift_lose_stay}
player_names = list(def_strategy_dict.keys())

CD_strategy_dict = {'Bitter Cooperator' : bitter_coop, 'Cooperator' : coop, 'Fourteen Coop' : fourteen_coop, 'Grim Trigger' : grim_trigger,
              'Thirteen Coop' : thirteen_coop, 'Tit For Tat' : tit_for_tat, 'Win-Stay Lose-Shift' : win_stay_lose_shift, 'Defector' : defector,
               'Fourteen Defect' : fourteen_defect, 'Stubborn Defect' : stubborn_defect, 'Suspicious Tit For Tat' :  suspicious_tit_for_tat, 
               'Sucker Defect' : sucker_defect, 'Two Defect' : two_defect, 'Win-Shift Lose-Stay' : win_shift_lose_stay}
player_names = list(CD_strategy_dict.keys())
# Dictionary that maps string names to decimal
name_dec_dict = dict()
for num, name in enumerate(player_names,1):
    name_dec_dict[name] = str(num)

# Game type declarations
stag = axl.game.Game(r=5, s=0, t=3, p=1)
high_t = axl.game.Game(r=3, s=0, t=7, p=1)
