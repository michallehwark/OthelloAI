
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
        returns the position of the human move
        """
        # define the color of the human player, 1 for black and -1 for white
        if self.color == 1:
            player = "[H] BLACK"
        else:
            player = "[H] WHITE"

        # human player -> enters the move position
        # 'Q' or 'q' -> returns 'Q' and end of game
        # board position as for example 'A1' -> check if input correct and legal (game rules)
        while True:
            event = input("Please enter the coordinate where you want to place a disk!\nConsider that the coordinate has to be a valid choice in the actual game situation.\nExample -> 'A5' or 'D2'\nIf you want to end the game, please enter q or Q.\n")
            
            if event == 'q' or event == 'Q':
                return "Q"

            else:
                row, column = event[1].upper(), event[0].upper()
                # check if on board
                if row in '123456' and column in 'ABCDEF':
                    # check if legal
                    if event in board.legal_events(self.color):
                        return event
                else:
                    print('Please enter a coordinate that corresponds to a valid choice in the actual game situation and that is on the board!')

        print('end of function make a move')

         
    
    """ def inverse_disk(self, board, event):
        inverse_position = board._move(event, self.color) """


    """ def strange
    # initialize the bolean to True in order to enter the loop at least once
        incorrect_input = True
        while incorrect_input == True:           

            event = input("Please enter the coordinate where you want to place a disk!\
            Consider that the coordinate has to be a valid choice in the actual game situation.\
            Example -> 'A5' or 'D2'\
            If you want to end the game, please enter q or Q.")

            if event == 'q' or event == 'Q':
                print('TO IMPLEMENT -> END THE GAME!!!!!')

            elif event[0] not in '12345678' or event[1] not in 'ABCDEFGH':
                print('Please enter a coordinate inside the given board!')
                incorrect_input = True

            elif event not in board.get_legal_actions(self.color):
                print('Please enter a coordinate that corresponds to a valid choice in the actual game situation!')
                incorrect_input = True

            else:
                # the row index is given by the numbers
                row_index = event[1]
                # the column index is given by the letters
                column_index = event[0]
                incorrect_input = False  """