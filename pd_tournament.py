
import axelrod as axl
from axelrod.action import Action
import numpy as np
import pandas as pd
from itertools import zip_longest

# Helper Functions
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def avg_normalised_state(results_obj, state_tupl):
    norm_state_dist = results_obj.normalised_state_distribution
    num_of_players = len(norm_state_dist)

    grd_ttl = 0
    for x in norm_state_dist:
        for bunch in grouper(x,num_of_players):
            totl = 0
            for pl in range(num_of_players):
                i = bunch[pl]
                totl += i[state_tupl]
            Ttl=totl/(num_of_players-1)
        grd_ttl += Ttl
    return grd_ttl/num_of_players


class PdTournament:
    """
    Tournament class that defines tournament players and tournament results ('data') and 
    methods to compute and save those results.
    """
    def __init__(self, strategy_list, game=None):
        self.player_list = strategy_list
        self.names = ','.join(sorted([n.name for n in list(strategy_list)]))
        self.data = None
        self.game = game

    def __repr__(self):
        return self.names

    def run_tournament(self):
        """
        Method to execute a round-robin tournament with all listed players. Results are 
        computed and stored in data variable as a pandas dataframe.  
        """
        # Instantiate tournament object
        roster = self.player_list
        print('Instantiating tournament object with these players: ', roster)
        tournament = axl.Tournament(players=roster,
                                    game=self.game,
                                    prob_end=0.1,
                                    turns=30,
                                    repetitions=1,
                                    seed=1)

        results = tournament.play(processes=0)
        
        # Collect Group Outcome Metrics
        avg_norm_score = np.average(results.normalised_scores)
        min_norm_score = np.amin(results.normalised_scores)
        avg_norm_cc_distribution = avg_normalised_state(results, (Action.C,Action.C))
        data = [self.names, 
                avg_norm_score,
                min_norm_score,
                avg_norm_cc_distribution]
        
        col = ['Tournament_Members', 
                'Avg_Norm_Score',
                'Min_Norm_Score',
                'Avg_Norm_CC_Distribution']
        
        # List manipulation to identify individual players in separate columns
        sorted_list = sorted([n.name for n in roster])
        pl_list = list()
        for num, p in enumerate(sorted_list,1):
            pl_list.append(f'Player{num}')
        data = [data[0]]+sorted_list+data[1:]
        col = [col[0]]+pl_list+col[1:]

        # Store data in pandas dataframe
        data_row = pd.DataFrame([data], columns=col)
        self.data = data_row

    def save_data(self, file_name):
        """ Method to save tournament data as a csv file """
        
        if self.game is None:
            R,P,S,T = axl.game.Game().RPST()
        else:
            R,P,S,T = self.game.RPST()
        
        self.data.to_csv(file_name+f'_gameRPST_{R!r}_{P!r}_{S!r}_{T!r}.csv', index=False)

