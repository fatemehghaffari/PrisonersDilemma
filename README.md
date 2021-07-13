[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Jessegoodspeed/PrisonersDilemma/HEAD?urlpath=lab)

# Prisoners Dilemma
Script, modules, and Jupyter Notebook for experimentation with the indefinitely, iterated prisoner's dilemma game. Use the Binder badge above to interact with the repo notebook from the browser. To incorporate each memory-one, deterministic strategy in our experiments, we forked the [Axelrod-Python library](https://github.com/Axelrod-Python/Axelrod/tree/master), and added missing strategies directly. [Here](https://github.com/Jessegoodspeed/PrisonersDilemma/blob/main/ListOfDeterministicStrategies.md) is a list of all the deterministic strategies we considered.

### Requirements to run main.py locally
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
