import tkinter
import coordinates
import othellologic
from tkinter import ttk
import tkinter.messagebox
from collections import namedtuple

Params = namedtuple('Params','rows cols first top_left win')

class OptionsMenu:
    def __init__(self):
        '''Options menu that allows the user to specify the behavior of the Othello game'''
        self._root_window = tkinter.Tk()
        self._params = None
        self._ComboBoxList = []
        self._root_window.wm_title('Othello Options')
        Labels = ['Rows', 'Columns', 'First Move', 'Top Left Piece', 'Win']
        Values = [['4','6','8','10','12','14','16'],['4','6','8','10','12','14','16'],['Black','White'],['Black','White'],['Most Discs','Fewest Discs']]
        self._Header_label = ttk.Label(master = self._root_window, text = 'Othello Options')
        self._Header_label.grid(row = 0, column = 0, pady = 10, sticky = tkinter.N + tkinter.S)
        for i in range(0,5):
            self._label = ttk.Label(master = self._root_window, text = Labels[i])
            self._label.grid(row = i+1, column = 0, padx = (5,10), pady = 5, sticky = tkinter.W + tkinter.E)
            self._DropDown = ttk.Combobox(master = self._root_window, values = Values[i], state = 'readonly')
            self._DropDown.set(Values[i][0])
            self._DropDown.grid(row = i+1, column = 0, padx = (100,5), pady = 5, sticky = tkinter.E + tkinter.W)
            self._ComboBoxList.append(self._DropDown)
            self._root_window.rowconfigure(i, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)
        self._Button1 = ttk.Button(master = self._root_window, text = 'Enter', cursor = 'pirate', command = self._combine)
        self._Button1.grid(row = 6, column = 0, pady = 10, sticky = tkinter.N + tkinter.S)

    def start(self) -> None:
        self._root_window.mainloop()

    def _on_enter_clicked(self) -> None:
            self._params = Params(
            rows = self._ComboBoxList[0].get(),
            cols = self._ComboBoxList[1].get(),
            first = self._ComboBoxList[2].get(),
            top_left = self._ComboBoxList[3].get(),
            win = self._ComboBoxList[4].get())

    def _close(self) -> None:
        self._root_window.destroy()

    def get_params(self) -> None:
        return self._params

    def _combine(self) -> None:
        self._on_enter_clicked()
        self._close()

class GameBoard:
    '''Draws the game board based around the game logic'''
    class Square:
        '''Square objects keep track of where they were drawn'''
        def __init__(self, top_left: tuple, bottom_right: tuple, width: float, height: float, i: int, j: int):
            self._top_left = top_left
            self._bottom_right = bottom_right
            self._width = width
            self._height = height
            self._i  = i
            self._j = j
            self._min_x, self._min_y = self._top_left.frac()
            self._max_x, self._max_y = self._bottom_right.frac()

        def click_in_square(self, x: float, y: float) -> None:
            if self._min_x * self._width < x < self._max_x * self._width and self._min_y * self._height < y < self._max_y * self._height:
                return True
            else:
                return False

        def return_index(self) -> list:
            return [self._j,self._i]
        
    def __init__(self, rows: int, cols: int, params: list):
        self._root_window = tkinter.Tk()
        self._params = params
        self._rows = int(rows)
        self._cols = int(cols)
        self._root_window.wm_title('Othello Game')
        self._canvas = tkinter.Canvas(master = self._root_window, width = 500, height = 400)
        self._Game = othellologic.OthelloGame()
        self._Game.set_turn(self._params.first)
        self._Game.rows_cols(self._cols, self._rows)
        self._Game.game_board(self._params.top_left)
        self._canvas.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
        self._show_game_info().grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tkinter.N + tkinter.S)
        self._canvas.configure(highlightbackground='black', highlightthickness = 1)
        self._canvas.bind('<Configure>', self._on_window_resized)
        self._canvas.bind('<Button-1>', self._on_mouse_click)
        self._root_window.rowconfigure(0, weight = 0)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)

    def _on_window_resized(self, event: tkinter.Event) -> None:
        self._draw_board()

    def _on_mouse_click(self, event: tkinter.Event) -> None:
        x = event.x
        y = event.y
        for square in self._squares:
            if square.click_in_square(x,y) == True:
                move = square.return_index()
                if self._Game.determine_valid_moves('black') == False and self._Game.determine_valid_moves('white') == False:
                    self._winner.set('Winner:  ' + self._Game.determine_winner(self._params.win))
                elif self._Game.determine_valid_moves(self._Game.current_turn()) == False:
                    tkinter.messagebox.showinfo(title='Pass',message=self._Game.current_turn() + ' Passes!')
                    self._Game.switch_turn()
                    self._draw_board()
                elif self._Game.flip_check(move[0],move[1],self._Game.current_turn()) != []:
                    self._Game.move(move[0], move[1])
                    self._Game.switch_turn()
                    self._draw_board()
                else:
                    self._draw_board()

    def _draw_board(self) -> None:
        '''Redraws the game board'''
        self._CurrentBoard = self._Game.get_board()
        self._canvas.delete(tkinter.ALL)
        self._squares = []
        for i in range(self._rows):
            for j in range(self._cols):
                canvas_width = self._canvas.winfo_width()
                canvas_height = self._canvas.winfo_height()
                min_x = j/self._cols
                min_y = i/self._rows
                max_x = (j+1)/self._cols
                max_y = (i+1)/self._rows
                top_left = coordinates.from_frac((min_x, min_y))
                bottom_right = coordinates.from_frac((max_x, max_y))
                top_left_x, top_left_y = top_left.absolute((canvas_width, canvas_height))
                bottom_right_x, bottom_right_y = bottom_right.absolute((canvas_width, canvas_height))
                self._canvas.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y)
                self._squares.append(self.Square(top_left, bottom_right, canvas_width, canvas_height, i, j))
                if self._CurrentBoard[j][i] != ' ':
                    self._draw_circle(top_left_x, top_left_y, bottom_right_x, bottom_right_y, self._CurrentBoard[j][i])
        self._w_score.set('White:  ' + str(self._Game.score()[0]))
        self._b_score.set('Black:  ' + str(self._Game.score()[1]))
        self._current_move.set('Current Turn: ' + self._Game.current_turn())
        if self._Game.determine_board_full() == True:
            self._winner.set('Winner:  ' + self._Game.determine_winner(self._params.win))

    def _draw_circle(self, top_left_x: float, top_left_y: float, bottom_right_x: float, bottom_right_y: float, space: str):
        if space == 'B':
            self._canvas.create_oval(top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill = 'black')
        elif space == 'W':
            self._canvas.create_oval(top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill = 'white')

    def _show_game_info(self) -> None:
        self._w_score = tkinter.StringVar()
        self._b_score = tkinter.StringVar()
        self._current_move = tkinter.StringVar()
        self._winner = tkinter.StringVar()
        self._info = tkinter.Frame(master = self._root_window)
        self._WhiteScoreLabel = tkinter.Label(master = self._info, textvariable = self._w_score)
        self._WhiteScoreLabel.grid(row = 1, column = 0)
        self._BlackScoreLabel = tkinter.Label(master = self._info, textvariable = self._b_score)
        self._BlackScoreLabel.grid(row = 2, column = 0)
        self._CurrentMoveLabel = tkinter.Label(master = self._info, textvariable = self._current_move)
        self._CurrentMoveLabel.grid(row = 3, column = 0)
        self._WinnerLabel = tkinter.Label(master = self._info, textvariable = self._winner)
        self._WinnerLabel.grid(row = 4, column = 0)
        return self._info

    def start(self) -> None:
        self._root_window.mainloop()

if __name__ == '__main__':
    options = OptionsMenu()
    options.start()
    params = options.get_params()
    board = GameBoard(params[0],params[1], params)
    board.start()


