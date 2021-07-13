## List of Deterministic Strategies

This list describes each of the deterministic, memory-one strategies included and added to the Axelrod software library. Each row includes the strategy’s name, a brief text description, initial move, and a tuple of memory-one probabilities - probabilities dependent on the player and opponent’s moves of the previous round. The tuple is defined as ( Prob(C | CC), Prob(C | CD), Prob(C | DC), Prob(C | DD) ), where C and D correspond to the moves to cooperate and defect, respectively. As an example, Prob(C | DC) can be translated as the probability that the next move is to cooperate given that the player defected and the opponent cooperated in the previous round. 

Some strategies can be differentiated by how it responds to the game’s payoff structure. In the classic Prisoner’s Dilemma Game, there are four relative payoffs: temptation(T), reward (R), punishment (P), and sucker (S), such that T > R > P > S. With respect to the player, they receive the payoff that corresponds to their and their opponent’s moves. So if the player and opponent mutually cooperate (CC) or defect (DD), then both parties receive R or P, respectively. In the case that the player cooperates while their opponent defects (CD), the player receives the sucker payoff (S) whereas the opponent receives the temptation payoff (T) and vice-versa (DC). An understanding of the tuple and the relative payoffs will lend a better understanding of the distinction between the various strategies below.

Name | Brief Description |	Initial Move	| Tuple
-----|-------------------|----------------|--------
Alternator*	|Alternates between C and D.	|C	|(0,0,1,1)
Anti Tit For Tat*|	Do the opposite of the opponent’s last move.|	C|	(0,1,0,1)
Bitter Cooperator|	This strategy is to defect only when the player receives the sucker's payoff.	|C	|(1,0,1,1)
Bitter Cooperator Def|	This strategy initially defects and then defects only when it receives the sucker's payoff.	|D|	(1,0,1,1)
Bully*	|The opposite of Tit For Tat.|	D|	(0,1,0,1)
Cooperator*|	Always cooperates.|	C|	(1,1,1,1)
Cooperator Def|	Always cooperates after the first move, which is a defection.	|D|	(1,1,1,1)
Coop When Both Defect| Player only cooperates when both players have defected.	|D|	(0,0,0,1)
Coop When Both Defect 1|	Player cooperates initially and when both players defect.|	C	|(0,0,0,1)
Curious Defector|	Always defects after the initial move.	|C|	(0,0,0,0)
Cycler DC*|	Repeats ‘DC’-cycle. Opposite of Alternator strategy.	|D|	(0,0,1,1)
Defector*|	Always defects.	|D|	(0,0,0,0)
Fourteen Coop	|This strategy is to defect only after receiving the punishment payoff.	|C	|(1,1,1,0)
Fourteen Defect|	This strategy is to defect initially and only after receiving the punishment payoff.	|D	|(1,1,1,0)
Grim Trigger|	Cooperates until other player defects. Then only defects from that point.This strategy is similar to Stubborn Def but the initial move is to cooperate. This strategy is the exact opposite of Seven Defect.	|C	|(1,0,0,0)
Seven Coop|	Player defects only after receving reward payoff.	|C	|(0,1,1,1)
Seven Defect|	Player defects initially and defects after receving reward payoff.|	D	|(0,1,1,1)
Stubborn Def|	Player only cooperates after receviing reward payoff, but this will never happen because the player initially defects and will only defect otherwise - a catch-22. This strategy is the exact opposite of Seven Coop.|	D	|(1,0,0,0)
Suspicious Tit For Tat*|	Same idea as Tit For Tat but the initial move is to defect.|	D	|(1,0,1,0)
Sucker Coop|	Player cooperates initially and after receiving the sucker's payoff.|	C	|(0,1,0,0)
Sucker Defect|	Player cooperates only after receiving the sucker's payoff.|	D	|(0,1,0,0)
Thirteen Coop	|This strategy is to defect only after receiving the temptation payoff.|	C	|(1,1,0,1)
Thirteen Defect|	This strategy is to defect initially and only after receiving the temptation payoff.	|D	|(1,1,0,1)
Tit For Tat*|	Player’s initial move is to cooperate and then just follow the opponent's last move.|	C	|(1,0,1,0)
Two Coop|	Player cooperates initially and after they receive the temptation payoff.|	C|	(0,0,1,0)
Two Defect|	Player cooperates only after they receive the temptation payoff.|	D	|(0,0,1,0)
Win-Shift Lose-Stay*|	Also called Reverse Pavlov.|	D|	(0,1,1,0)
Win-Shift Lose-Stay Coop|	Same as Win-Shift Lose-Stay but the initial move is to cooperate.|	C|	(0,1,1,0)
Win-Stay Lose-Shift*|	Also called Pavlov.	|C	|(1,0,0,1)
Win-Stay Lose-Shift Defect|	This strategy is similar to Win-Stay Lose-Shift but the initial move is to defect.	|D	|(1,0,0,1)

\* These strategies were already implemented in the Axelrod library.			
