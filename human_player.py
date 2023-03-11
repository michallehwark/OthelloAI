
from player import Player

class Human_player(Player):
    """
    class for a human player
    """

    def __init__(self, color):
        """
        constructor for the class Human_player
        inherit from the class Player -> Player initializes
        param color -> the color, X for black and O for white
        """
        super().__init__(color)

    def make_a_move(self, board):
        """
        legal position of humans based on the current board/ matrix
        param board -> the current board/ matrix
        returns the position of the human move or Q if the game has been ended or 
        """
        # define the color of the human player, X for black and O for white
        if self.color == 'X':
            player = "BLACK (X)"
        else:
            player = "WHITE (O)"

        # human player -> enters the move position
        # 'Q' or 'q' -> returns 'Q' and end of game
        # board position as for example 'A1' -> check if input correct and legal (game rules)

        wrong_input = False
        # a player can't use more than 5 attempts in order to make a move
        attempts_counter = 0
        while True:

            if attempts_counter >= 5:
                return 0

            if not wrong_input:
                print('Current player:', player)
                event = input("Please enter the coordinate where you want to place a disk!\nConsider that the coordinate has to be a valid choice in the actual game situation.\nExample -> 'A5' or 'D2'\nIf you want to end the game, please enter q or Q.\n")
            else:
                event = input()

            if event == 'q' or event == 'Q':
                return "Q"

            if len(event) != 2 or event[0] not in 'ABCDEF' or event[1] not in '123456':
                print('Please enter with the correct systax a coordinate (or end the game with q or Q)')
                wrong_input = True

            else:
                # check if legal
                if event in board.legal_events(self.color):
                        return event
                else:
                    print('Please enter a coordinate that corresponds to a valid choice in the actual game situation!')
            
            # one more attempt has been used
            attempts_counter += 1
            
