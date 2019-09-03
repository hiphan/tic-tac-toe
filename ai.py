from copy import deepcopy


X = 1
O = 0


class SmartAgent:
    def __init__(self, maximizing_player):
        """
        :param maximizing_player: bool. True as X, False as O

        """
        self.maximizing_player = maximizing_player

    def get_valid_moves(self, tictactoe):
        valid_moves = []
        for r in range(3):
            for c in range(3):
                if tictactoe.state[r][c] == -1:
                    valid_moves.append((r, c))
        return valid_moves

    def make_move(self, tictactoe, move, maximizing):
        r = move[0]
        c = move[1]
        next_tictactoe = deepcopy(tictactoe)
        next_tictactoe.turn_counter += 1
        if maximizing:
            next_tictactoe.state[r][c] = X
            next_tictactoe.turn = O
        else:
            next_tictactoe.state[r][c] = O
            next_tictactoe.turn = X
        return next_tictactoe

    def get_node_value(self, tictactoe):
        if tictactoe.over():
            if tictactoe.winner == X:
                return 1
            elif tictactoe.winner == O:
                return -1
            else:
                return 0
        return 0

    def minimax(self, tictactoe, depth, maximizing):
        if depth == 0 or tictactoe.over():
            return None, self.get_node_value(tictactoe)
        valid_moves = self.get_valid_moves(tictactoe)
        if maximizing:
            value = -9999
            best_move = (-1, -1)
            for move in valid_moves:
                next_tictactoe = self.make_move(tictactoe, move, True)
                next_tictactoe_value = self.minimax(next_tictactoe, depth - 1, False)[1]
                if next_tictactoe_value > value:
                    value = next_tictactoe_value
                    best_move = move
            return best_move, value
        else:
            value = 9999
            best_move = (-1, -1)
            for move in valid_moves:
                next_tictactoe = self.make_move(tictactoe, move, False)
                next_tictactoe_value = self.minimax(next_tictactoe, depth - 1, True)[1]
                if next_tictactoe_value < value:
                    value = next_tictactoe_value
                    best_move = move
            return best_move, value
