
from board_implementation import Board
from func_timeout import func_timeout, FunctionTimedOut
from copy import deepcopy


class Game(object):
    """
    class for the game
    """

    def __init__(self, black_player, white_player):
        """
        constructor of the class Game
        color black corresponds to X and color white corresponds to O
        """
        self.board = Board()
        self.current_player = None
        self.black_player = black_player
        self.white_player = white_player
        self.black_player.color = "X"
        self.white_player.color = "O"
    

    def change_player(self, black_player, white_player):
        """
        change the current player 
        param black_player -> the player playing with the color black
        param white_player -> the player playing with the color white
        returns the current player
        """
        # start with the black player
        if self.current_player is None:
            return black_player
        else:
            # if the current player is the black player -> change to white player
            if self.current_player == self.black_player:
                return white_player
            # if the current player is the white player -> change to black player
            else:
                return black_player

    # MIGHT NOT WORK   
    def show_winner(self, winner):
        """
        print the winner
        param winner -> 0 if there is draw (no winner), 1 if black is the winner and 2 if white is the winner
        no return
        """
        if winner == 0:
            print('There is a draw, no winner!')
        elif winner == 1:
            print('The black player wins the game!')
        elif winner == 2:
            print('The white player wins the game!')
        # DELETE THIS PART 
        else:
            print('There is a problem!')

    
    def forced_game_end(self, board_problem=False, attempt_problem=False):
        """
        if more than 5 attempts are used in order to place legally a piece on the board -> the game is over
        it is also not possible to modify the board
        param board_problem -> if the board has been modified
        param attempt_problem -> if the maximum number of 5 attempts to put a piece has been passed
        returns the winner and the difference between the winner and the loser at the current state of the game
        if black is the winner -> returns 1 
        if white is the winner -> returns 2
        """
        if self.current_player == self.black_player:
            winner_color = 'White (O)'
            loser_color = 'Black (X)'
            winner = 2
        else:
            winner_color = 'Black (X)'
            loser_color = 'White (=)'
            winner = 1
        
        # used too many attempts in order to put a piece legally on the board
        if attempt_problem:
            print('\n{} tried too many times to put a piece legally on the board, so {} wins'.format(loser_color, winner_color))
        # the board has been illegally modified
        if board_problem:
            print('\n{} made illegal changes to the chessboard, so {} wins'.format(loser_color, winner_color))

        # since the reason for the game ending is special -> the difference between winner and loser is set to 0
        difference = 0

        return winner, difference


    def run_game(self):
        """
        run the whole game
        no return
        """
        # initialize the winner and the difference of points between the winner and the other player
        winner = None
        difference = -1

        # print in the terminal that the game starts
        print('\nSTART OF THE GAME OTHELLO\n')

        # POSSIBLE PROBLEM SINCE SOMETHING IS MISSING HERE (TIME PART)
        self.board.show_board()

        # while loop -> ensure that the game goes on until it is over
        while True:
            # change the current player or start the game with one player
            # if the game starts -> it's the black player's turn
            # if the white player is the current one -> change to the black player
            # if the black player is the current one -> change to the white player
            self.current_player = self.change_player(self.black_player, self.white_player)

            # determine the color of the current player -> X for black and O for white
            if self.current_player == self.black_player:
                color = 'X'
            else:
                color = 'O'
            
            # find the legal moves for the current player
            legal_moves = list(self.board.legal_events(color))

            # if there are no legal moves -> either the game is over or the player has to be changed
            if len(legal_moves) == 0:
                # game over
                if self.end_of_game():
                    winner, difference = self.board.winner_check()
                    break
                # change the player (if there are legal moves for him)
                else:
                    continue

            # create a copy of the board
            board = deepcopy(self.board._board)

            # if there are legal moves for the current player
            # a player can't try more than 5 times to make a legal move -> in range(0,5)
            for i in range(0, 5):
                print('i', i)
                # get the position of the move 
                event = func_timeout(60, self.current_player.make_a_move, kwargs={'board': self.board})
                #event = self.current_player.get_move

                # for input Q or q -> the game has to end directly, it will be ended with the actual points for both players
                if event == 'q' or event == 'Q':
                    break
                # maybe the current move is not legal
                if event not in legal_moves:
                    print('This move is not legal, please put your piece at another (legal) location!')
                    continue
                # the current move is legal
                else:
                    break
            # the player used all his 5 attemps to place a piece correctly -> end the game
            else:
                winner, difference = self.forced_game_end(attempt_problem=True)
                print('5 failed attempts to put a piece legally on the board -> game over!')

            # the board has been modified illegally
            if board != self.board._board:
                winner, difference = self.forced_game_end(board_problem=True)
                break

            # for input Q or q -> the game has to end directly, it will be ended with the actual points for both players
            if event == 'q' or event == 'Q':
                winner, difference = self.board.winner_check()
                break

            if event == None:
                continue
            else:
                # update the game
                self.board.make_move(event, color)

                # print the current matrix/ board in the terminal
                self.board.show_board()

                # check if the game is over
                if self.end_of_game():
                    winner, difference = self.board.winner_check()
                    break
            
        print('THE GAME OTHELLO IS OVER')
        self.board.show_board()
        self.show_winner(winner)

        # return the winner and the difference in points
        if winner is not None and difference > -1:
            result = {1: 'Black Player Wins!', 2: 'White Player Wins!', 0: 'There is a draw!'}[winner]

            # WHY IS THIS IN COMMENTS
            #return result, difference


    def end_of_game(self):
        """
        check if the game is over
        returns TRUE if the game is over and FALSE otherwise
        """
        # check if the current player has a legal possible move
        # if not, change the player and check the same
        # if there is no legal possible move for none of the players -> the game is over
        black_move_list = list(self.board.legal_events('X'))
        white_move_list = list(self.board.legal_events('O'))

        # check if the lists contain any legal moves, if not -> game over
        if len(black_move_list) == 0 and len(white_move_list) == 0:
            return True
        else:
            return False

