
import axelrod as axl
import numpy as np
import pandas as pd

class PdSystem:
    def __init__(self, team_list, game=None):
        tournament_dict = dict()
        for num, team in enumerate(team_list,1):
            new_tour = PdTournament(team, game)
            new_tour.run_tournament()
            tournament_dict[f'team{num}'] = new_tour
        self.team_list = team_list  # List of tuples, where tuples
                                    # are teams of player strategies
        self.data = None

    def compute_data(self):
        '''
        Class method that concatenates each individual team dataframe,
        computes the system metrics, and then assigns a single dataframe to
        self.data
        '''
        pass

    def save_data(self, file_name):
        self.data.to_csv(file_name)

