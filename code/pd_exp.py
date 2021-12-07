'''
Pd_exp: Prisoner's Dilemma Experimentation
==========================================

Generate data for numerous Prisoner's Dilemma tournaments or systems of 
tournaments.

Classes:

    PdTournament
        A class to represent a tournament.
    PdSystem 
        Generate data for multiple tournaments and organize it into a dataframe
    PdExp
        Generate data for multiple systems
        
Functions:

    grouper(iterable, n, fillvalue=None) -> iterable of n-sized-chunks
        Collect data into fixed-length chunks or blocks
    avg_normalised_state(object, tuple) -> float
        Returns the tournament average for given state distribution (e.g.
        (C,C), (D,D), (C,D), (D,C))

'''
from axelrod import Action, game, Tournament, plot
import copy
from itertools import zip_longest
import numpy as np
import pandas as pd
from pathlib import Path
import settings
import subprocess
from time import sleep


# Helper Functions
def grouper(iterable, n, fillvalue=None):
    '''
    Collect data into fixed-length chunks or blocks
    
        Parameters:
            iterable (object): an iterable type
            n (int): integer to indicate size of blocks to group iterable units
            fillvalue (str): if no more elements are available to create a
            block, fillvalue is used to finish final block
        
        Returns:
            new-iterable (object): new-iterable that is composed of n-length 
            blocks of the original iterable.
            
           ex: grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    '''
    
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def avg_normalised_state(results_obj, state_tupl):
    '''
    Returns the tournament average for given state distribution (e.g.
        (C,C), (D,D), (C,D), (D,C))
    
        Parameters:
            results_obj (object): output generated from Axelrod 
                tournament.play()
            state_tupl (tuple): player-opponent action pair that is the game 
                state of interest (e.g. (Action.C, Action.C) for mutual 
                cooperation)
                
        Returns:
            (float): average distribution of state_tupl for the tournament 
                that results_obj describes.
    '''
    
    norm_state_dist = results_obj.normalised_state_distribution
    num_of_players = len(norm_state_dist)

    grd_ttl = 0
    for x in norm_state_dist:
        for bunch in grouper(x,num_of_players):
            totl = 0
            for pl in range(num_of_players):
                i = bunch[pl]
                totl += i[state_tupl]  # Each player's CC distribution (one for
                                       # each opponent) is summed together
            
            Ttl=totl/(num_of_players-1)  # Normalized across opponents by 
                                         # dividing by num_of_players-1
        grd_ttl += Ttl
    return grd_ttl/num_of_players  # Averaged across all players

def new_avg_normalised_state(results_obj, state_tupl):
    '''
    Returns the tournament average for given state distribution (e.g.
        (C,C), (D,D), (C,D), (D,C))
    
        Parameters:
            results_obj (object): output generated from Axelrod 
                tournament.play()
            state_tupl (tuple): player-opponent action pair that is the game 
                state of interest (e.g. (Action.C, Action.C) for mutual 
                cooperation)
                
        Returns:
            (float): average distribution of state_tupl for the tournament 
                that results_obj describes.
    '''
    
    norm_state_dist = results_obj.normalised_state_distribution
    num_of_players = len(norm_state_dist)
    totl = 0
    grd_ttl = 0
    for x in norm_state_dist:
        for bunch in grouper(x,num_of_players):
            for pl in range(num_of_players):
                i = bunch[pl]
                totl += i[state_tupl]  # Each player's CC distribution (one for
                                       # each opponent) is summed together
            
            # Ttl=totl/(num_of_players-1)  # Normalized across opponents by 
        grd_ttl += totl
    return grd_ttl/num_of_players  # Averaged across all players

def sum_state(results_obj, state_tupl):
    state_dist = results_obj.state_distribution
    state_sum = 0
    # print('Counting the number of CC states:') # this
    i = 1
    for player in state_dist:
        # print('player ', i, 'states:') # this
        i += 1
        for state_counter in player:
            states = dict(state_counter)
            # print(states) # this
            try:
                state_sum += states[state_tupl]
            except:
                continue
    # print("The total number of CCs: ", state_sum) # this
    return state_sum

def CC_threshold(results_obj, state_tupl, t):
    state_dist = results_obj.state_distribution
    state_sum = 0
    i = 1
    AllSuperGames = 0
    GoodSuperGames = 0
    for player in state_dist:
        # print('player ', i, 'states:') # this
        i += 1
        for state_counter in player:
            states = dict(state_counter)
            if bool(states):
                AllSuperGames += 1
            # print("     ", states) # this
            try:
                fraction = states[state_tupl] / sum(list(states.values()))
                # print("     ", fraction)
                if fraction >= t:
                    # print("     GOOD")
                    GoodSuperGames += 1

            except:
                continue
        # sleep(10)
    fraction = GoodSuperGames / AllSuperGames
    # print("The total number of CCs: ", fraction) # this
    return fraction

class Agent:
    def __init__(self, strategy):
        self.strategy = strategy

class PdTournament:
    """
    A class to represent a tournament. 
    
    ...
    
    Attributes
    ----------
    player_list : list
        list of strategy names that also describe the tournament players
    names : str
        single string that includes the names of all strategies/players 
        separated by comma
    game : axelrod.game (object)
        container for game matrix and scoring logic
    data : pandas.dataframe (object)
        placeholder for the tournament results
        
    Methods
    -------
    run_tournament(reps=1):
        Executes a round-robin tournament with all listed players. Results are 
        computed and stored in data variable as a pandas dataframe.
    save_data(file_name):
        Saves tournament data as a csv file
    """
    
    def __init__(self, strategy_list, game=None, t = 0.5, reps=1):
        """
        Constructs all the necessary attributes for tournament object
        
        Parameters
        ----------
        player_list : list
            list of strategy names that also describe the tournament players
        game : axelrod.game (object)
            container for game matrix and scoring logic (default is None, which
            will prompt the classic PD setting)
        reps : int
            number of times to repeat tournament (default is 1)
        """
        self.CCThreshold = t
        self.player_list = strategy_list
        self.names = ','.join(sorted([n.name for n in strategy_list]))
        self.game = game
        self.data = self.run_tournament(reps)  # If reps=1, then data will be 
                                               # one row. If reps >1, then data
                                               # will be multiple rows

    def __repr__(self):
        return self.names

    def run_tournament(self, reps=1):
        """
        Executes a round-robin tournament with all listed players. 
        
        Results are computed and stored in data attribute as a pandas dataframe.
        
        Parameters
        ----------
        reps : int
            number of times to repeat tournament (default is 1)
         
        Returns
        -------
        data_row : pandas.dataframe (object)
            row representation of individual tournament results, which consists of
            tournament players, player statistics and tournament metrics
        
        """
        
        # Instantiate tournament object
        roster = self.player_list
        # print('Instantiating tournament object with these players: ', self.names) # this
        tourn = Tournament(players=roster,
                                    game=self.game,
                                    prob_end=0.1,
                                    turns=30,
                                    repetitions=reps,
                                    seed=1)

        results = tourn.play(processes=0)  
        # print("\nMatch length for each user against other users: ", results.match_lengths) # this
        sum_T = 0
        match_len = results.match_lengths
        for i in range(len(match_len)):
            srp = []
            for xi in range(len(match_len[i])):
                match_len[i][xi].pop(xi)
                srp.append(sum(match_len[i][xi]))
            sum_T = sum(srp)
        # Collect Group Outcome Metrics
        normal_scores = results.normalised_scores
        sscores = results.scores
        avg_norm_score = np.average(normal_scores)
        new_avg_norm_score = np.average(sscores)
        avg_norm_score_2 = (new_avg_norm_score * len(results.scores)) / (sum_T / 2)

        min_norm_score = np.amin(normal_scores)
        avg_norm_cc_distribution = avg_normalised_state(results, (Action.C,Action.C))
        new_avg_norm_cc_distribution = new_avg_normalised_state(results, (Action.C,Action.C))
        avg_norm_cc_distribution_2 = sum_state(results, (Action.C,Action.C)) / sum_T
        avg_CC_threshold = CC_threshold(results, (Action.C,Action.C), self.CCThreshold)
        data = [self.names, 
                avg_norm_score,
                avg_norm_score_2,
                min_norm_score,
                avg_norm_cc_distribution,
                avg_norm_cc_distribution_2,
                avg_CC_threshold]
        
        col = ['Tournament_Members', 
                'Avg_Norm_Score',
                'Avg_Norm_Score_2',
                'Min_Norm_Score',
                'Avg_Norm_CC_Distribution',
                'Avg_Norm_CC_Distribution_2',
                'Avg_CC_Threshold']
        
        # List manipulation to identify individual players in separate columns
        sorted_list = sorted([n.name for n in roster])
        pl_list = list()
        for num, p in enumerate(sorted_list,1):
            pl_list.append(f'Player{num}')
            pl_list.append(f'P{num}_Norm_Score')

        pl_data_list = list()
        for name, score in zip(sorted_list, normal_scores):
            pl_data_list.append(name)
            pl_data_list.append(score[0])

        data = [data[0]]+pl_data_list+data[1:]
        col = [col[0]]+pl_list+col[1:]

        # Store data in pandas dataframe
        data_row = pd.DataFrame([data], columns=col)
        #self.data = data_row
        return data_row

    def save_data(self, file_name):
        """ Saves tournament data as a csv file """
        
        if self.game is None:
            R,P,S,T = game.Game().RPST()
        else:
            R,P,S,T = self.game.RPST()
        self.data.to_csv(file_name+f'_gameRPST_{R!r}_{P!r}_{S!r}_{T!r}.csv', 
                  index=False)

class PdSystem:
    """
    A class to represent a system of tournaments. 
    
    ...
    
    Attributes
    ----------
    game : axelrod.game (object)
        container for game matrix and scoring logic
    data : pandas.dataframe (object)
        placeholder for system data
    id : 
    team_dict : dictionary
        container to hold team-tournament object pairs
        
    Methods
    -------
    compute_data:
        Concatenates each individual team dataframe, computes the system 
        metrics, and then assigns a single dataframe to data attribute
    save_data(file_name):
        Saves system data as a csv file
    """
    
    def __init__(self, team_list, game_type=None, t = 0.5):
        """
        Constructs all the necessary attributes for system object
        
        Parameters
        ----------
        team_list : list
            a two-dimensional list where each item of the first-dimension is a
            player_list for a single tournament
        game_type : axelrod.game (object)
            container for game matrix and scoring logic (default is None, which
            will prompt the classic PD setting)
        
        """
        self.CCThreshold = t
        self.data = None
        self.id = None
        self.game = game_type
        self.team_list = team_list
        tournament_dict = dict()
        
        # Loop through team list and construct tournament instances
        # for each team. Save each team to the tournament dictionary
        for num, team in enumerate(team_list,1):
            player_list = [settings.CD_strategy_dict[i] for i in team]
            new_tour = PdTournament(player_list, game_type, self.CCThreshold)
            tournament_dict[f'Team{num}'] = new_tour
        
        self.team_dict = tournament_dict                             
        

    def compute_data(self):
        '''
        Concatenates each individual team dataframe, computes the system 
        metrics, and then assigns a single dataframe to data attribute
        '''
        
        first = True
        for key, value in self.team_dict.items():

            # renaming columns to tournament data frame
            df = value.data.rename(columns={'Tournament_Members': key,
                                        'Avg_Norm_Score': f'{key} Avg Score',
                                        'Avg_Norm_Score_2': f'{key} New Avg Score',
                                        'Min_Norm_Score': f'{key} Min Score',
                                        'Avg_Norm_CC_Distribution': f'{key} Avg CC Dist',
                                        'Avg_Norm_CC_Distribution_2': f'{key} New Avg CC Dist',
                                        'Avg_CC_Threshold': f'{key} Avg CC Fraction'})
            if first:
                df1 = df
                first = False
            else:
                df1 = pd.concat([df1,df], axis=1)
        
        df1.index += 1  # Initialize index from 1 instead of 0
        # Collect team data
        min_scores = [df1[f'{i} Min Score'].values for i in list(self.team_dict)]
        avg_scores = [df1[f'{i} Avg Score'].values for i in list(self.team_dict)]
        new_avg_scores = [df1[f'{i} New Avg Score'].values for i in list(self.team_dict)]
        cc_dists = [df1[f'{i} Avg CC Dist'].values for i in list(self.team_dict)]
        new_cc_dists = [df1[f'{i} New Avg CC Dist'].values for i in list(self.team_dict)]
        cc_fraction = [df1[f'{i} Avg CC Fraction'].values for i in list(self.team_dict)]
        # Compute system metrics and create new data frame
        sys_df = pd.DataFrame({'SYS MIN Score' : [np.amin(min_scores)],
                               'SYS AVG Score' : [np.average(avg_scores)],
                               'MIN of Team Avgs' : [np.amin(avg_scores)],
                               'AVG of Team Mins' : [np.average(min_scores)],
                               'SYS CC Dist AVG' : [np.average(cc_dists)],
                               'SYS CC Dist MIN' : [np.amin(cc_dists)],
                               'SYS New CC Dist AVG' : [np.average(new_cc_dists)],
                               'SYS New CC Dist MIN' : [np.amin(new_cc_dists)],
                               'SYS CC Fraction AVG' : [np.average(cc_fraction)],
                               'SYS CC Fraction MIN' : [np.amin(cc_fraction)]}, index=[1])

        # Concatenate two data frames
        sys_df = pd.concat([sys_df,df1], axis=1)

        # Reformat team names into decimal code to distinguish system runs
        teams_ = [df1[f'{i}'].values.tolist()[0] for i in list(self.team_dict)]
        str_list = [0 for x in range(len(teams_))]
        for num, tm in enumerate(teams_):
            str_list[num] = tm.split(',')
        str_list2 = copy.deepcopy(str_list)
        str_list = self.team_list
        # print("str_list", str_list) # this
        # print("team list:", self.team_list) # this
        for num, lst in enumerate(str_list):
            dec_list=[settings.name_dec_dict[n] for n in lst]
            dec_list = ','.join(dec_list)
            str_list[num] = dec_list
        new_str='_'.join(str_list)
        # print('str str:' , new_str) # this
        self.id = new_str
        new_df = pd.DataFrame({'System ID' : [new_str]}, index=[1])
        self.data = pd.concat([new_df,sys_df], axis=1)

    def save_data(self, path_to_file):
        """ Saves system data as a csv file """
        
        if self.game is None:
            R,P,S,T = game.Game().RPST()
        else:
            R,P,S,T = self.game.RPST()

        self.data.to_csv(path_to_file+f'sid_{self.id}_RPST_{R!r}_{P!r}_{S!r}_{T!r}.csv')

class PdExp:
    """
    A class to represent a series of systems. 
    
    ...
    
    Attributes
    ----------
    sys_tuple : tuple
        three-dimensional ordered list, or tuple, where the first-dimension is
        a list of systems, the 2nd-dimension is the team list, and the 
        3rd-dimension is the individual players.
    game : axelrod.game (object)
        container for game matrix and scoring logic 
 
    Methods
    -------
    run_experiments:
        Iterates through each system, runs the different tournaments and 
        then saves the data to the data attribute.
    save_data(path_to_directory, descrip_name):
        Saves experiment data as a csv file
    """
   
    def __init__(self, tuple_of_systems, t = 0.5, game_type=None):
        """
        Constructs all the necessary attributes for pd experiment object
        
        Parameters
        ----------
        tuple_of_systems : tuple
            a multi-dimensional matrix where each item of the first-dimension is an
            ordered list of systems, and the second dimension is an ordered-list of 
            teams
        game_type : axelrod.game (object)
            container for game matrix and scoring logic (default is None, which
            will prompt the classic PD setting)
        
        """
        self.CCThreshold = t
        self.sys_tuple = tuple_of_systems # list of lists with partition sets
        self.game = game_type
        # for system in tuple_of_systems:
        #     systems = []
        #     for team in system:
        #         teams = []
        #         for player in team:
        #             l = []
        #             l.append(Agent(player))
        #             tpl = tuple(l)
        #         teams.append(tpl)
        #     systems.append(teams)
        # self.systems = systems

    def run_experiments(self):
        """
        Iterates through each system, runs the different tournaments and 
        then saves the data to the data attribute.
        """
        
        first = True
        list_len = len(self.sys_tuple)
        #proc_list = []
        for num, sys in enumerate(self.sys_tuple, 1):
            # print('partition list: ', f'{sys!r}') # this

            sys_n = PdSystem(sys, self.game, self.CCThreshold)
            sys_n.compute_data()

            if first:
                exp_df = sys_n.data
                first = False
            else:
                exp_df = pd.concat([exp_df, sys_n.data])
            # print('***Processing number ', num) # this
            if (num % 100 == 0):
                self.data = exp_df
                ###### Change file_name string below when changing num of 
                ###### strategies (n) used or the number of players in a team 
                ###### (k)
                self.save_data('Data/Desk/',f'Comb_Sys1to{num}_12strat_4plx3partitions')
                # print(f'System {num} completed and batch saved!') # this
            if (num % 1000 == 0):
                print(f'***Reached system {num}. Progress: ', num/list_len, '%') # this
        self.data = exp_df

    def return_data(self):
        """ 
        Returns experiment data as a pandas df 

        """
        return self.data

    def save_data(self, path_to_directory, descrip_name):
        """ 
        Saves experiment data as a csv file 
        
        Parameters
        ----------
        path_to_directory (str) :  relative path to folder where data is to be stored
        descrip_name (str) : file name prefix for the output data to be saved
        
        Post-condition
        --------------
        csv file is saved in the given directory with the given prefix-name
        """
        # Make directory if it does not exist
        Path(path_to_directory).mkdir(parents=True, exist_ok=True)
        # print("I am saving the data") # this
        if self.game is None:
            R,P,S,T = game.Game().RPST()
        else:
            R,P,S,T = self.game.RPST()
        # print("The file name is: ", path_to_directory+f'{descrip_name}_RPST_{R!r}_{P!r}_{S!r}_{T!r}.csv') # this
        self.data.to_csv(path_to_directory+f'{descrip_name}_RPST_{R!r}_{P!r}_{S!r}_{T!r}.csv')
