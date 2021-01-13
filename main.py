#!/usr/bin/env python

import pd_exp
from helper_funcs import partitions
from settings import player_names
import time

start_time = time.time()

print('creating partitions')
part_list = list(partitions(player_names[:16],4))

print('running PD Exp')
classic_pdExp = pd_exp.PdExp(part_list[:1])
#stag_pdExp = pd_exp.PdExp(part_list,game=settings.stag)
#unconv_pdExp = pd_exp.PdExp(part_list,game=settings.high_t)

print('Running experiments and computing data')
classic_pdExp.run_experiments()
#stag_pdExp.run_experiments()
#unconv_pdExp.run_experiments()

print('NOT Saving experiment data')
path = 'Data/Experiment2/'
#classic_pdExp.save_data(path, 'Delete_this_ClassicPD_4x4_16uniq')
#stag_pdExp.save_data(path, 'StagHunt_4x4_16uniq')
#unconv_pdExp.save_data(path,'UnconvPD_4x4_16uniq')

print("--- %s seconds ---" % (time.time() - start_time))

#print('creating tournament')
#test_run = PdTournament(tuple(settings.one_mem_players[:4]))
#print('running tournament')
#test_run.run_tournament()
#print('saving tournament data')
#test_run.save_data('delete_this_file')
    
