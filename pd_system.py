
import axelrod as axl
import numpy as np
import pandas as pd
import settings
from pd_tournament import PdTournament
import copy

class PdSystem:
    def __init__(self, team_list, game=None):
        self.game = game
        tournament_dict = dict()
        
        # Loop through team list and construct tournament instances
        # for each team. Save each team to the tournament dictionary
        for num, team in enumerate(team_list,1):
            player_list = [settings.name_strategy_dict[i] for i in team]
            new_tour = PdTournament(player_list, game)
            new_tour.run_tournament()
            tournament_dict[f'Team{num}'] = new_tour
        
        self.team_dict = tournament_dict                             
        self.data = None
        self.id = None

    def compute_data(self):
        '''
        Class method that concatenates each individual team dataframe,
        computes the system metrics, and then assigns a single dataframe to
        self.data
        '''
        first = True
        for key, value in self.team_dict.items():

            # renaming columns to tournament data frame
            df = value.data.rename(columns={'Tournament_Members': key,
                                        'Avg_Norm_Score': f'{key} Avg Score',
                                        'Min_Norm_Score': f'{key} Min Score',
                                        'Avg_Norm_CC_Distribution': f'{key} Avg CC Dist'})
            if first:
                df1 = df
                first = False
            else:
                df1 = pd.concat([df1,df], axis=1)
        
        df1.index += 1  # Initialize index from 1 instead of 0
        
        # Collect team data
        min_scores = [df1[f'{i} Min Score'].values for i in list(self.team_dict)]
        avg_scores = [df1[f'{i} Avg Score'].values for i in list(self.team_dict)]
        cc_dists = [df1[f'{i} Avg CC Dist'].values for i in list(self.team_dict)]
        
        # Compute system metrics and create new data frame
        sys_df = pd.DataFrame({'SYS MIN Score' : [np.amin(min_scores)],
                               'SYS AVG Score' : [np.average(avg_scores)],
                               'MIN of Team Avgs' : [np.amin(avg_scores)],
                               'AVG of Team Mins' : [np.average(min_scores)],
                               'SYS CC Dist AVG' : [np.average(cc_dists)],
                               'SYS CC Dist MIN' : [np.amin(cc_dists)]},
                            index=[1])

        # Concatenate two data frames
        sys_df = pd.concat([sys_df,df1], axis=1)

        # Reformat team names into decimal code to distinguish system runs
        teams_ = [df1[f'{i}'].values.tolist()[0] for i in list(self.team_dict)]
        str_list = [0 for x in range(len(teams_))]
        for num, tm in enumerate(teams_):
            str_list[num] = tm.split(',')
        str_list2 = copy.deepcopy(str_list)
        for num, lst in enumerate(str_list):
            dec_list=[settings.name_dec_dict[n] for n in lst]
            dec_list = ','.join(dec_list)
            str_list[num] = dec_list
        new_str='_'.join(str_list)
        
        self.id = new_str
        new_df = pd.DataFrame({'System ID' : [new_str]}, index=[1])
        self.data = pd.concat([new_df,sys_df], axis=1)

    def save_data(self, path_to_file):
        if self.game is None:
            R,P,S,T = axl.game.Game().RPST()
        else:
            R,P,S,T = self.game.RPST()

        self.data.to_csv(path_to_file+f'sid_{self.id}_RPST_{R!r}_{P!r}_{S!r}_{T!r}.csv')

