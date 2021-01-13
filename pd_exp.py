from axelrod import Action, game, Tournament 
import copy
from itertools import zip_longest
import numpy as np
import pandas as pd
from pathlib import Path
import settings, subprocess


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
        self.names = ','.join(sorted([n.name for n in strategy_list]))
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
        print('Instantiating tournament object with these players: ', self.names)
        tourn = Tournament(players=roster,
                                    game=self.game,
                                    prob_end=0.1,
                                    turns=30,
                                    repetitions=1,
                                    seed=1)

        results = tourn.play(processes=0)
        
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
            R,P,S,T = game.Game().RPST()
        else:
            R,P,S,T = self.game.RPST()
        
        self.data.to_csv(file_name+f'_gameRPST_{R!r}_{P!r}_{S!r}_{T!r}.csv', index=False)

class PdSystem:
    def __init__(self, team_list, game_type=None):
        self.game = game_type
        tournament_dict = dict()
        
        # Loop through team list and construct tournament instances
        # for each team. Save each team to the tournament dictionary
        for num, team in enumerate(team_list,1):
            player_list = [settings.name_strategy_dict[i] for i in team]
            new_tour = PdTournament(player_list, game_type)
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
            R,P,S,T = game.Game().RPST()
        else:
            R,P,S,T = self.game.RPST()

        self.data.to_csv(path_to_file+f'sid_{self.id}_RPST_{R!r}_{P!r}_{S!r}_{T!r}.csv')

class PdExp:
    """
    Class object that holds list of partition sets (AKA systems of multiple teams) and runs
    experiments, collects data and saves them to csv.
    """
    def __init__(self, list_of_lp, game_type=None):
        self.lp_list = list_of_lp  # list of lists with partition sets
        self.game = game_type

    def run_experiments(self):
        first = True
        list_len = len(self.lp_list)
        proc_list = []
        for num, sys in enumerate(self.lp_list):
            proc = subprocess.Popen(['./new_sys2csv.py', f'{num}'])
            proc_list.append(proc)
            print('partition index, list: ', f'{num}', f'{sys}')

            #sys_n = PdSystem(sys)
            #sys_n.compute_data()

            #if first:
             #   exp_df = sys_n.data
              #  first = False
            #else:
             #   exp_df = pd.concat([exp_df, sys_n.data])
            print('***Processing number ', num)
            if (num % 1000 == 0):
                print(f'***Reached system {num}. Progress: ', num/list_len, '%')
        #self.data = exp_df
        for proc in proc_list:
            try:
                outs, errs = proc.communicate(timeout=15)
                print("Errors: ", errs)
                print("Outs: ", outs)
            except subprocess.TimeoutExpired:
                #proc.kill()
                #print('Process killed')
                outs, errs = proc.communicate()
                print("Errors: ", errs)
                print("Outs: ", outs)
                
    def compile_saved_data(self, path_to_directory):
        """
        Class method to retrieve saved system data frames and create one master data frame and output in csv file.  
        """
        pass

    def save_data(self, path_to_directory, descrip_name):
        # Make directory if it does not exist
        Path(path_to_directory).mkdir(parents=True, exist_ok=True)

        if self.game is None:
            R,P,S,T = game.Game().RPST()
        else:
            R,P,S,T = self.game.RPST()
        
        self.data.to_csv(path_to_directory+f'{descrip_name}_RPST_{R!r}_{P!r}_{S!r}_{T!r}.csv')
