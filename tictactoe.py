"""
Tic Tac Toe Player
"""

import math

# Constants representing the players and empty cells in the Tic Tac Toe game
X = "X"      # Player X
O = "O"      # Player O
EMPTY = None # Empty cell on the board


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    
    """
    The player function should take a board state as input, and return which player's turn it is (either X or O).
        - In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move.
        - Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).
    """
    # Debugging: Print the current board state
    print("Current board state:")
    for row in board:
        print(row)
    
    # In the initial game X takes the first move
    if board == initial_state():
        print("Initial state detected. X's turn.")
        return X
    
    # If the game is over, return None
    if terminal(board):
        print("Game is over. No player's turn.")
        return None
    
    # Count the number of moves made by each player
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    # Debugging: Print the count of X and O
    print(f"X count: {x_count}, O count: {o_count}")
    
    # If the game is not over, return the player who has the next turn
    if x_count > o_count:
        print("O's turn.")
        return O
    else:
        print("X's turn.")
        return X




def actions(board):

    """
    Returns set of all possible actions (i, j) available on the board.
        - Each action is a tuple (i, j) where i is the row and j is the column.
        - Possible moves are any cells that do not already have an X or an O.
        - Any return value is acceptable if a terminal board is provided as input.
    """
    possible_actions = set()
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    - If action is not a valid action for the board, your program should raise an exception.
    - The returned board state should be the board that would result from taking the original input board, 
    and letting the player whose turn it is make their move at the cell indicated by the input action.
    - Importantly, the original board should be left unmodified: since Minimax will ultimately require considering 
    many different board states during its computation. This means that simply updating a cell in board itself 
    is not a correct implementation of the result function. You'll likely want to make a deep copy of the board 
    first before making any changes.
    """
    import copy

    print(f"Action received: {action}")
    if action not in actions(board):
        raise ValueError("Invalid action")

    # Create a deep copy of the board to ensure the original board is not modified
    new_board = copy.deepcopy(board)
    print(f"Original board:\n{board}")
    i, j = action
    if new_board[i][j] != EMPTY:
        raise ValueError("Cell is already occupied")
    new_board[i][j] = player(board)
    print(f"New board after action {action}:\n{new_board}")
    return new_board


def winner(board):
    """
    The winner function should accept a board as input, and return the winner of the board if there is one.
    - If the X player has won the game, your function should return X. If the O player has won the game, your function should return O.
    - One can win the game with three of their moves in a row horizontally, vertically, or diagonally.
    - You may assume that there will be at most one winner (that is, no board will ever have both players with three-in-a-row, since that would be an invalid board state).
    """
    for player in ['X', 'O']:
        print(f"Checking for player {player}")
        # Check rows
        for row in board:
            print(f"Checking row: {row}")
            if row == [player, player, player]:
                print(f"Player {player} wins by row: {row}")
                return player
        # Check columns
        for col in range(3):
            column = [board[row][col] for row in range(3)]
            print(f"Checking column {col}: {column}")
            if column == [player, player, player]:
                print(f"Player {player} wins by column {col}: {column}")
                return player
        # Check diagonals
        diagonal1 = [board[i][i] for i in range(3)]
        diagonal2 = [board[i][2 - i] for i in range(3)]
        print(f"Checking diagonal1: {diagonal1}")
        print(f"Checking diagonal2: {diagonal2}")
        if diagonal1 == [player, player, player]:
            print(f"Player {player} wins by diagonal1: {diagonal1}")
            return player
        if diagonal2 == [player, player, player]:
            print(f"Player {player} wins by diagonal2: {diagonal2}")
            return player
    print("No winner found")
    return None


def terminal(board):
    """
    The terminal function should accept a board as input, and return a boolean value indicating whether the game is over.
    - If the game is over, either because someone has won the game or because all cells have been filled without anyone winning, the function should return True.
    - Otherwise, the function should return False if the game is still in progress.
    """
    if winner(board) is not None or all(cell is not EMPTY for row in board for cell in row):
        return True
    return False    


def utility(board):
    """
    The utility function should accept a terminal board as input and output the utility of the board.
    - If X has won the game, the utility is 1. If O has won the game, the utility is -1. If the game has ended in a tie, the utility is 0.
    - You may assume utility will only be called on a board if terminal(board) is True.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    The minimax function should take a board as input and return the optimal move for the player to move on that board.
    The move returned should be the optimal action (i, j) that is one of the allowable actions on the board. If multiple moves are equally optimal, any of those moves is acceptable.
    If the board is a terminal board, the minimax function should return None.

    # Minimax is a recursive algorithm used in decision-making and game theory. It provides an optimal move for the player assuming that the opponent is also playing optimally.
    # The algorithm simulates all possible moves, evaluates the resulting game states, and chooses the move that maximizes the player's minimum gain (hence "minimax").
    # This is special because it ensures the best possible outcome for the player, even if the opponent is also playing optimally.

    # Limitations of Minimax:
    # 1. Computationally Expensive: Minimax can be very slow for games with a large search space, as it needs to explore all possible moves and game states.
    # 2. Depth Limitation: In practical scenarios, the depth of the search is often limited to save computation time, which can result in suboptimal moves.
    # 3. Assumes Perfect Play: Minimax assumes that the opponent will always play optimally, which might not be the case in real-world scenarios.
    # 4. Memory Usage: The algorithm can consume a lot of memory due to the large number of game states that need to be stored and evaluated.

    # Minimax typically fails in:
    # 1. Real-time Games: Where decisions need to be made quickly, and there isn't enough time to compute the optimal move.
    # 2. Games with High Complexity: Such as Chess or Go, where the number of possible moves and game states is extremely large.
    # 3. Non-deterministic Games: Where elements of chance or hidden information are involved, making it difficult to predict the opponent's moves accurately.
    """
    def max_value(board):
        if terminal(board):
            return utility(board), None
        v = float('-inf')
        best_move = None
        for action in actions(board):
            min_val, _ = min_value(result(board, action))
            if min_val > v:
                v = min_val
                best_move = action
        return v, best_move

    def min_value(board):
        if terminal(board):
            return utility(board), None
        v = float('inf')
        best_move = None
        for action in actions(board):
            max_val, _ = max_value(result(board, action))
            if max_val < v:
                v = max_val
                best_move = action
        return v, best_move

    if terminal(board):
        return None
    
    current_player = player(board)
    if current_player == X:
        _, optimal_move = max_value(board)
    else:
        _, optimal_move = min_value(board)
    
    return optimal_move
