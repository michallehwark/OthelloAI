import numpy as np

def alfaBetaPruning(self, currentBoard, depth=3):
    value, bestMove = maxValueSearch()
    return True

def maxValueSearch(self, board, alfa=-float('inf'), beta=float('inf'), depth=3):

    if self.TerminalState(board) or depth == 0:
        return self.utility()
    
    #get all possible legal moves
    actionList = getAllMoves(board)
    if actionList == 
    
    # minValueSearch
    return False

def minValueSearch(self, board, alfa=-float('inf'), beta=float('inf'), depth=3):

    if self.TerminalState(board)  or depth == 0:
        return self.GameOver
    
    return False

def utility(self, currentStateOfBoard, depth):
    """
    Function to determine the current state of the game.
    """
    boardScore = np.sum(currentStateOfBoard)
    #lastMoveScore = 
    finalScore = boardScore #+ lastMoveScore

    return finalScore
