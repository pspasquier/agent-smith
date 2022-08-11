import random
import numpy as np
import sys
import math
import copy
from ..othello import board

# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

INFINITY = math.inf
MAX_DEPTH = 5

# the Static heuristic value for a player is calculated by adding together the weights of the 
# squares in which the player’s coins are present. It can be used as evaluation or simply sort 
# the sucessors of GameState by the position (Kill Move).
STATIC_WEIGHTS = [[4, -3, 2, 2, 2, 2, -3, 4],
                  [-3, -4, -1, -1, -1, -1, -4, -3],
                  [2, -1, 1, 0, 0, 1, -1, 2],
                  [2, -1, 0, 1, 1, 0, -1, 2],
                  [2, -1, 0, 1, 1, 0, -1, 2],
                  [2, -1, 1, 0, 0, 1, -1, 2],
                  [-3, -4, -1, -1, -1, -1, -4, -3],
                  [4, -3, 2, 2, 2, 2, -3, 4]]

class GameState(object):
    def __init__(self, board: board.Board, playerColor: chr, depth: int, currColor: chr):
        self.board = board
        self.playerColor = playerColor
        self.oponentColor = board.opponent(self.playerColor)
        self.depth = depth
        self.currColor = currColor

    def is_terminal(self) -> bool:  
        return self.depth >= MAX_DEPTH or self.board.is_terminal_state()
    
    def sortAction(action):
        return -STATIC_WEIGHTS[action[1], action[0]]

    def possibleActionsSorted(self) -> list[tuple[int, int]]:
        sortedActions = self.board.legal_moves(self.currColor)
        sortedActions.sort(key=sortAction)
        return sortedActions

    def evaluation(self) -> float:
        # Changes heuristic weights according to remaining number of moves
        if self.board.piece_count[self.board.EMPTY] >= 20:
            heuristicWeights = [3, 1, 10, 3]
        elif self.board.piece_count[self.board.EMPTY] >= 10:
            heuristicWeights = [3, 5, 10, 3]
        else:
            heuristicWeights = [0, 3, 1, 0]
        # Sum of heuristics          
        heuristic = self.mobilityHeuristic() * heuristicWeights[0]
        heuristic += self.coinParityHeuristic() * heuristicWeights[1]
        heuristic += self.cornersHeuristic() * heuristicWeights[2]
        if heuristicWeights[3] != 0:
            heuristic += self.staticWeightsHeuristic() * heuristicWeights[3]
        return heuristic

    def result(self, action: tuple[int, int]) -> object:
        newBoard = copy.deepcopy(self.board)
        newBoard.process_move(action, self.currColor)
        return GameState(newBoard, self.playerColor, self.depth+1, self.board.opponent(self.currColor))

    def succ(self) -> list:
        succs = possibleActionsSorted(self)
        return succs

    def mobilityHeuristic(self) -> int:

        maxPlayerMoves = len(self.board.legal_moves(self.playerColor))
        minPlayerMoves = len(self.board.legal_moves(self.oponentColor))

        if maxPlayerMoves + minPlayerMoves != 0:
            return (maxPlayerMoves - minPlayerMoves) / (maxPlayerMoves + minPlayerMoves)
        return 0

    def coinParityHeuristic(self) -> int:

        maxPlayerCoins = self.board.piece_count[self.playerColor]
        minPlayerCoins = self.board.piece_count[self.oponentColor]

        return (maxPlayerCoins - minPlayerCoins) / (maxPlayerCoins + minPlayerCoins)

    def cornersHeuristic(self) -> int:

        maxPlayerCorners = 0
        minAgentCorners = 0

        corners = [(0, 0), (7, 7), (0, 7), (7, 0)]

        for cornerX, cornerY in corners:
            if self.board.tiles[cornerX][cornerY] == self.playerColor:
                maxPlayerCorners += 1
            elif self.board.tiles[cornerX][cornerY] == self.oponentColor:
                minAgentCorners += 1

        if minAgentCorners + maxPlayerCorners == 0:
            return 0
        return (maxPlayerCorners - minAgentCorners) / (minAgentCorners + maxPlayerCorners)

    def staticWeightsHeuristic(self) -> float:

        maxPlayerEval = 0
        minAgentEval = 0

        for i in range(8):
            for j in range(8):
                if self.board.tiles[i][j] == self.playerColor:
                    maxPlayerEval += STATIC_WEIGHTS[i][j]
                elif self.board.tiles[i][j] == self.oponentColor:
                    minAgentEval += STATIC_WEIGHTS[i][j]

        if maxPlayerEval + minAgentEval != 0:
            return (maxPlayerEval - minAgentEval) / (maxPlayerEval + minAgentEval)
        return 0

def max_value(state: GameState, alfa: float, beta: float) -> tuple[float, tuple[int, int]]:
    if state.is_terminal(): return (state.evaluation(), None)
    value = -INFINITY
    action = None
    for succState, succAction in state.succ():
        value, action = max([(value, action), (min_value(succState, alfa, beta)[0], succAction)], key=lambda x:x[0]) # Refatorar esta Linha
        alfa = max(alfa, value)
        if alfa >= beta: break
    return (alfa, action)

def min_value(state: GameState, alfa: float, beta: float) -> tuple[float, tuple[int, int]]:
    if state.is_terminal(): return (state.evaluation(), None)
    value = INFINITY
    action = None
    for succState, succAction in state.succ():
        value, action = min([(value, action), (max_value(succState, alfa, beta)[0], succAction)], key=lambda x:x[0]) # Refatorar esta Linha
        beta = min(beta, value)
        if beta <= alfa: break
    return (beta, action)

def make_move(board: board.Board, color: chr) -> tuple[int, int]:
    """
    Returns an Othello move
    :param board: a Board object with the current game state
    :param color: a character indicating the color to make the move ('B' or 'W')
    :return: tuple with x, y indexes of the move (remember: 0 is the first row/column)
    """
    value, action = max_value(GameState(board, color, 0, color), -INFINITY, INFINITY)
    return action if action else (-1,-1)

