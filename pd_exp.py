import pd_system
import pandas as pd
import axelrod as axl


class PdExp:
    """
    Class object that holds list of partition sets (AKA systems of multiple teams) and runs
    experiments, collects data and saves them to csv.
    """
    def __init__(self, list_of_lp, game=None):
        self.lp_list = list_of_lp  # list of lists with partition sets
        self.game = game

    def run_experiments(self):
        first = True
        for num, sys in enumerate(self.lp_list):
            sys_n = PdSystem(sys)
            sys_n.compute_data()

            if first:
                exp_df = sys_n.data
            else:
                exp_df = pd.concat([exp_df, sys_n.data])

        self.data = exp_df

    def save_data(self, path_to_file, descrip_name):
        if self.game is None:
            R,P,S,T = axl.game.Game().RPST()
        else:
            R,P,S,T = self.game.RPST()

        self.data.to_csv(path_to_file+f'{descrip_name}_RPST_{R!r}_{P!r}_{S!r}_{T!r}.csv')
