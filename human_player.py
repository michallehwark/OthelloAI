

class Human_player(object):

    def _init_(self, color):
        self.color = color

    def make_a_move(self, board):

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
                incorrect_input = False  
    
    def inverse_disk(self, board, event):
        inverse_position = board._move(event, self.color)
