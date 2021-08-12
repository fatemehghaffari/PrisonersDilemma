[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Jessegoodspeed/PrisonersDilemma/HEAD?urlpath=lab)

# Prisoner's Dilemma
A classic economic game and social dilemma, the Prisoner's Dilemma (PD) started to gain prominence in the ‘50s. The premise is that two suspects are arrested and isolated, and the charging prosecutor gives them two options - either to protect the other suspect by remaining silent (cooperate) or confess the crime (defect). If suspect A defects and suspect B cooperates, charges will be dropped against A, and B will receive the maximum penalty. If suspect B defects and A cooperates, charges will be dropped against B, and A receives the maximum penalty. If both A and B cooperate, both will receive a lesser penalty, whereas if both defect, both will receive the minimum penalty. This game can be interpreted as an individual being presented a choice between the selfish opportunity to serve one’s sole interest and the altruistic choice to cooperate with the other player. Below is a payoff matrix that represents a player's choice along the axes and the corresponding payoff within the cells in row-column order.

|| Cooperate| Defect|
|----|----|-----|
|**Cooperate** | R, R |S, T|
|**Defect**|T, S|P, P|

In the classic PD Game, there are four relative payoffs: temptation(T), reward (R), punishment (P), and sucker (S), such that T > R > P > S and 2R > T + S. By changing the order of the relative payoffs, one is changing the game. Another classic game that is also studied and contrasted with PD is the Stag Hunt game, where R > T > P > S.

This repository was created to devise a model of group behavior as a round-robin tournament of PD players. This repo contains scripts, modules, and Jupyter Notebooks for experimentation with the indefinitely, iterated prisoner's dilemma game. Use the Binder badge above to interact with the repo notebooks from the browser. To incorporate each memory-one, deterministic strategy in our experiments, we forked the [Axelrod-Python library](https://github.com/Axelrod-Python/Axelrod/tree/master), and added missing strategies directly. [Here](https://github.com/Jessegoodspeed/PrisonersDilemma/blob/main/ListOfDeterministicStrategies.md) is a list of all the deterministic strategies we considered.

### Requirements to run main.py locally
* Python 3
* Numpy
* Pandas
* Install modified Axelrod library from source

#### To install modified Axelrod library from source
```
$ git clone https://github.com/Jessegoodspeed/Axelrod.git
$ cd Axelrod
$ python setup.py install
```
#### To run script
```
$ ./main.py
```
