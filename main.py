#!/usr/bin/env python

import pd_exp
from helper_funcs import partitions
import settings
import time

start_time = time.time()

print('creating partitions')
part_list = list(partitions(settings.player_names[:16],4))
print('running PD Exp')
test_pdExp = pd_exp.PdExp(part_list[:10])
print('Running experiments and computing data')
test_pdExp.run_experiments()
print('Saving experiment data')
test_pdExp.save_data('Data/Experiment2/', 'test_run_10_lists')

print("--- %s seconds ---" % (time.time() - start_time))

#print('creating tournament')
#test_run = PdTournament(tuple(settings.one_mem_players[:4]))
#print('running tournament')
#test_run.run_tournament()
#print('saving tournament data')
#test_run.save_data('delete_this_file')
    
