def get_move_tic_tac_toe(board, who_went_first):
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
                    best_move = [i, j]
                board[i][j] = None
    return best_move


def get_move_connect_four(board, player):
    best_score = -1000
    best_move = None
    moves = get_available_moves_connect_four(board)
    for move in moves:
        i, j = move
        board[i][j] = "O"
        score = minimax_alpha_beta(board, 0, player, -1000, 1000)
        if score > best_score:
            best_score = score
            best_move = (i, j)
        board[i][j] = None

    return best_move


def get_available_moves_connect_four(board):
    available_moves = []
    for i, row in enumerate(reversed(board), start=-len(board) + 1):
        for j, col in enumerate(row):
            if len(available_moves) == 7:
                break
            else:
                if col is None:
                    if abs(i) + 1 > len(board) - 1:
                        available_moves.append((abs(i), j))
                    elif abs(i) + 1 <= len(board) - 1:
                        if board[abs(i) + 1][j] is not None:
                            available_moves.append((abs(i), j))

    return available_moves


def get_connect_four_winner(board):
    """Return -> False - if no winner | True - if winner & who wins or None"""
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for row in board:
        previous = None
        count = 0
        for item in row:
            if previous is None and item is not None:
                previous = item
                count += 1
            else:
                if item == previous and item is not None:
                    count += 1
                else:
                    count = 0
                previous = item

            if count == 4:
                return False, item

    # Check vertical
    for j in range(cols):
        previous = None
        count = 0
        for i in range(rows-1,-1,-1):
            if previous is None and board[i][j] is not None:
                previous = board[i][j]
                count += 1
            else:
                if board[i][j] == previous and board[i][j] is not None:
                    count += 1
                else:
                    count = 0
                previous = board[i][j]

            if count == 4:
                return False, board[i][j]

    # Check diagonal
    for i in range(rows):
        for j in range(cols):
            neighbors = get_diagonals(rows, cols, board, i, j)

            # Check diagonal 1
            if len(neighbors[0]) >= 4:
                previous = None
                count = 0
                for item in neighbors[0]:
                    if previous is None and item is not None:
                        previous = item
                        count += 1
                    else:
                        if item == previous and item is not None:
                            count += 1
                        else:
                            count = 0
                        previous = item

                    if count == 4:
                        return False, item

            if len(neighbors[1]) >= 4:
                # Check diagonal 2
                previous = None
                count = 0
                for item in neighbors[1]:
                    if previous is None and item is not None:
                        previous = item
                        count += 1
                    else:
                        if item == previous and item is not None:
                            count += 1
                        else:
                            count = 0
                        previous = item

                    if count == 4:
                        return False, item

    return True, None


def get_diagonals(rows, cols, board, i, j):
    diagonal_items = []
    ascending_diagonal = []
    descending_diagonal = []
    # Ascending right diagonal
    r, c = i, j

    while r > 0 and c < cols:
        if r - 1 >= 0 and c + 1 <= cols - 1:
            r -= 1
            c += 1
            ascending_diagonal.append(board[r][c])
        else:
            break

    r, c = i, j
    while r < rows and c > 0:
        if r + 1 <= rows - 1 and c - 1 >= 0:
            r += 1
            c -= 1
            ascending_diagonal.insert(0, board[r][c])
        else:
            break

    diagonal_items.append(ascending_diagonal)

    # Descending right diagonal
    r, c = i, j
    while r < rows and c < cols:
        if r + 1 <= rows - 1 and c + 1 <= cols - 1:
            r += 1
            c += 1
            descending_diagonal.append(board[r][c])
        else:
            break

    r, c = i, j
    while r > 0 and c > 0:
        if r - 1 >= 0 and c - 1 >= 0:
            r -= 1
            c -= 1
            descending_diagonal.insert(0, board[r][c])
        else:
            break

    diagonal_items.append(descending_diagonal)

    return diagonal_items


def score_board_connect_four(board):
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    max_player_horizontal = 0
    max_computer_horizontal = 0
    for row in board:
        previous = None
        player_row_score = 0
        computer_row_score = 0
        for item in row:
            if previous is None and item is not None:
                previous = item
                if item == 'X':
                    player_row_score += 1
                else:
                    computer_row_score += 1
            else:
                if item == previous and item is not None:
                    if item == 'X':
                        player_row_score += 1
                    else:
                        computer_row_score += 1
                else:
                    if item == 'X':
                        player_row_score = 0
                    else:
                        computer_row_score = 0
            previous = item

        if player_row_score > max_player_horizontal:
            max_player_horizontal = player_row_score

        if computer_row_score > max_computer_horizontal:
            max_computer_horizontal = computer_row_score

    # Check vertical
    max_player_vertical = 0
    max_computer_vertical = 0
    for j in range(cols):
        previous = None
        player_col_score = 0
        computer_col_score = 0
        for i in range(rows-1,-1,-1):
            if previous is None and board[i][j] is not None:
                previous = board[i][j]
                if board[i][j] == "X":
                    player_col_score += 1
                else:
                    computer_col_score += 1
            else:
                if board[i][j] == previous and board[i][j] is not None:
                    if board[i][j] == 'X':
                        player_col_score += 1
                    else:
                        computer_col_score += 1
                else:
                    if board[i][j] == 'X':
                        player_col_score = 0
                    else:
                        computer_col_score = 0
                previous = board[i][j]

        if player_col_score > max_player_vertical:
            max_player_vertical = player_col_score

        if computer_col_score > max_computer_vertical:
            max_computer_vertical = computer_col_score

    # Check diagonal
    max_player_diagonal = 0
    max_computer_diagonal = 0
    for i in range(rows):
        for j in range(cols):
            neighbors = get_diagonals(rows, cols, board, i, j)
            player_diagonal_score = 0
            computer_diagonal_score = 0
            previous = None

            # Check diagonal 1
            for item in neighbors[0]:
                if previous is None and item is not None:
                    previous = item
                    if item == 'X':
                        player_diagonal_score += 1
                    else:
                        computer_diagonal_score += 1
                else:
                    if item == previous and item is not None:
                        if item == 'X':
                            player_diagonal_score += 1
                        else:
                            computer_diagonal_score += 1
                    else:
                        if item == 'X':
                            player_diagonal_score = 0
                        else:
                            computer_diagonal_score = 0
                    previous = item

                if player_diagonal_score > max_player_diagonal:
                    max_player_diagonal = player_diagonal_score

                if computer_diagonal_score > max_computer_diagonal:
                    max_computer_diagonal = computer_diagonal_score

                # Check diagonal 2
                player_diagonal_score = 0
                computer_diagonal_score = 0
                previous = None

                if previous is None and item is not None:
                    previous = item
                    if item == 'X':
                        player_diagonal_score += 1
                    else:
                        computer_diagonal_score += 1
                else:
                    if item == previous and item is not None:
                        if item == 'X':
                            player_diagonal_score += 1
                        else:
                            computer_diagonal_score += 1
                    else:
                        if item == 'X':
                            player_diagonal_score = 0
                        else:
                            computer_diagonal_score = 0
                    previous = item

            if player_diagonal_score > max_player_diagonal:
                max_player_diagonal = player_diagonal_score

            if computer_diagonal_score > max_computer_diagonal:
                max_computer_diagonal = computer_diagonal_score


    player_score = max_player_diagonal * max_player_vertical * max_player_horizontal
    computer_score = max_computer_diagonal * max_computer_vertical * max_computer_horizontal
    return (player_score, computer_score)


def minimax_alpha_beta(board, depth, player, alpha, beta):
    board_scores = {
        'O': 10,
        'X': -10,
    }

    moves = get_available_moves_connect_four(board)

    _, winner = get_connect_four_winner(board)
    player_score, computer_score = score_board_connect_four(board)

    if winner is not None:
        return board_scores[winner] * computer_score if player else board_scores[winner] * computer_score

    elif winner is None and depth > 3:
        return computer_score if player else -player_score

    elif winner is None and moves == []:
        return 0

    if player:
        value = -10000
        for move in moves:
            i, j = move
            board[i][j] = 'O'
            value = max(value, minimax_alpha_beta(board, depth + 1, False, alpha, beta))
            alpha = max(alpha, value)
            board[i][j] = None
            if beta <= alpha:
                break
        return value

    else:
        value = 10000
        for move in moves:
            i, j = move
            board[i][j] = 'X'
            value = min(value, minimax_alpha_beta(board, depth + 1, True, alpha, beta))
            beta = min(beta, value)
            board[i][j] = None
            if beta <= alpha:
                break

        return value


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
