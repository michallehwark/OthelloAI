

from human_player import Human_player

if __name__ == "__main__":

    # initialize the bolean to True in order to enter the loop at least once
    incorrect_input = True 
    while incorrect_input == True:

        input_value = int(input('Please select a game mode:\n1: Human player vs human player\n2: Human player vs AI player\n'))

        if input_value == 1:
            # the color black corresponds to X and the color white corresponds to O
            black = Human_player('X')
            white = Human_player('O')
            incorrect_input = False 
        elif input_value == 2:
            black = Human_player('X')
            white = AI_player('O')
            incorrect_input = False 
        else:
            print('Please enter either game mode 1 or game mode 2!')
            incorrect_input = True