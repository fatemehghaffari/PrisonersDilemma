#!/usr/bin/env python

import pd_exp
from helper_funcs import partitions
from pathlib import Path
from settings import player_names, stag, high_t
import time, json

### For experiment 1
part_list = tuple([tuple([player_names])])

### For experiment 2
# Checking for txt file with list of systems
#p = Path('partition_list_12_strategies_3teams_of4.txt')
#if p.exists():
#    with open(p, "r") as f:
#        part_list = json.load(f)
#else:
#    print('creating partitions and saving to file')
#    part_list = list(partitions(player_names,4))
#    p.touch()
#    with open(p, "w") as f:
#        json.dump(part_list, f)


print('Total count of systems: ',len(part_list))  #Should be 5775 for n=12 and k=4
start_time = time.time()

print('running PD Exp')
classic_pdExp = pd_exp.PdExp(part_list)
stag_pdExp = pd_exp.PdExp(part_list,game_type=stag)
unconv_pdExp = pd_exp.PdExp(part_list,game_type=high_t)

print('Running experiments and computing data')
classic_pdExp.run_experiments()
stag_pdExp.run_experiments()
unconv_pdExp.run_experiments()

print('Saving experiment data')
### For experiment 1
path = 'Data/Experiment1/'
classic_pdExp.save_data(path, 'ClassicPD_1x30_30uniq')  # CHANGE file_name string when necessary
stag_pdExp.save_data(path, 'StagHunt_1x30_30uniq')  # CHANGE file_name string when necessary
unconv_pdExp.save_data(path,'UnconvPD_1x30_30uniq')  # CHANGE file_name string when necessary


### For experiment 2
#path = 'Data/Experiment2/'
#classic_pdExp.save_data(path, 'ClassicPD_4x3_12uniq_scores')  # CHANGE file_name string when necessary
#stag_pdExp.save_data(path, 'StagHunt_4x3_12uniq_scores')  # CHANGE file_name string when necessary
#unconv_pdExp.save_data(path,'UnconvPD_4x3_12uniq_scores')  # CHANGE file_name string when necessary

print("--- %s seconds ---" % (time.time() - start_time))

#print('creating tournament')
#test_run = PdTournament(tuple(settings.one_mem_players[:4]))
#print('running tournament')
#test_run.run_tournament()
#print('saving tournament data')
#test_run.save_data('delete_this_file')
    
