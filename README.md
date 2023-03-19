# Project 1: Board game Othello

## 02180 : Introduction to Artificial Intelligence

### TABLE OF CONTENT

* [Authors](#authors)
* [Files](#files)
* [Description](#description)

### Authors

This project was entirely coded by:

- Céline Kalbermatten - s221401
- Michal Lehwark - s222999
- Malthe Jesper Mathiesen - s194031
- Eline Dorothea Siegumfeldt - s183540

### Files

- `main.py`
- `game_implementation.py`
- `board_implementation.py`
- `player.py`
- `human_player.py`
- `AI_player.py`

### Description

In this first project, the goal was to implement a board game as well as some AI algorithms. 

The whole implementation has been done in Python.

The file `main.py` is the main file, where several parameters as for example the depth for the algorithms can be modified. It is also this file which has to be executed in order to play the game.

In the file `board_implementation.py` everything related to the board has been implemented. It contains several functions which check for example the borders of the board or how many pieces are currently on it.

In the file `game_implementation.py` everything related to the game logic and the rules has been implemented. It is also this file which contains the function to run the game (run_game).

In the file `player.py` a class for a player in general has been implemented. 

The file `human_player.py` has been used to implement a class for a human player. It inherits from the class Player.

The file `AI_player.py` has been used to implement a class for an AI player. It inherits from the class Player and contains the Minimax-Search algorithm as well as the Alpha-Beta-Pruning algorithm. Both algorithms have been implemented with two different heuristic functions. They can as well be found in this file.

### Packages

In order to excecute the present project, the following packages are required:
- Python 
- [numpy](https://numpy.org/)
- [func_timeout](https://pypi.org/project/func-timeout/)
- [copy](https://pypi.org/project/pycopy-copy/)

### Execution

The above mentioned files can be executed in an environment written in Python. 
The files have been created on Visual Studio Code.
