# Run a simple test to check if the tictactoe.py module is working correctly

import unittest
from tictactoe import initial_state, player, actions, result, winner, terminal, utility, minimax, X, O, EMPTY

class TestTicTacToe(unittest.TestCase):

    def test_initial_state(self):
        self.assertEqual(initial_state(), [[EMPTY, EMPTY, EMPTY],
                                           [EMPTY, EMPTY, EMPTY],
                                           [EMPTY, EMPTY, EMPTY]])

    def test_player(self):
        self.assertEqual(player(initial_state()), X)
        board = [[X, EMPTY, EMPTY],
                 [EMPTY, O, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(player(board), X)
        board[2][2] = X
        self.assertEqual(player(board), O)

    def test_actions(self):
        board = [[X, O, X],
                 [EMPTY, O, EMPTY],
                 [EMPTY, X, EMPTY]]
        expected_actions = {(1, 0), (1, 2), (2, 0), (2, 2)}
        self.assertEqual(actions(board), expected_actions)

    def test_result(self):
        board = [[EMPTY, X, O],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        new_board = result(board, (1, 1))
        self.assertEqual(new_board, [[EMPTY, X, O],
                                     [EMPTY, X, EMPTY],
                                     [EMPTY, EMPTY, EMPTY]])
        with self.assertRaises(ValueError):
            result(board, (0, 1))  # This cell is already occupied

    def test_winner(self):
        board_x_wins = [[X, X, X],
                        [O, O, EMPTY],
                        [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(winner(board_x_wins), X)

        board_o_wins = [[X, X, EMPTY],
                        [O, O, O],
                        [X, EMPTY, EMPTY]]
        self.assertEqual(winner(board_o_wins), O)

        board_no_winner = [[X, O, X],
                           [X, O, O],
                           [O, X, X]]
        self.assertIsNone(winner(board_no_winner))

    def test_terminal(self):
        board_game_over = [[X, O, X],
                           [X, O, O],
                           [O, X, X]]
        self.assertTrue(terminal(board_game_over))

        board_game_in_progress = [[X, O, X],
                                  [X, O, EMPTY],
                                  [O, EMPTY, EMPTY]]
        self.assertFalse(terminal(board_game_in_progress))

    def test_utility(self):
        board_x_wins = [[X, X, X],
                        [O, O, EMPTY],
                        [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(utility(board_x_wins), 1)

        board_o_wins = [[X, X, EMPTY],
                        [O, O, O],
                        [X, EMPTY, EMPTY]]
        self.assertEqual(utility(board_o_wins), -1)

        board_tie = [[X, O, X],
                     [X, O, O],
                     [O, X, X]]
        self.assertEqual(utility(board_tie), 0)

    def test_minimax(self):
        # Test winning move for X
        board = [[X, X, EMPTY],
                 [O, O, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(minimax(board), (0, 2))

        # Test blocking move for O
        board = [[X, X, EMPTY],
                 [EMPTY, O, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(minimax(board), (0, 2))

        # Test terminal board
        board = [[X, O, X],
                 [X, O, O],
                 [O, X, X]]
        self.assertIsNone(minimax(board))

if __name__ == '__main__':
    unittest.main()