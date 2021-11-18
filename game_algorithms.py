

# Node is current state of the board in the algorithm
# Heuristic value returned will be the value returned if the path result in a win/loss/tie
# Depth is how many moves the algorithm is looking ahead

# board_scores = {
#     'Win': 1,
#     'Loss': -1,
#     'Tie': 0,
#     'Nill':None
# }


def minimax(node,depth,maximizingPlayer):

    if depth == 0:
        return

    # Maximizer
    if maximizingPlayer:
        value = -100
        for child in node:
            value = max(value,minimax(child,depth-1,False))
        return value

    # Minimizer
    else:
        value = 100
        for child in node:
            value = min(value,minimax(child,depth-1,True))
        return value



def connect_four():
    pass