import random
import math
import numpy
from copy import deepcopy

class BoardService:
    def __init__(self, valid, repo):
        self._repo = repo
        self._valid = valid

    def add_disc(self, column, player):
        # Takes 2 arguments: the column and the player.
        # Just like in the physical game, the program will "drop" a disc in that column and put it into the first
        # nonzero row x column pair that it finds. If the disc is labelled 1 it is the human's and if it is labelled 2
        # it is the computer's.
        rowsub = 0
        while self._repo.get_slot_status(rowsub + 5, column) == 1 or self._repo.get_slot_status(rowsub + 5, column) == 2:
            rowsub = rowsub - 1
            if rowsub + 5 < 0:
                break
        self._repo.update_board(rowsub + 5, column, player)

    def get_full_board(self):
        # Gets the full information of the board
        return self._repo.get_board()

    def evaluate_window(self, window, piece):
        # Scores a window based on how advantageous it is to the computer
        score = 0
        opp_piece = 1
        if piece == 1:
            opp_piece = 2

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def score_position(self, board, piece):
        # Prepares windows for the evaluate_window function.
        score = 0
        boardarray = numpy.asarray(board)

        # Score center column
        center_array = [int(i) for i in list(boardarray[:, 7 // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score Horizontal
        for r in range(6):
            row_array = [int(i) for i in list(boardarray[r, :])]
            for c in range(7 - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)

        # Score Vertical
        for c in range(7):
            col_array = [int(i) for i in list(boardarray[:, c])]
            for r in range(6 - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece)

        # Score positive sloped diagonal
        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        # Score negative sloped diagonal
        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def get_valid_locations(self, board):
        # Gets all the valid locations where the computer can insert a disc
        valid_locations = []
        for col in range(7):
            if board[0][col] == 0:
                valid_locations.append(col)
        return valid_locations

    def is_terminal_node(self, board):
        # Checks a board if it has a terminal node.
        return self.victory_flag_minimax(board, 1) or self.victory_flag_minimax(board, 2) or len(self.get_valid_locations(board)) == 0

    def add_disc_minimax(self, board, col, player):
        # The same thing as add_disc, but works on a board given at input.
        rowsub = 0
        while board[rowsub + 5][col] == 1 or board[rowsub + 5][col] == 2:
            rowsub = rowsub - 1
        board[rowsub + 5][col] = player

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        # An alpha beta minimax algorithm, the computer's ai.
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.victory_flag(2):
                    return None, 100000000000000
                elif self.victory_flag(1):
                    return None, -10000000000000
                else:  # Game is over, no more valid moves
                    return None, 0
            else:  # Depth is zero
                return None, self.score_position(board, 2)
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = deepcopy(board)
                self.add_disc_minimax(b_copy, col, 2)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = deepcopy(board)
                self.add_disc_minimax(b_copy, col, 1)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def human_player_move(self, column):
        # Gets the column in which the human player wishes to "drop" the disc, validates it and passes it to the
        # add_disc function.
        self._valid.validate(column)
        self.add_disc(column, 1)

    def victory_flag_minimax(self, board, player):
        # Check horizontal locations for win
        for c in range(7 - 3):
            for r in range(6):
                if board[r][c] == player and board[r][c+1] == player \
                        and board[r][c+2] == player and board[r][c+3] == player:
                    return True

        # Check vertical locations for win
        for c in range(7):
            for r in range(6 - 3):
                if board[r][c] == player and board[r+1][c] == player \
                        and board[r+2][c] == player and board[r+3][c] == player:
                    return True

        # Check positively sloped diagonals for win
        for c in range(7 - 3):
            for r in range(6 - 3):
                if board[r][c] and board[r+1][c+1] == player \
                        and board[r+2][c+2] == player and board[r+3][c+3] == player:
                    return True

        # Check negatively sloped diagonals for win
        for c in range(7 - 3):
            for r in range(3, 6):
                if board[r][c] == player and board[r-1][c+1] == player \
                        and board[r-2][c+2] == player and board[r-3][c+3] == player:
                    return True

        return False

    def victory_flag(self, player):
        # Check horizontal locations for win
        for c in range(7 - 3):
            for r in range(6):
                if self._repo.get_slot_status(r, c) == player and self._repo.get_slot_status(r, c+1) == player \
                        and self._repo.get_slot_status(r, c+2) == player and self._repo.get_slot_status(r, c+3) == player:
                    return True

        # Check vertical locations for win
        for c in range(7):
            for r in range(6 - 3):
                if self._repo.get_slot_status(r, c) == player and self._repo.get_slot_status(r+1, c) == player \
                        and self._repo.get_slot_status(r+2, c) == player and self._repo.get_slot_status(r+3, c) == player:
                    return True

        # Check positively sloped diagonals for win
        for c in range(7 - 3):
            for r in range(6 - 3):
                if self._repo.get_slot_status(r, c) and self._repo.get_slot_status(r+1, c+1) == player \
                        and self._repo.get_slot_status(r+2, c+2) == player and self._repo.get_slot_status(r+3, c+3) == player:
                    return True

        # Check negatively sloped diagonals for win
        for c in range(7 - 3):
            for r in range(3, 6):
                if self._repo.get_slot_status(r, c) == player and self._repo.get_slot_status(r-1, c+1) == player \
                        and self._repo.get_slot_status(r-2, c+2) == player and self._repo.get_slot_status(r-3, c+3) == player:
                    return True

        return False
