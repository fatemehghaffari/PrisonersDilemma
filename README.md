[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Jessegoodspeed/PrisonersDilemma/HEAD?urlpath=lab)

# Prisoners Dilemma
Script, modules, and Jupyter Notebook for experimentation with the indefinitely, iterated prisoner's dilemma game. Use the Binder badge above to interact with the repo files from the browser.

### Requirements to run main.py locally
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
