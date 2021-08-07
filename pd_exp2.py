'''
Pd_exp2: Prisoner's Dilemma Experimentation 2
==========================================

Generate data for numerously repeated Prisoner's Dilemma tournaments.

Classes:

    PdTournament
        Tournament class that defines tournament players and tournament results 
        ('data') and methods to compute and save those results.
        
Functions:

    grouper(iterable, n, fillvalue=None) -> iterable of n-sized-chunks
        Collect data into fixed-length chunks or blocks
    avg_normalised_state(object, tuple) -> float
        Returns the tournament average for given state distribution (e.g.
        (C,C), (D,D), (C,D), (D,C))

'''
from axelrod import Action, game, Tournament 
import copy
from itertools import zip_longest
import numpy as np
import pandas as pd
from pd_exp import grouper, avg_normalised_state


# # Helper Functions
# def grouper(iterable, n, fillvalue=None):
#     '''
#     Collect data into fixed-length chunks or blocks
    
#         Parameters:
#             iterable (object): an iterable type
#             n (int): integer to indicate size of blocks to group iterable units
#             fillvalue (str): if no more elements are available to create a
#             block, fillvalue is used to finish final block
        
#         Returns:
#             new-iterable (object): new-iterable that is composed of n-length 
#             blocks of the original iterable.
            
#            ex: grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
#     '''
#     args = [iter(iterable)] * n
#     return zip_longest(*args, fillvalue=fillvalue)

# def avg_normalised_state(results_obj, state_tupl):
#     '''
#     Returns the tournament average for given state distribution (e.g.
#         (C,C), (D,D), (C,D), (D,C))
    
#         Parameters:
#             results_obj (object):
#             state_tupl (tuple): player-opponent action pair that is the game 
#                 state of interest
#     '''
#     norm_state_dist = results_obj.normalised_state_distribution
#     num_of_players = len(norm_state_dist)

#     grd_ttl = 0
#     for x in norm_state_dist:
#         #  For-loop iterates through each player's stats
#         for bunch in grouper(x,num_of_players):
#             totl = 0
#             for pl in range(num_of_players):
#                 i = bunch[pl]
#                 totl += i[state_tupl]  # Each player's CC distribution (one for each opponent) is summed together
#             Ttl=totl/(num_of_players-1)  # Normalized across opponents by dividing by num_of_players-1
#         grd_ttl += Ttl
#     return grd_ttl/num_of_players  # Averaged across all players

class PdTournament:
     """
    A class to represent a tournament. 
    
    ...
    
    Attributes
    ----------
    agg_data : pandas.dataframe (object)
        placeholder for aggregate tournament results
    player_list : list
        list of strategy names that also describe the tournament players
    names : str
        single string that includes the names of all strategies/players 
        separated by comma
    game : axelrod.game (object)
        container for game matrix and scoring logic
    data : pandas.dataframe (object)
        placeholder for individual player results
    results : (object)
        output of tournament.play()
        
    Methods
    -------
    run_tournament(reps, filename=None):
        Executes a round-robin tournament with all listed players. Results are 
        computed and stored in data variable as a pandas dataframe.
    save_data(file_name):
        Saves tournament data as a csv file
    """
    def __init__(self, strategy_list, game=None, reps=1, filename=None):
        self.player_list = strategy_list
        self.names = ','.join(sorted([n.name for n in strategy_list]))
        self.game = game
        self.results = None
        # If reps=1, then data will be one row. If reps >1, then data will be multiple rows
        if filename:
            self.data, self.agg_data = self.run_tournament(reps, filename)  # df for tournament reps (individual player norm scores) and 
        else:                                                      # df for aggregate data (player averages and tournament min, averages, and cc Dist)
            self.data, self.agg_data = self.run_tournament(reps)
         

    def __repr__(self):
        return self.names

    def run_tournament(self, reps, filename=None):
        """
        Executes a round-robin tournament with all listed players. 
        
        Results are computed and stored in data variable as a pandas dataframe.
        
        Parameters
        ----------
        reps : int
            number of times to run the same tournament
        filename : str
            filename to use to save raw tournament data (default is None)
            
        Returns
        -------
        dataf : pandas.dataframe (object)
            dataframe that depicts individual player data and metrics
        agg_data : pandas.dataframe (object)
            dataframe that depicts aggregate tournament data and metrics
        """
        # Instantiate tournament object
        roster = self.player_list
        print('Instantiating tournament object with these players: ', self.names)
        tourn = Tournament(players=roster,
                                    game=self.game,
                                    prob_end=0.1,
                                    turns=30,
                                    repetitions=reps,
                                    seed=1)

        if filename:
            results = tourn.play(processes=0, filename=filename)
        else:
            results = tourn.play(processes=0)
        
        self.results = results
        
        # Collect Group Outcome Metrics
        normal_scores = results.normalised_scores
        pl_avg_norm_score = np.average(normal_scores, axis=1)
        pl_min_norm_score = np.amin(normal_scores, axis=1)
        tourn_avg_norm_cc_distribution = avg_normalised_state(results, (Action.C,Action.C))
        
        # List manipulation to identify individual players in separate columns
        pl_list =[]
        pl_dict = {}
        for num, scores in enumerate(normal_scores,1):
            pl_dict[f'P{num}_Norm_Score'] = scores
        
        ##### Included a 2nd dataframe object to track aggregate data for repeated tournaments
        agg_data_dict = {}
        for num, avg, minimum in zip(range(1,len(roster)+1), pl_avg_norm_score, pl_min_norm_score):
            agg_data_dict[f'P{num}_Avg_Norm_Score'] = [avg]
            agg_data_dict[f'P{num}_Min_Norm_Score'] = [minimum]
            
        agg_data_dict['Avg_of_PL_Scores'] = [np.average(normal_scores)]
        agg_data_dict['Min_of_PL_Scores'] = [np.amin(normal_scores)]
        agg_data_dict['Avg_CC_Distribution'] = [tourn_avg_norm_cc_distribution]

        idx = [i for i in range(1,reps+1)]

        # Store data in pandas dataframe
        dataf = pd.DataFrame(pl_dict, index=idx)
        
        # Store aggregate data in a separate dataframe
        agg_data = pd.DataFrame(agg_data_dict, index=[reps])
        #self.data = data_row
        return dataf, agg_data

    def save_data(self, file_name):
        """ Method to save tournament data as a csv file """
        
        if self.game is None:
            R,P,S,T = game.Game().RPST()
        else:
            R,P,S,T = self.game.RPST()
        
        self.data.to_csv(file_name+f'_gameRPST_{R!r}_{P!r}_{S!r}_{T!r}.csv', index=False)

