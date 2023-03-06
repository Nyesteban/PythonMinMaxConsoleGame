import unittest
import math

from repository.board_repository import BoardRepository
from services.board_services import BoardService
from services.board_validator import BoardValidator


class AllTests(unittest.TestCase):

    def setUp(self) -> None:
        self._repo = BoardRepository()
        self._valid = BoardValidator()
        self._serv = BoardService(self._valid, self._repo)

    def tearDown(self) -> None:
        pass

    def test_repo(self):
        self.assertEqual(self._repo.get_slot_status(1, 1), 0)
        self._repo.update_board(1, 2, 1)
        self.assertEqual(self._repo.get_slot_status(1, 2), 1)
        self._repo.update_board(3, 3, 2)
        self.assertEqual(self._repo.get_slot_status(3, 3), 2)
        self.assertEqual(self._repo.get_board(), [[0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                                                  [0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
        self.assertRaises(Exception, self._repo.update_board, -1, 2, 1)

    def test_serv1(self):
        self._serv.add_disc(1, 1)
        self._serv.add_disc(1, 2)
        self._serv.add_disc(0, 1)
        self.assertEqual(self._repo.get_slot_status(5, 1), 1)
        self.assertEqual(self._repo.get_slot_status(4, 1), 2)
        self.assertEqual(self._repo.get_slot_status(5, 0), 1)
        self.assertEqual(self._serv.get_full_board(), [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                                                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                                                       [0, 2, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0]])
        self._serv.add_disc(1, 2)
        self._serv.human_player_move(1)
        self._serv.add_disc(1, 2)
        self._serv.add_disc(1, 1)
        self.assertRaises(Exception, self._serv.add_disc, 1, 2)

    def test_valid1(self):
        self.assertRaises(Exception, self._serv.human_player_move, 7)
        self.assertRaises(Exception, self._serv.human_player_move, -1)

    def test_serv2(self):
        self._serv.human_player_move(1)
        self._serv.human_player_move(1)
        self._serv.human_player_move(1)
        self.assertEqual(self._serv.victory_flag(1), False)
        self._serv.human_player_move(1)
        self.assertEqual(self._serv.victory_flag(1), True)

    def test_serv3(self):
        self._serv.human_player_move(0)
        self._serv.human_player_move(1)
        self._serv.human_player_move(2)
        self._serv.human_player_move(3)
        self.assertEqual(self._serv.victory_flag(2), False)
        self.assertEqual(self._serv.victory_flag(1), True)

    def test_serv4(self):
        self._serv.human_player_move(0)
        self._serv.add_disc(1, 2)
        self._serv.human_player_move(1)
        self._serv.add_disc(2, 2)
        self._serv.add_disc(2, 2)
        self._serv.human_player_move(2)
        self._serv.add_disc(3, 2)
        self._serv.add_disc(3, 2)
        self._serv.add_disc(3, 2)
        self._serv.human_player_move(3)
        self.assertEqual(self._serv.victory_flag(1), True)

    def test_serv5(self):
        self._serv.add_disc(0, 2)
        self._serv.add_disc(0, 2)
        self._serv.add_disc(0, 2)
        self._serv.human_player_move(0)
        self._serv.add_disc(1, 2)
        self._serv.add_disc(1, 2)
        self._serv.human_player_move(1)
        self._serv.add_disc(2, 2)
        self._serv.human_player_move(2)
        self._serv.human_player_move(3)
        self.assertEqual(self._serv.victory_flag(1), True)

    def test_serv6(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                                                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                                                       [0, 2, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 2, 1]]
        self.assertEqual(len(self._serv.get_valid_locations(board)), 7)

    def test_serv2_again(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        self._serv.add_disc_minimax(board, 1, 1)
        self._serv.add_disc_minimax(board, 1, 1)
        self._serv.add_disc_minimax(board, 1, 1)
        self.assertEqual(self._serv.victory_flag_minimax(board, 1), False)
        self._serv.add_disc_minimax(board, 1, 1)
        self.assertEqual(self._serv.victory_flag_minimax(board, 1), True)

    def test_serv3_again(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        self._serv.add_disc_minimax(board, 0, 1)
        self._serv.add_disc_minimax(board, 1, 1)
        self._serv.add_disc_minimax(board, 2, 1)
        self._serv.add_disc_minimax(board, 3, 1)
        self.assertEqual(self._serv.victory_flag_minimax(board, 2), False)
        self.assertEqual(self._serv.victory_flag_minimax(board, 1), True)

    def test_serv4_again(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        self._serv.add_disc_minimax(board, 0, 1)
        self._serv.add_disc_minimax(board, 1, 2)
        self._serv.add_disc_minimax(board, 1, 1)
        self._serv.add_disc_minimax(board, 2, 2)
        self._serv.add_disc_minimax(board, 2, 2)
        self._serv.add_disc_minimax(board, 2, 1)
        self._serv.add_disc_minimax(board, 3, 2)
        self._serv.add_disc_minimax(board, 3, 2)
        self._serv.add_disc_minimax(board, 3, 2)
        self._serv.add_disc_minimax(board, 3, 1)
        self.assertEqual(self._serv.victory_flag_minimax(board, 1), True)

    def test_serv5_again(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        self._serv.add_disc_minimax(board, 0, 2)
        self._serv.add_disc_minimax(board, 0, 2)
        self._serv.add_disc_minimax(board, 0, 2)
        self._serv.add_disc_minimax(board, 0, 1)
        self._serv.add_disc_minimax(board, 1, 2)
        self._serv.add_disc_minimax(board, 1, 2)
        self._serv.add_disc_minimax(board, 1, 1)
        self._serv.add_disc_minimax(board, 2, 2)
        self._serv.add_disc_minimax(board, 2, 1)
        self._serv.add_disc_minimax(board, 3, 1)
        self.assertEqual(self._serv.victory_flag_minimax(board, 1), True)

    def test_serv7(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        self.assertEqual(self._serv.is_terminal_node(board), False)

    def test_serv8(self):
        self.assertEqual(self._serv.evaluate_window([1, 1, 1, 1], 1), 100)
        self.assertEqual(self._serv.evaluate_window([1, 1, 1, 0], 2), -4)
        self.assertEqual(self._serv.evaluate_window([1, 1, 0, 0], 1), 2)
        self.assertEqual(self._serv.evaluate_window([1, 1, 1, 0], 1), 5)

    def test_serv9(self):
        board = [[0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 2, 0, 0, 0],
                 [0, 0, 0, 1, 2, 0, 0],
                 [0, 0, 0, 1, 1, 2, 0]]
        self.assertEqual(self._serv.score_position(board, 1), 6)

    def test_serv10(self):
        board = [[0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0]]
        self.assertEqual(self._serv.minimax(board, 5, -math.inf, math.inf, True), (3, 9))

    def test_serv11(self):
        board = [[2, 1, 2, 1, 2, 1, 2],
                 [2, 1, 2, 1, 2, 1, 2],
                 [1, 2, 1, 2, 1, 2, 1],
                 [1, 2, 1, 2, 1, 2, 1],
                 [2, 1, 2, 1, 2, 1, 2],
                 [2, 1, 2, 1, 2, 1, 2]]
        self.assertEqual(self._serv.minimax(board, 5, -math.inf, math.inf, True), (None, 0))
