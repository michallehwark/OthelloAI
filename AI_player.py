
import numpy as np
from player import Player


class AI_player(Player):
    """
    class for an AI player
    """

    def __init__(self, color, given_algorithm, given_depth):
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

        # define with which algorithm the AI is playing
        self.algorithm = given_algorithm

        # define a depth for expaning the trees in the algorithms
        self.depth = given_depth
    

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

        # find the event with minimax-decision
        if self.algorithm == "minimax_decision_algorithm":
            event = self.minimax_decision(board, self.depth)

        # find the event with alpha-beta-search
        if self.algorithm == "alpha_beta_search_algorithm":
            event = self.alpha_beta_search(board, self.depth)

        return event


    def minimax_decision(self, state, depth):
        """
        implementation of the minimax algorithm
        param state -> the current board situation/ state
        returns an event -> the event in the possible events that has the utility value v
        """
        # find the utility value and the corresponding event
        heuristic, event = self.max_value(state, self.depth)

        # return the best found event in the current state
        return event


    def max_value(self, state, depth):
        """
        implementation if the max value function
        param state -> the current board situation/ state
        param depth -> the depth unti which the tree has to be expanded
        returns the value v and the corresponding event (which is the best possible event)
        """
        # check if the actual state is a terminal state
        if self.terminal_test(state) or depth == 0:
            # there is only one possible move left, find this possible move
            only_possible_event = state.legal_events(self.color)
            return self.heuristic(state), only_possible_event
        
        # find all possible actions in the current state/ board situation
        possible_events = list(state.legal_events(self.color))

        # if there are no legal actions
        if len(possible_events) == 0:
            return self.heuristic(state), None

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
            # call min function
            actual_value, actual_event = self.min_value(state, depth-1)
            # backtrack the actual changes on the board, change all the pieces that have to be changed
            state.backtrack(event, flipped_positions, self.color)
            # check if the actual value is bigger than the value v, if yes -> replace it and replace also the best possible event
            if actual_value > value:
                value = actual_value
                best_event = event
               
        # return the value v and the corresponding event (which is the best possible event)
        return value, best_event


    def min_value(self, state, depth):
        """
        implementation if the min value function
        param state -> the current board situation/ state
        param depth -> the depth unti which the tree has to be expanded
        returns the value v and the corresponding event (which is the best possible event)
        """
        # check if the actual state is a terminal state
        if self.terminal_test(state) or depth == 0:
            # there is only one possible move left, find this possible move
            only_possible_event = state.legal_events(self.opposite_color)
            return self.heuristic(state), only_possible_event
        
        # find all possible actions in the current state/ board situation
        possible_events = list(state.legal_events(self.opposite_color))

        # if there are no legal actions
        if len(possible_events) == 0:
            return self.heuristic(state), None

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
            actual_value, actual_event = self.max_value(state, depth-1)
            # backtrack the actual changes on the board, change all the pieces that have to be changed
            state.backtrack(event, flipped_positions, self.opposite_color)
            
            # check if the actual value is smaller than the value v, if yes -> replace it and replace also the best possible event
            if actual_value < value:
                value = actual_value
                best_event = event

        # return the value v and the corresponding event (which is the best possible event)
        return value, best_event



    def alpha_beta_search(self, state, depth):
        """
        implementation of the alpha-beta-pruning
        param state -> the current board situation/ state
        param depth -> the depth until which the tree has to be expanded
        returns an event -> the event in the possible events that has the value v
        """
        # find the utility value and the corresponding event
        heuristic, event = self.max_value_ab(state, depth, alpha=-float('inf'), beta=-float('inf'))

        # return the best found event in the current state
        return event


    def max_value_ab(self, state, depth, alpha, beta):
        """
        implementation if the max value function
        param state -> the current board situation/ state
        param alpha -> the value of the best choice (highest value) found so far for MAX
        param beta -> the value of the best choice (lowest value) found so far for MIN
        param depth -> the depth until which the tree has to be expanded
        returns a value v and the corresponding event (which is the best possible event)
        """
        # check if the actual state is a terminal state
        if self.terminal_test(state) or depth == 0:
            # there is only one possible move left, find this possible move
            only_possible_event = state.legal_events(self.color)
            return self.heuristic(state), only_possible_event
        
        # find all possible actions in the current state/ board situation
        possible_events = list(state.legal_events(self.color))

        # if there are no legal actions
        if len(possible_events) == 0:
            return self.heuristic(state), None

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
            actual_value, actual_event = self.min_value_ab(state, alpha, beta, depth-1)
            # backtrack the actual changes on the board, change all the pieces that have to be changed
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


    def min_value_ab(self, state, alpha, beta, depth):
        """
        implementation if the min value function
        param state -> the current board situation/ state
        param alpha -> the value of the best choice (highest value) found so far for MAX
        param beta -> the value of the best choice (lowest value) found so far for MIN
        param depth -> the depth until which the tree has to be expanded
        returns a utility value v and the corresponding event (which is the best possible event)
        """
        # check if the actual state is a terminal state
        if self.terminal_test(state) or depth == 0:
            # there is only one possible move left, find this possible move
            only_possible_event = state.legal_events(self.opposite_color)
            return self.heuristic(state), only_possible_event
        
        # find all possible actions in the current state/ board situation
        possible_events = list(state.legal_events(self.opposite_color))

        # if there are no legal actions
        if len(possible_events) == 0:
            return self.heuristic(state), None

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
            actual_value, actual_event = self.max_value_ab(state, alpha, beta, depth-1)
            # backtrack the actual changes on the board, change all the pieces that have to be changed
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


    def heuristic(self, state):
        """
        heuristic function
        compute the difference in the number of new flipped pieces of both players 
        and then the fraction between them and the total number of pieces in the current situation
        param state -> the current state/ situation of the board
        returns the heuristic value found for the current state
        """
        # compute the difference in pieces
        difference_in_pieces = state.counter(self.color) - state.counter(self.opposite_color)
        # compute the total number of pieces present on the current board
        total_number_pieces = state.counter(self.color) + state.counter(self.opposite_color)
        # compute the fraction 
        fraction_pieces = difference_in_pieces / total_number_pieces

        return fraction_pieces

        
            

    
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
                    







        


