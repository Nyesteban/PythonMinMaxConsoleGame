import math
from copy import deepcopy

class UI:
    def __init__(self, serv):
        self._serv = serv

    def display_info(self):
        print("Discs labelled by 1 are the human player's and the ones labelled by 2 are the computer's.")
        print("Columns are enumerated from 0 to 6.")

    def move_human(self):
        c = input("Please input the column in which you wish to insert the disc: ")
        try:
            self._serv.human_player_move(int(c))
        except Exception as e:
            print(e)
            self.move_human()

    def move_computer(self):
        board = deepcopy(self._serv.get_full_board())
        col, minimax_score = self._serv.minimax(board, 5, -math.inf, math.inf, True)
        self._serv.add_disc(col, 2)

    def print_board(self):
        for r in self._serv.get_full_board():
            print(*r)

    def start(self):
        self.display_info()
        while True:
            self.move_human()
            print("The board after your move: ")
            self.print_board()
            if self._serv.victory_flag(1) is True:
                print("Human player wins!")
                return
            self.move_computer()
            print("The board after computer's move: ")
            self.print_board()
            if self._serv.victory_flag(2) is True:
                print("Computer wins!")
                return
