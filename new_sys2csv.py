#!/usr/bin/env python

import subprocess, time
import pd_system
import argparse
from pathlib import Path

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("partition_list", help="List of system partitions. Each system is comprised of teams, or tournaments.", type=list)
parser.add_argument("-g", "--game", help="Name of game type, (R,P,S,T)", choices=['stag', 'uncon'])
args = parser.parse_args()
PARTITION_LIST = args.partition_list
GAME = args.game

print("partition list: ", PARTITION_LIST)
print("Game: ", GAME)

Path('Data/Desk/').mkdir(parents=True, exist_ok=True)

for num, partition in enumerate(PARTITION_LIST):
    new_sys = pd_system.PdSystem(partition, GAME)
    new_sys.compute_data()
    new_sys.save_data('Data/Desk/')
