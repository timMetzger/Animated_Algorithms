# Node is current state of the board in the algorithm
# Heuristic value returned will be the value returned if the path result in a win/loss/tie
# Depth is how many moves the algorithm is looking ahead

def get_move(board,who_went_first):
    """Board : game board
       who_went_first : to determine if maximizing or minimizing player
    """
    best_score = -100
    best_move = None
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] is None:
                board[i][j] = "O"
                score = minimax(board, 0, who_went_first)
                if score > best_score:
                    best_score = score
                    best_move = [i,j]
                board[i][j] = None
    return best_move

def minimax(board, depth, maximizingPlayer):
    board_scores = {
        'O': 1,
        'X': -1,
        'Tie': 0,
    }
    winner = check_winner_tic_tac_toe(board)

    if winner is not None:
        return board_scores[winner]

    # Maximizer
    if maximizingPlayer:
        value = -100
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] is None:
                    board[i][j] = 'O'
                    value = max(value, minimax(board, depth + 1, False))
                    board[i][j] = None
        return value

    # Minimizer
    else:
        value = 100
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] is None:
                    board[i][j] = 'X'
                    value = min(value, minimax(board, depth + 1, True))
                    board[i][j] = None

        return value

def check_winner_tic_tac_toe(board):
    # Check horizontal
    for row in board:
        # Check horizontal
        if len(set(row)) == 1 and set(row) != {None}:
            return row[0]

    # Check vertical
    column = []
    for i in range(len(board)):

        for j in range(len(board[0])):
            column.append(board[j][i])

        if len(set(column)) == 1 and set(column) != {None}:
            return column[0]

        column = []

    # Check diagonal
    top_left = [board[0][0], board[1][1], board[2][2]]
    bottom_left = [board[2][0], board[1][1], board[0][2]]
    if len(set(top_left)) == 1 and set(top_left) != {None}:
        return top_left[0]
    elif len(set(bottom_left)) == 1 and set(bottom_left) != {None}:
        return bottom_left[0]

    # Check if board is full
    full_board = True
    for row in board:
        for entry in row:
            if entry is None:
                full_board = False

    if full_board:
        return "Tie"
    else:
        return None

def connect_four():
    pass


# board = [["X", "O",None],[None,None,None],[None,None,None]]
#



