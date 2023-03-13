
import numpy as np
from player import Player


class AI_player(Player):
    """
    class for an AI player
    """

    def __init__(self, color):
        """
        constructor for the class AIPlayer
        param color -> the color of the AI player, X for black and O for white
        """
        # inherit from the class Player -> Player initializes
        super().__init__(color)
        # find the opponent player's color
        if color == 'X':
            self.opposite_color = 'O'
        else:
            self.opposite_color = 'X'
    

    def make_a_move(self, board):
        """
        find the best move for the AI player based on the current board/ matrix
        param board -> the current board/ matrix
        returns the best possible position for the AI move (for example 'B2')
        """
        # define the actual player (AI), black corresponds to X and white to O
        if self.color == 'X':
            player = "BLACK (X) (AI)"
        else:
            player = "WHITE (O) (AI)"

        print('Current player:', player)
        print("Please wait, {} is thinking!\n".format(player))

        # find the event with alpha-beta-pruning
        event = self.alpha_beta_search(board)

        return event


    def alpha_beta_search(self, state):
        """
        implementation of the alpha-beta-pruning
        param state -> the current board situation/ state
        returns an event -> the event in the possible events that has the utility value v
        """
        # find the utility value and the corresponding event
        utility, event = self.max_value(state, alpha=-float('inf'), beta=-float('inf'))

        print('coucouuuuuu')

        # return the best found event in the current state
        return event


    def max_value(self, state, alpha, beta):
        """
        implementation if the max value function
        param state -> the current board situation/ state
        param alpha -> the value of the best choice (highest value) found so far for MAX
        param beta -> the value of the best choice (lowest value) found so far for MIN
        returns a utility value v and the corresponding event (which is the best possible event)
        """
        # check if the actual state is a terminal state
        if self.terminal_test(state):
            return self.utility(state), None
        
        # find all possible actions in the current state/ board situation
        possible_events = list(state.legal_events(self.color))

        # if there are no legal actions
        if len(possible_events) == 0:
            return self.utility(state), None

        # initialize the value v to -inf
        value = -float('inf')
        # initialize the best event to None
        best_event = None
        
        # iterate over all possible events
        for event in possible_events:
            # find all the positions where a piece has to be placed/ flipped when considering the event in question
            flipped_positions = state.make_move(event, self.color)
            # if make_move return False -> no possible events in the actual sitation
            if not flipped_positions:
                continue
            # try to find a better value
            actual_value, actual_event = self.min_value(state, alpha, beta)
            """backtrack -> not 100% for the moment"""
            state.backtrack(event, flipped_positions, self.color)
            # check if the actual value is bigger than the value v, if yes -> replace it and replace also the best possible event
            if actual_value > value:
                value = actual_value
                best_event = event
            # check if the value is bigger/ equal than beta, if yes -> beta-cut, prune further search below that node
            if value >= beta:
                break
            # define the new alpha value -> it is the max between the actual alpha and the value v
            alpha = max(alpha, value)
        
        # return the utility value v and the corresponding event (which is the best possible event)
        return value, best_event


    def min_value(self, state, alpha, beta):
        """
        implementation if the min value function
        param state -> the current board situation/ state
        param alpha -> the value of the best choice (highest value) found so far for MAX
        param beta -> the value of the best choice (lowest value) found so far for MIN
        returns a utility value v and the corresponding event (which is the best possible event)
        """
        # check if the actual state is a terminal state
        if self.terminal_test(state):
            return self.utility(state), None
        
        # find all possible actions in the current state/ board situation
        possible_events = list(state.legal_events(self.color))

        # if there are no legal actions
        if len(possible_events) == 0:
            return self.utility(state), None

        # initialize the value v to +inf
        value = float('inf')
        # initialize the best event to None
        best_event = None

        # iterate over all possible events
        for event in possible_events:
            # find all the positions where a piece has to be placed/ flipped when considering the event in question
            flipped_positions = state.make_move(event, self.opposite_color)
            # if make_move return False -> no possible events in the actual sitation
            if not flipped_positions:
                continue
            # try to find a better value
            actual_value, actual_event = self.max_value(state, alpha, beta)
            """backtrack -> not 100% for the moment"""
            state.backtrack(event, flipped_positions, self.opposite_color)
            
            # check if the actual value is smaller than the value v, if yes -> replace it and replace also the best possible event
            if actual_value < value:
                value = actual_value
                best_event = event
            # check if the value is smaller/ equal than alpha, if yes -> alpha-cut, prune further search below that node
            if value <= alpha:
                break
            # define the new beta value -> it is the min between the actual beta and the value v
            beta = min(beta, value)

        # return the utility value v and the corresponding event (which is the best possible event)
        return value, best_event


    def terminal_test(self, state):
        """
        determine if the current state is a terminal state which means that the game is over
        param state -> the current state/ situation of the board
        return True if if the current state is a terminal state (game over) and False otherwise
        """
        # if there are no more empty spaces -> game over, terminal state
        if state.counter('.') == 0:
            return True
        else:
            return False

    
    def utility(self, state):
        """
        utility function (or objective function or payoff function)
        defines the final numeric value for a game that ends in a certain state
        param state -> the current state, the state for which the utility value has to be determined
        returns the utility value for the current state (terminal state)
        """

        """THIS FUNCTION WILL ONLY BE USED IF WE HAVE A WEIGHT MATRIX"""
        def board_to_matrix(board):
            """
            transform the board into a matrix
            X (black) will be transformed into 1 and O (white) will be transformed into -1
            empty spaces will correspond to the value 0
            param board -> the current board that has to be transformed into a matrix
            returns the matrix corresponding to the current board
            """
            # initialize the matrix with zeros
            matrix = np.zeros((6,6))
            for line in range(6):
                for column in range(6):
                    if board._board[line][column] == 'X':
                        """WHY WITH A COMMA HERE?"""
                        matrix[line, column] = 1
                    elif board._board[line][column] == 'O':
                        matrix[line, column] = -1
            return matrix

        return state.counter(self.color) - state.counter(self.opposite_color)
                    







        


