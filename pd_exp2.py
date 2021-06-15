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
        #  For-loop iterates through each player's stats
        for bunch in grouper(x,num_of_players):
            totl = 0
            for pl in range(num_of_players):
                i = bunch[pl]
                totl += i[state_tupl]  # Each player's CC distribution (one for each opponent) is summed together
            Ttl=totl/(num_of_players-1)  # Normalized across opponents by dividing by num_of_players-1
        grd_ttl += Ttl
    return grd_ttl/num_of_players  # Averaged across all players


class PdTournament:
    """
    Tournament class that defines tournament players and tournament results ('data') and 
    methods to compute and save those results.
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
        #proc_list = []
        for num, sys in enumerate(self.lp_list, 1):
            #proc = subprocess.Popen(['./new_sys2csv.py', f'{num}', f'{sys}'])
            #proc_list.append(proc)
            print('partition list: ', f'{sys!r}')

            sys_n = PdSystem(sys, self.game)
            sys_n.compute_data()

            if first:
                exp_df = sys_n.data
                first = False
            else:
                exp_df = pd.concat([exp_df, sys_n.data])
            print('***Processing number ', num)
            if (num % 100 == 0):
                self.data = exp_df
                ###### Change file_name string below when changing num of strategies (n) used or
                ###### the number of players in a team (k)
                self.save_data('Data/Desk/',f'Comb_Sys1to{num}_12strat_4plx3partitions')
                print(f'System {num} completed and batch saved!')
            if (num % 1000 == 0):
                print(f'***Reached system {num}. Progress: ', num/list_len, '%')
        self.data = exp_df
        #for proc in proc_list:
        #    try:
        #        outs, errs = proc.communicate(timeout=120)
        #        print("Errors: ", errs)
        #        print("Outs: ", outs)
        #    except subprocess.TimeoutExpired:
        #        proc.kill()
        #        print('Process killed')
        #        outs, errs = proc.communicate()
        #        print("Errors: ", errs)
        #       print("Outs: ", outs)
                
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
