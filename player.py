

class Player(object):
    """
    class for a general player
    """

    def _init_(self, color=None):
        """
        constructor for the class player
        param color -> the color, 1 for black and -1 for white
        """
        self.color = color

    def get_best_move(self, board):
        """
        get the coordinates of the best move position in the current board situation
        :param board: current board/ matrix
        returns the coordinates for the best move
        """
        pass
    
    def player_move(self, board, event):
        """
        change a piece, the coordinates of the piece dropped by the root piece get the coordinate list of the reverse piece
        param board -> board/ matrix
        param action -> the coordinates of the dropped piece
        returns the reverse list of pawn coordinates
        """
        flipped_position = board.make_move(event, self.color)
        return flipped_position