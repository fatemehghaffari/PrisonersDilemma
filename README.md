[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Jessegoodspeed/PrisonersDilemma/HEAD?urlpath=https%3A%2F%2Fgithub.com%2FJessegoodspeed%2FPrisonersDilemma%2Fblob%2Fmain%2FSensitivity_Analysis_PD_Model.ipynb)

# Prisoners Dilemma
Script and modules for experimentation with the indefinitely, iterated prisoner's dilemma game.

### Requirements to run this script
* Numpy
* Pandas
* Install modified Axelrod library from source
  - Note: The modified Axelrod library is a fork of the [Axelrod-Python library](https://github.com/Axelrod-Python/Axelrod/tree/master) with some added custom strategies.
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
