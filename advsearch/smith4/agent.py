import math
import timeit
import random
from ..othello import board

# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

E = "."
INFINITY = math.inf
STOP_TIME = 4.9

# the Static heuristic value for a player is calculated by adding together the weights of the 
# squares in which the player’s coins are present. It can be used as evaluation or simply sort 
# the sucessors of GameState by the position (Kill Move).
STATIC_WEIGHTS = [[120, -20, 20,  5,  5, 20, -20, 120],
                  [-20, -40, -5, -5, -5, -5, -40, -20],
                  [ 20,  -5, 15,  3,  3, 15,  -5,  20],
                  [  5,  -5,  3,  3,  3,  3,  -5,   5],
                  [  5,  -5,  3,  3,  3,  3,  -5,   5],
                  [ 20,  -5, 15,  3,  3, 15,  -5,  20],
                  [-20, -40, -5, -5, -5, -5, -40, -20],
                  [120, -20, 20,  5,  5, 20, -20, 120]]

def stabilityHeuristic2(board: board.Board) -> float:

    stable_coins = {'W': 0, 'B' : 0}

    corner1 = board.tiles[0][0]
    corner2 = board.tiles[0][7]
    corner3 = board.tiles[7][0]
    corner4 = board.tiles[7][7]

    # PROCURA ESTADOS ESTAVEIS NA LINHA DE CIMA ------------------------------------------------------
    stable12 = [E]*6
    stopped_12_at = 0
    if corner1 != E:
        stable_coins[corner1] += 1  # Marca a corner 1

        while stopped_12_at <= 5:
            if board.tiles[0][1+stopped_12_at] != corner1:
                break
            stable12[stopped_12_at] = corner1
            stopped_12_at += 1
            stable_coins[corner1] += 1

    stopped_21_at = 0
    if corner2 != E and stopped_12_at != 6:
        while stopped_21_at <= 5:
            if board.tiles[0][6-stopped_21_at] != corner2:
                break
            stable12[5 - stopped_21_at] = corner2
            stopped_21_at += 1
            stable_coins[corner2] += 1

    # PROCURA ESTADOS ESTAVEIS NA LINHA DE BAIXO ------------------------------------------------------
    stable34 = [E] * 6

    stopped_43_at = 0
    if corner4 != E:
        stable_coins[corner4] += 1  # Marca a corner 4

        while stopped_43_at <= 5:
            if board.tiles[7][6-stopped_43_at] != corner4:
                break
            stable34[5 - stopped_43_at] = corner4
            stopped_43_at += 1
            stable_coins[corner4] += 1

    stopped_34_at = 0
    if corner3 != E and stopped_43_at != 6:
        while stopped_34_at <= 5:
            if board.tiles[7][1+stopped_34_at] != corner3:
                break
            stable34[stopped_34_at] = corner3
            stopped_34_at += 1
            stable_coins[corner3] += 1

    # PROCURA ESTADOS ESTAVEIS NA COLUNA DA ESQUERDA ------------------------------------------------------
    stable13 = [E] * 6

    stopped_31_at = 0
    if corner3 != E:
        stable_coins[corner3] += 1  # MARCA A CORNER 3

        while stopped_31_at <= 5:
            if board.tiles[6-stopped_31_at][0] != corner3:
                break
            stable13[5 - stopped_31_at] = corner3
            stopped_31_at += 1
            stable_coins[corner3] += 1

    stopped_13_at = 0
    if corner1 != E and stopped_31_at != 6:
        while stopped_13_at <= 5:
            if board.tiles[1+stopped_13_at][0] != corner1:
                break
            stable13[stopped_13_at] = corner1
            stopped_13_at += 1
            stable_coins[corner1] += 1

    # PROCURA ESTADOS ESTAVEIS NA COLUNA DA DIREITA ------------------------------------------------------
    stable24 = [E] * 6

    stopped_24_at = 0
    if corner2 != E:
        stable_coins[corner2] += 1  # MARCA A CORNER 2

        while stopped_24_at <= 5:
            if board.tiles[1+stopped_24_at][7] != corner2:
                break
            stable24[stopped_24_at] = corner2
            stopped_24_at += 1
            stable_coins[corner2] += 1

    stopped_42_at = 0
    if corner4 != E and stopped_24_at != 6:
        while stopped_42_at <= 5:
            if board.tiles[6-stopped_42_at][7] != corner4:
                break
            stable24[5 - stopped_42_at] = corner4
            stopped_42_at += 1
            stable_coins[corner4] += 1

    static_tiles = [[corner1] + stable12 + [corner2],
                    [E, E, E, E, E, E, E, E],
                    [E, E, E, E, E, E, E, E],
                    [E, E, E, E, E, E, E, E],
                    [E, E, E, E, E, E, E, E],
                    [E, E, E, E, E, E, E, E],
                    [E, E, E, E, E, E, E, E],
                    [corner3] + stable34 + [corner4]]
    return (stable_coins[PLAYER_COLOR] - stable_coins[OPPONENT_COLOR]) / 28



def mobilityHeuristic(board: board.Board) -> float:

    maxPlayerMoves = len(board.legal_moves(PLAYER_COLOR))
    minPlayerMoves = len(board.legal_moves(OPPONENT_COLOR))

    if maxPlayerMoves + minPlayerMoves != 0:
        return (maxPlayerMoves - minPlayerMoves) / (maxPlayerMoves + minPlayerMoves)
    return 0


def coinDifferenceHeuristic(board: board.Board) -> float:

    maxPlayerCoins = board.piece_count[PLAYER_COLOR]
    minPlayerCoins = board.piece_count[OPPONENT_COLOR]

    return (maxPlayerCoins - minPlayerCoins) / (maxPlayerCoins + minPlayerCoins)


def cornersHeuristic(board: board.Board) -> float:

    maxPlayerCorners = 0
    minAgentCorners = 0

    corners = [(0, 0), (7, 7), (0, 7), (7, 0)]

    for cornerX, cornerY in corners:
        if board.tiles[cornerX][cornerY] == PLAYER_COLOR:
            maxPlayerCorners += 1
        elif board.tiles[cornerX][cornerY] == OPPONENT_COLOR:
            minAgentCorners += 1

    return (maxPlayerCorners - minAgentCorners)/4


def staticWeightsHeuristic(board: board.Board) -> float:

    maxPlayerEval = 0
    minAgentEval = 0
    max_possible_sum = 0

    for i in range(8):
        for j in range(8):
            if board.tiles[i][j] == PLAYER_COLOR:
                maxPlayerEval += STATIC_WEIGHTS[i][j]
                max_possible_sum += abs(STATIC_WEIGHTS[i][j])
            elif board.tiles[i][j] == OPPONENT_COLOR:
                minAgentEval += STATIC_WEIGHTS[i][j]
                max_possible_sum += abs(STATIC_WEIGHTS[i][j])


    if max_possible_sum != 0:
        return (maxPlayerEval - minAgentEval)/max_possible_sum
    return 0


def stabilityHeuristic(board: board.Board) -> float:
    stable_coins = {'W': 0, 'B': 0}

    corner1 = board.tiles[0][0]
    corner2 = board.tiles[0][7]
    corner3 = board.tiles[7][0]
    corner4 = board.tiles[7][7]

    # PROCURA ESTADOS ESTAVEIS NA LINHA DE CIMA ------------------------------------------------------
    stopped_12_at = 0
    if corner1 != E:
        stable_coins[corner1] += 1  # Marca a corner 1

        while stopped_12_at <= 5:
            if board.tiles[0][1 + stopped_12_at] != corner1:
                break
            stopped_12_at += 1
            stable_coins[corner1] += 1

    stopped_21_at = 0
    if corner2 != E and stopped_12_at != 6:
        while stopped_21_at <= 5:
            if board.tiles[0][6 - stopped_21_at] != corner2:
                break
            stopped_21_at += 1
            stable_coins[corner2] += 1

    # PROCURA ESTADOS ESTAVEIS NA LINHA DE BAIXO ------------------------------------------------------

    stopped_43_at = 0
    if corner4 != E:
        stable_coins[corner4] += 1  # Marca a corner 4

        while stopped_43_at <= 5:
            if board.tiles[7][6 - stopped_43_at] != corner4:
                break
            stopped_43_at += 1
            stable_coins[corner4] += 1

    stopped_34_at = 0
    if corner3 != E and stopped_43_at != 6:
        while stopped_34_at <= 5:
            if board.tiles[7][1 + stopped_34_at] != corner3:
                break
            stopped_34_at += 1
            stable_coins[corner3] += 1

    # PROCURA ESTADOS ESTAVEIS NA COLUNA DA ESQUERDA ------------------------------------------------------
    stopped_31_at = 0
    if corner3 != E:
        stable_coins[corner3] += 1  # MARCA A CORNER 3

        while stopped_31_at <= 5:
            if board.tiles[6 - stopped_31_at][0] != corner3:
                break
            stopped_31_at += 1
            stable_coins[corner3] += 1

    stopped_13_at = 0
    if corner1 != E and stopped_31_at != 6:
        while stopped_13_at <= 5:
            if board.tiles[1 + stopped_13_at][0] != corner1:
                break
            stopped_13_at += 1
            stable_coins[corner1] += 1

    # PROCURA ESTADOS ESTAVEIS NA COLUNA DA DIREITA ------------------------------------------------------
    stopped_24_at = 0
    if corner2 != E:
        stable_coins[corner2] += 1  # MARCA A CORNER 2

        while stopped_24_at <= 5:
            if board.tiles[1 + stopped_24_at][7] != corner2:
                break
            stopped_24_at += 1
            stable_coins[corner2] += 1

    stopped_42_at = 0
    if corner4 != E and stopped_24_at != 6:
        while stopped_42_at <= 5:
            if board.tiles[6 - stopped_42_at][7] != corner4:
                break
            stopped_42_at += 1
            stable_coins[corner4] += 1

    return (stable_coins[PLAYER_COLOR] - stable_coins[OPPONENT_COLOR]) / 28


class GameState(object):
    def __init__(self, board: board.Board, depth: int, max_depth: int, curr_color: chr, start: float, weights: list):
        self.board = board
        self.depth = depth
        self.max_depth = max_depth
        self.curr_color = curr_color
        self.start = start
        self.weights = weights

    def is_terminal(self) -> bool:  
        return self.depth >= self.max_depth or self.board.is_terminal_state() or (timeit.default_timer() - self.start >= STOP_TIME)
    
    def evaluation(self) -> float:

        # Sum of heuristics          
        heuristic = mobilityHeuristic(self.board) * self.weights[0]
        heuristic += coinDifferenceHeuristic(self.board) * self.weights[1]
        heuristic += cornersHeuristic(self.board) * self.weights[2]
        if self.weights[3] != 0:
            heuristic += staticWeightsHeuristic(self.board) * self.weights[3]
        if self.weights[4] != 0:
            heuristic += stabilityHeuristic(self.board) * self.weights[4]
        return heuristic

    def result(self, action: (int, int)) -> object:
        new_board = self.board.copy()
        new_board.process_move(action, self.curr_color)
        return GameState(new_board, self.depth+1, self.max_depth, self.board.opponent(self.curr_color), self.start, self.weights)

    def succ(self) -> list:
        return [(self.result(action), action) for action in self.board.legal_moves(self.curr_color)]


def max_value(state: GameState, alfa: float, beta: float) -> (float, (int, int) or None):
    if state.is_terminal() or state.succ() == []: return (state.evaluation(), None)
    value = -INFINITY
    action = None
    for succState, succAction in state.succ():
        succValue = min_value(succState, alfa, beta)[0]
        value, action = max([(value, action), (succValue, succAction)], key=lambda x:x[0])
        alfa = max(alfa, value)
        if alfa >= beta: break
    return (alfa, action)


def min_value(state: GameState, alfa: float, beta: float) -> (float, (int, int) or None):
    if state.is_terminal() or state.succ() == []: return (state.evaluation(), None)
    value = INFINITY
    action = None
    for succState, succAction in state.succ():
        succValue = max_value(succState, alfa, beta)[0]
        value, action = min([(value, action), (succValue, succAction)], key=lambda x:x[0])
        beta = min(beta, value)
        if beta <= alfa: break
    return (beta, action)


def make_move(board: board.Board, color: chr) -> (int, int):
    """
    Returns an Othello move
    :param board: a Board object with the current game state
    :param color: a character indicating the color to make the move ('B' or 'W')
    :return: tuple with x, y indexes of the move (remember: 0 is the first row/column)
    """

    start = timeit.default_timer()

    global PLAYER_COLOR, OPPONENT_COLOR
    PLAYER_COLOR = color
    OPPONENT_COLOR = board.opponent(color)

    last_good_action = (-2, -2)

    REMAINING_MOVES = board.piece_count[board.EMPTY]

    # Changes heuristic weights according to remaining number of moves
    if REMAINING_MOVES >= 40:
        heuristic_weights = [1, 0, 40, 1, 0]  # Focuses on mobility and good positioning
    elif REMAINING_MOVES >= 20:
        heuristic_weights = [1, 0, 40, 1, 5]  # Middle game: Same lol
    elif REMAINING_MOVES >= 10:
        heuristic_weights = [4, 3, 40, 4, 40]  # End game: focuses on corner and some coins

    if REMAINING_MOVES < 10:
        heuristic_weights = [0, 1, 0, 0, 0]
        max_depth = REMAINING_MOVES
    elif 50 > REMAINING_MOVES >= 40 or len(board.legal_moves(PLAYER_COLOR)) < 6:
        max_depth = 4
    else:
        max_depth = 3  # STARTS WITH MAX DEPTH 3 TO TRY AND GO INTO MAX DEPTH 5

    while max_depth <= REMAINING_MOVES:

        value, action = max_value(GameState(board, 0, max_depth, color, start, heuristic_weights), -INFINITY, INFINITY)

        time_spent = timeit.default_timer() - start
        if time_spent >= STOP_TIME:
            return last_good_action

        if time_spent <= 0.14:  # Jumps one depth if it knows it will be shallow now
            max_depth += 1

        max_depth += 1
        last_good_action = action

    legal_moves = board.legal_moves(color)
    if action == None:
        return random.choice(legal_moves) if len(legal_moves) > 0 else (-1, -1)
    else: 
        return action

