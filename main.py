#!/usr/bin/env python

import axelrod as axl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
from pd_tournament import PdTournament 
from helper_funcs import partitions
import settings

print('creating tournament')
test_run = PdTournament(tuple(settings.one_mem_players[:4]))
print('running tournament')
test_run.run_tournament()
print('saving tournament data')
test_run.save_data('delete_this_file')
    
