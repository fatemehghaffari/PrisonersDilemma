#!/usr/bin/env python

import pd_system
import argparse
from pathlib import Path
from settings import player_names

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("list_index", help="Index of list of system partitions. Each system is comprised of teams, or tournaments.", type=int)
parser.add_argument("-g", "--game", help="Name of game type, (R,P,S,T)", choices=['stag', 'uncon'])
args = parser.parse_args()
IDX = args.list_index
GAME = args.game

print("partition list index: ", IDX)
print("Game: ", GAME)
print("players ", player_names)

Path('Data/Desk/').mkdir(parents=True, exist_ok=True)

for num, partition in enumerate(player_names[IDX]):
    print('Partition: ', partition)
    new_sys = pd_system.PdSystem(partition, GAME)
    new_sys.compute_data()
    print('Saving system number ', num)
    new_sys.save_data(f'Data/Desk/{num}_')
