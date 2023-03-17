
from game_implementation import Game
from human_player import Human_player
from AI_player import AI_player

if __name__ == "__main__":

    # initialize the bolean to True in order to enter the loop at least once
    incorrect_input = True 
    while incorrect_input == True:

        input_value = int(input('Please select a game mode:\n1: Human player vs human player\n2: Human player vs AI player (Minimax-Search, fraction)\n3: Human player vs AI player (Minimax-Search, weightboard)\
        \n4: Human player vs AI player (Alpha-Beta-Search, fraction)\n5: Human player vs AI player (Alpha-Beta-Search, weightboard)\n'))

        if input_value == 1:
            # the color black corresponds to X and the color white corresponds to O
            black = Human_player("X")
            white = Human_player("O")
            incorrect_input = False 
        elif input_value == 2:
            black = Human_player("X")
            white = AI_player("O", "minimax_decision_algorithm", "fraction", 2)
            incorrect_input = False 
        elif input_value == 3:
            black = Human_player("X")
            white = AI_player("O", "minimax_decision_algorithm", "weightboard", 2)
            incorrect_input = False 
        elif input_value == 4:
            black = Human_player("X")
            white = AI_player("O", "alpha_beta_search_algorithm", "fraction", 2)
        elif input_value == 5:
            black = Human_player("X")
            white = AI_player("O", "alpha_beta_search_algorithm", "weightboard", 2)
        else:
            print('Please enter either a game mode from 1 to 5!')
            incorrect_input = True

        game = Game(black, white)
        game.run_game()