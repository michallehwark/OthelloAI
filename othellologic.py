class OthelloInvalidMoveError(Exception):
    '''Raised when an attempt to make an invalid move is made'''
    pass

class OthelloGameOverError(Exception):
    '''Raised when an attempt to make a move occurs after the game has ended'''
    pass

class OthelloInvalidRowColError(Exception):
    '''Raised when an invalid column or row number is entered'''
    pass

class OthelloGame:
    def __init__(self):
        self._winner = None

    def game_board(self, top_left: str) -> [[str]]:
        self._board = []

        for col in range(self._cols):
            self._board.append([])
            for row in range(self._rows):
                self._board[-1].append(' ')

        if top_left.lower() == 'black':
            self._board[(self._cols//2)-1][(self._rows//2)-1] = 'B'
            self._board[(self._cols//2)][self._rows//2] = 'B'
            self._board[(self._cols//2)-1][self._rows//2] = 'W'
            self._board[self._cols//2][(self._rows//2)-1] = 'W'
        else:
            self._board[(self._cols//2)-1][(self._rows//2)-1] = 'W'
            self._board[(self._cols//2)][self._rows//2] = 'W'
            self._board[(self._cols//2)-1][self._rows//2] = 'B'
            self._board[self._cols//2][(self._rows//2)-1] = 'B'     
        
        return self._board


    def rows_cols(self, cols: int, rows: int) -> None:
        if cols % 2 != 0 or rows % 2 != 0 or rows < 4 or rows > 16 or cols < 4 or cols > 16:
            raise OthelloInvalidRowColError()
        else:
            self._rows = rows
            self._cols = cols


    def current_turn(self) -> str:
        if self._turn.lower() == 'black':
            return 'Black'
        elif self._turn.lower() == 'white':
            return 'White'


    def switch_turn(self) -> str:
        if self._turn.lower() == 'black':
            self._turn = 'white'
            return 'white'
        elif self._turn.lower() == 'white':
            self._turn = 'black'
            return 'black'


    def set_turn(self, turn: str) -> None:
        self._turn = turn
        return self._turn


    def determine_winner(self, win: str) -> str:
        if win == 'Most Discs':
            final_score = self.score()
            if final_score[0] > final_score[1]:
                self._winner = 'White'
                return 'White'
            elif final_score[1] > final_score[0]:
                self._winner = 'White'
                return 'Black'
            elif final_score[0] == final_score[1]:
                self._winner = 'Tie'
                return 'Tie'
        elif win == 'Fewest Discs':
            if final_score[0] < final_score[1]:
                self._winner = 'White'
                return 'White'
            elif final_score[1] < final_score[0]:
                self._winner = 'Black'
                return 'Black'
            elif final_score[0] == final_score[1]:
                self._winner = 'White'
                return 'Tie'
        

    def determine_valid_moves(self, turn: str) -> bool:
        valid_moves = []
        for col in range(self._cols):
            for row in range(self._rows):
                if self._board[col][row] == ' ':
                    valid_moves.extend(self.flip_check(col,row,turn))
                else:
                    continue
        if len(valid_moves) == 0:
            return False
        else:
            return True

        
    def determine_board_full(self) -> bool:
        empty_spaces = 0
        for col in range(self._cols):
            for row in range(self._rows):
                if self._board[col][row] == ' ':
                    empty_spaces+=1
        if empty_spaces == 0:
            return True
        else:
            return False

        
    def score(self) -> list:
        '''Adds up the pieces on the board and returns the score'''
        w = 0
        b = 0
        for col in range(self._cols):
            for row in range(self._rows):
                if self._board[col][row] == 'W':
                    w+=1
                elif self._board[col][row] == 'B':
                    b+=1
        return [w,b]


    def move(self, col: int, row: int) -> None:
        '''Makes a move'''
        if col > self._cols or col < 0 or row > self._rows or row < 0:
            raise OthelloInvalidMoveError()
        elif self._winner != None:
            raise OthelloGameOverError()
        else:
            flipped = self.flip_check(col,row,self._turn)
            if self._turn.lower() == 'black' and flipped != []:
                self._board[col][row] = 'B'
                for i in flipped:
                    self._board[i[0]][i[1]] = 'B'
            elif self._turn.lower() == 'white' and flipped != []:
                self._board[col][row] = 'W'
                for i in flipped:
                    self._board[i[0]][i[1]] = 'W'
                

    def flip_check(self, col: int, row: int, turn: str) -> [[int]]:
        ''' If a move was made in this spot, what would be flipped?'''
        flipped = []

        if turn.lower() == 'black':
            opposite = 'W'
        elif turn.lower() == 'white':
            opposite = 'B'
            
        if self._board[col][row] == ' ':
            temp = []
            i = 1
            while True:
                if row-i < 0:
                    break
                elif self._board[col][row-i] == opposite:
                    temp.append([col,row-i])
                    i+=1
                    continue
                elif self._board[col][row-i] != ' ': 
                    flipped.extend(temp)
                break
            temp = []
            i = 1
            while True:
                if row+i > self._rows-1:
                    break
                elif self._board[col][row+i] == opposite:
                    temp.append([col,row+i])
                    i+=1
                    continue
                elif self._board[col][row+i] != ' ': 
                    flipped.extend(temp)
                break
            temp = []
            i = 1
            while True:
                if col-i < 0:
                    break
                elif self._board[col-i][row] == opposite:
                    temp.append([col-i,row])
                    i+=1
                    continue
                elif self._board[col-i][row] != ' ': 
                    flipped.extend(temp)
                break
            temp = []
            i = 1
            while True:
                if col+i > self._cols-1:
                    break
                elif self._board[col+i][row] == opposite:
                    temp.append([col+i,row])
                    i+=1
                    continue
                elif self._board[col+i][row] != ' ': 
                    flipped.extend(temp)
                break
            temp = []
            i = 1
            while True:
                if row-i < 0 or col+i > self._cols-1:
                    break
                elif self._board[col+i][row-i] == opposite:
                    temp.append([col+i,row-i])
                    i+=1
                    continue
                elif self._board[col+i][row-i] != ' ': 
                    flipped.extend(temp)
                break
            temp = []
            i = 1
            while True:
                if row-i < 0 or col-i < 0:
                    break
                elif self._board[col-i][row-i] == opposite:
                    temp.append([col-i,row-i])
                    i+=1
                    continue
                elif self._board[col-i][row-i] != ' ': 
                    flipped.extend(temp)
                break
            temp = []
            i = 1
            while True:
                if col+i > self._cols-1 or row+i > self._rows-1:
                    break
                elif self._board[col+i][row+i] == opposite:
                    temp.append([col+i,row+i])
                    i+=1
                    continue
                elif self._board[col+i][row+i] != ' ': 
                    flipped.extend(temp)
                break
            temp = []
            i = 1
            while True:
                if row+i > self._rows-1 or col-i < 0:
                    break
                elif self._board[col-i][row+i] == opposite:
                    temp.append([col-i,row+i])
                    i+=1
                    continue
                elif self._board[col-i][row+i] != ' ': 
                    flipped.extend(temp)
                break

        return flipped


    def get_board(self) -> [list]:
        '''Returns the game board'''
        return self._board
