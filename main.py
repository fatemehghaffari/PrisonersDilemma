#!/usr/bin/env python

import axelrod as axl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
from pd_tournament import PdTournament 
from pd_system import PdSystem
from helper_funcs import partitions
import settings
import time

start_time = time.time()

print('creating partitions')
part_list = list(partitions(settings.player_names[:16],4))
print('creating one system')
test_sys = PdSystem(part_list[0])
print('Computing data')
test_sys.compute_data()
print('Saving system data')
test_sys.save_data('')

print("--- %s seconds ---" % (time.time() - start_time))

#print('creating tournament')
#test_run = PdTournament(tuple(settings.one_mem_players[:4]))
#print('running tournament')
#test_run.run_tournament()
#print('saving tournament data')
#test_run.save_data('delete_this_file')
    
