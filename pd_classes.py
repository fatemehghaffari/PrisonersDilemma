from __future__ import annotations
from abc import ABC, abstractmethod
from varname import Wrapper

# Payoff Vector
T = 20
R = 10
P = 5
S = 0
PAYOFF_VECT = (T, R, P, S)

# Strategies are dictionaries that represent a player's initial move and responses to four scenarios.
#  There are 32 possible strategies.
tit_for_tat = Wrapper({'init': 1,
                       (1,2) : 2,
                       (2,2) : 2,
                       (1,1) : 1,
                       (2,1) : 1})

grim = Wrapper({'init': 1,
                (1,2) : 2,
                (2,2) : 2,
                (1,1) : 1,
                (2,1) : 2})

always_C =  Wrapper({'init': 1,
                     (1,2) : 1,
                     (2,2) : 1,
                     (1,1) : 1,
                     (2,1) : 1})
 
always_D = Wrapper({'init': 2,
                    (1,2) : 2,
                    (2,2) : 2,
                    (1,1) : 2,
                    (2,1) : 2})

w_stay_l_shift = Wrapper({'init': 1,
                              (1,2) : 2,
                              (2,2) : 1,
                              (1,1) : 1,
                              (2,1) : 2})

# Player class which is comprised of a strategy and payoff account
class Player:
    def __init__(self, strategy):
        self.policy = strategy.value
        self.name = strategy.name
        self.account = 0
        self.last_move = None

    def update(self, payoff):
        self.account += payoff

    def get_account(self):
        return self.account

    def make_move(self, my_last_move=None, their_last_move=None):
        if self.last_move is None:
            self.last_move = self.policy['init']
            return self.last_move
        else:
            return self.policy[(my_last_move,their_last_move)]

class Two_Player_Sim:
    def __init__(self, payoff_vector, player_1, player_2, num_of_rounds=10):
        # initialize data members
        # tally statistics such as frequency of cooperation, individual payoffs, average payoff
        # scorecard variable
        self.payoff_V = payoff_vector
        self.p1 = player_1
        self.p2 = player_2
        self.round_total = num_of_rounds
        self.coop_count = 0
        self.avg_payoff = 0

    def play_round(self):
        p1_move = self.p1.make_move(self.p1.last_move,self.p2.last_move)
        p2_move = self.p2.make_move(self.p2.last_move,self.p1.last_move)
                
        # Update player hx
        self.p1.last_move = p1_move
        self.p2.last_move = p2_move
        p1_payoff, p2_payoff = self.score_moves(p1_move, p2_move)
        self.p1.update(p1_payoff)
        self.p2.update(p2_payoff)

    def score_moves(self, first_move, second_move):
        # Logging
        print(first_move, second_move)
        T, R, P, S =  self.payoff_V
        if first_move == second_move:
            if first_move == 1:
                self.coop_count += 1
                return (R,R)
            else:
                return (P,P)
        else:
            if first_move == 1:
                return (S,T)
            else:
                return (T,S)

    def play_game(self):
        # Play first round
        #p1_move = self.p1.make_move()
        #p2_move = self.p2.make_move()
        
        # Logging
        print("Payoff Matrix: T", T, " R", R," P", P, " S", S)
        print("P1 Move | P2 Move")
        #print(p1_move, p2_move)
        
       # p1_payoff, p2_payoff = self.score_moves(p1_move, p2_move)
       # self.p1.update(p1_payoff)
       # self.p2.update(p2_payoff)
        
       # if self.round_total > 1:
        for i in range(self.round_total):
            self.play_round()  
        
        payoff_sums = self.p1.get_account() + self.p2.get_account()
        self.avg_payoff = payoff_sums / 2

    def print_statistics(self):
        print("Cooperation Frequency: ", self.coop_count/self.round_total, "Payoff Avg: ", self.avg_payoff)
        print("Player 1: ", self.p1.name, "Ttl Payoff: ", self.p1.get_account())
        print("Player 2: ", self.p2.name, "Ttl Payoff: ", self.p2.get_account())

pl1 = Player(always_D)
pl2 = Player(w_stay_l_shift)

prisoner_dilemma = Two_Player_Sim(PAYOFF_VECT, pl1, pl2, 5) 
prisoner_dilemma.play_game()
prisoner_dilemma.print_statistics()
