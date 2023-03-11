

class Board(object):
    """
    class for the board
    an empy space corresponds to a . in the matrix
    a black piece corresponds to a X in the matrix
    a white piece corresponds to a O in the matrix
    """
    
    def __init__(self):
        """
        constructor of the class Board
        """
        self.empty = '.'
        """ for i in range(6):
            for j in range(6):
                self._board = self.empty """
        self._board = [[self.empty for _ in range(6)] for _ in range(6)]
        # initialize the middle square of the board 
        self._board[2][2] = 'O'
        self._board[2][3] = 'X'
        self._board[3][2] = 'X'
        self._board[3][3] = 'O'


    def _getvalue_(self, row, column):
        """
        get the value at a certain position in the board (matrix)
        param row -> the row index of the position of interest
        param column -> the column index of the position of interest
        """
        return self._board[row][column]


    def show_board(self):
        """
        display the game board on the terminal
        """
        board = self._board
        # print column names 
        print(' ', ' '.join(list('ABCDEF'))) 
        # print row names and the whole matrix (board)
        for i in range(6):
            print(str(i + 1), ' '.join(board[i]))
        print("~   Black: " + str(self.counter('X')))
        print("~   White: " + str(self.counter('O')) + '\n')


    def counter(self, color):
        """
        counter in order to find out the actual number of pieces of a certain color
        . corresponds to none of the colors
        X corresponds to the color black
        O corresponds to the color white
        param color -> the color of interest, the one we want to know the number of pieces of
        """
        counter = 0
        for i in range(6):
            for j in range(6):
                if self._board[i][j] == color:
                    counter += 1

        return counter


    def winner_check(self):
        """
        check which player is winning, based on the number of pieces in the color of each player
        return 0 -> no player is winning, draw
        return 1 -> black player is winning
        return 2 -> white player is winning
        also return the difference of number of pieces of each color
        """
        # initial number of pieces of each color
        black_counter = 0
        white_counter = 0
        for i in range(6):
            for j in range(6):
                # black counter
                if self._board[i][j] == 'X':
                    black_counter += 1
                # white counter
                if self._board[i][j] == 'O':
                    white_counter += 1

        if black_counter > white_counter:
            # black is the winner
            difference = black_counter - white_counter
            return 1, difference
        elif black_counter < white_counter:
            # white is the winner 
            difference = white_counter - black_counter 
            return 2, difference
        elif black_counter == white_counter:
            # Indicates a tie, the number of black pieces is equal to the number of white
            difference = 0
            return 0, difference


    def legal_move_check(self, event, color):
        """
        check if the current move is legal or not
        param event -> the position
        param color -> the current color of the position in question
        return -> list of the reversed coordinates of the other player or FALSE if the move is not legal 
        """
        # convert the string into digital coordinates
        if isinstance(event, str):
            event = self.board_number(event)
        x_start, y_start = event

        # check if there is already a piece placed on the coordinates in question or if the coordinates are out of bounds
        if not self.bound_check(x_start, y_start) or self._board[x_start][y_start] != self.empty:
            return False

        # place a piece (color) in the specified coordinates 
        self._board[x_start][y_start] = color
        # find out the opposite color
        if color == 'X':
            opposite_color = 'O'
        else:
            opposite_color = 'X'

        # initialize a list where all the positions that need to be flipped will be stored
        flipped_positions_list = []
        flipped_positions_board = []

        # have a look at the neighbours of the initial position
        for x_direction, y_direction in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:

            # initialize x and y with the initial coordinates
            x_coordinate = x_start
            y_coordinate = y_start
            # go in all the possible directions from the point of view of the initial coordinates
            x_coordinate += x_direction
            y_coordinate += y_direction

            # check if the new coordinates (neighbors of the initial ones) are on the board/ matrix
            # and if they are of the opposite color (other player)
            if self.bound_check(x_coordinate, y_coordinate) and self._board[x_coordinate][y_coordinate] == opposite_color:
                x_coordinate += x_direction
                y_coordinate += y_direction

                # check if the new point is still on the matrix/ board
                if not self.bound_check(x_coordinate, y_coordinate):
                    continue

                # have a look at even more positions and check if they still belong to the opposite player
                # also check if they are still on the board/matrix
                while self._board[x_coordinate][y_coordinate] == opposite_color:
                    x_coordinate += x_direction
                    y_coordinate += y_direction
                    if not self.bound_check(x_coordinate, y_coordinate):
                        break

                # going out of the bounds but no opposite color -> for example OXXXX
                # so no need to flip 
                if not self.bound_check(x_coordinate, y_coordinate):
                    continue

                # going until a position where there is the same color again (not the opposite one)
                # example -> OXXXO
                # need to flip the colors of the coordinates in between -> add them to the list
                if self._board[x_coordinate][y_coordinate] == color:
                    while True:
                        x_coordinate -= x_direction
                        y_coordinate -= y_direction
                        # going back until the initial position
                        if x_coordinate == x_start and y_coordinate == y_start:
                            break
                        # add the positions at which the color has to be flipped to the list
                        flipped_positions_list.append([x_coordinate, y_coordinate])

        # take off again the color at the initial coordinates
        self._board[x_start][y_start] = self.empty

        # if there is no change of color at any position -> the move is not legal
        if len(flipped_positions_list) == 0:
            return False
        
        # if there are positions where the color has to be flipped -> add them to the list 
        for position in flipped_positions_list:
            # convert from digital coordinates into board coordinates
            flipped_positions_board.append(self.digital_to_board(position))

        # return the list of the coordinates of the positions where the color has to be flipped
        return flipped_positions_board


    def make_move(self, event, color):
        """
        put a piece at certain coordinates (in the matrix/ board)
        param event -> the coordinates where the piece has to be placed, in the form of (row, column)
        param color -> a piece is of a certain color (X for black, O for white and . for no piece)
        returns the list of the coordinates where a piece has been placed/ changed or FALSE if the move fails
        """
        # convert the string into digital coordinates
        if isinstance(event, str):
            event = self.board_to_digital(event)

        fliped_pieces = self.legal_move_check(event, color)

        # change the coordinates of the other player's piece, if there is
        if fliped_pieces:
            for fliped_piece in fliped_pieces:
                x, y = self.board_to_digital(fliped_piece)
                self._board[x][y] = color
            # change the coordinates
            x, y = event
            # change the matrix/ board accordingly
            self._board[x][y] = color
            return fliped_pieces
        else:
            return False


    def backtrack(self, event, flipped_positions, color):
        """
        backtracking -> MAKE BETTER COMMENT
        param event -> 
        param flipped_positions -> list of the flipped places on the matrix/ board
        color -> the color of the flipped places (1 for black, -1 for white and 0 for no piece)
        no return
        """
        # convert the string into digital coordinates
        if isinstance(event, str):
            event = self.board_to_digital(event)
        
        # make the space empty before changing it to the opposite color
        self._board[event[0]][event[1]] = self.empty
        # define the opposite color
        if color == 'X':
            opposite_color = 'O'
        else:
            opposite_color = 'X'
        
        for position in flipped_positions:
            # convert the string into digital coordinates
            if isinstance(position, str):
                position = self.board_to_digital(position)
            # put the new (opposite) color in the desired location on the matrix/ board
            self._board[position[0]][position[1]] = opposite_color


    def bound_check(self, row, column):
        """
        check if some given coordinates are out of the bounds of the matrix/ board
        param row -> the row coordinate of a specific point
        param column -> the column coordinate of a specifit point
        return -> TRUE if the coordinates are on the board and FALSE if not
        """
        if row >= 0 and row <= 5 and column >= 0 and column <= 5:
            bound_check = True
        else:
            bound_check = False
        return bound_check

    
    def legal_events(self, color):
        """
        create coordinates with legal moves (according to the game rules)
        param color -> the color at a certain coordinate (X for black, O for white and . for no piece)
        return the legal move coordinates
        """
        # specify the possible directions around one specific coordinate -> put them in a list
        possible_directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

        # define the opposite color
        if color == 'X':
            opposite_color = 'O'
        else:
            opposite_color = 'X'

        # find the positions around the opposite color position -> the legal positions
        # initialize a list where all these positions will be stocked
        pos_around_opposite = []

        # iterate over the whole matrix/ board
        board = self._board
        for i in range(6):
            for j in range(6):
                if board[i][j] == opposite_color:
                    for x_direction, y_direction in possible_directions:
                        x_coordinate = i + x_direction
                        y_coordinate = j + y_direction
                        # check if the coordinates are inside the board and if there is no other piece at the moment
                        if 0 <= x_coordinate <= 5 and 0 <= y_coordinate <= 5 and board[x_coordinate][y_coordinate] == self.empty and (x_coordinate, y_coordinate) not in pos_around_opposite:
                            pos_around_opposite.append((x_coordinate, y_coordinate))

        # use yield instead of return since the functions will return a large set of values that will only be needed once
        # yield -> returns a generator
        size_list = list(range(6))

        for position in pos_around_opposite:
            if self.legal_move_check(position, color):
                # check the borders
                if position[0] in size_list and position[1] in size_list:
                    # convert from digital coordinates into board coordinates
                    position = self.digital_to_board(position)
                yield position


    def board_to_digital(self, event):
        """
        convert the board coordinates into digital coordinates
        param event -> board/ matrix coordinates, for example '24'
        the first number indicates the column and the second number the row
        return the digital coordinates of a position, for example for '11' it would be (0,0)
        """
        row = str(event[1]).upper()
        column = str(event[0]).upper()

        # check if the coordinates are inside the board/ matrix
        if row in '123456' and column in 'ABCDEF':
            x_coordinate = '123456'.index(row)
            y_coordinate = 'ABCDEF'.index(column)

        return x_coordinate, y_coordinate


    def digital_to_board(self, event):
        """
        convert the digital coordinates into board coordinates
        param event -> digital coordinates, for example '(0,0)'
        return the board coordinates of a position, for example for '(0,0)' it would be '11'
        """
        row, column = event
        size_list = list(range(6))

        # check if the coordinates are inside the board
        if row in size_list and column in size_list:
            return chr(ord('A') + column) + str(row + 1)



        