import chess


class GameEngine:
    def __init__(self):
        self.board = chess.Board()
        self.waiting_for_promotion = None
        self.move_log = []

    def make_move(self, move_str):
        """move_str example: 'e2e4'"""
        move = chess.Move.from_uci(move_str)
        if move in self.board.legal_moves:
            self.board.push(move)
            self.move_log.append(move)
            return True
        return False

    def is_promotion_move(self, from_sq, to_sq):
        piece = self.board.piece_at(from_sq)
        if piece and piece.piece_type == chess.PAWN:
            if (piece.color == chess.WHITE and chess.square_rank(to_sq) == 7) or (
                piece.color == chess.BLACK and chess.square_rank(to_sq) == 0
            ):
                return True
        return False

    def undo_move(self):
        if len(self.board.move_stack) > 0:
            return self.board.pop()
