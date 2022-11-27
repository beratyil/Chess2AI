import numpy

import board
import pieces
import evaluation

main_diagonal_1 = [[0,7], [1,6], [2,5], [3,4], [4,3], [5,2],[1,6],[7,0]]
main_diagonal_2 = [[0,0], [1,1], [2,2], [3,3], [4,4], [5,5],[6,6],[7,7]]

middle_squares = [[4,4], [4,5], [5,4], [5,5]]

edges = [[0,0], [0,7], [7,0,], [7,7]]

class Heuristics:
    # The tables denote the points scored for the position of the chess pieces on the board.

    @staticmethod
    def new_evaluation_function(board, currentColor):
        my_score = 0
        rival_score = 0
        
        rivalcolor = pieces.Piece.flipColor(currentColor)

        chess_pieces = board.chess_pieces

        my_pieces = None
        rival_pieces = None

        if currentColor == pieces.Piece.WHITE:
            my_pieces = board.whitePieces
            rival_pieces = board.blackPieces
        else:
            my_pieces = board.blackPieces
            rival_pieces = board.whitePieces

        for x in range(8):
            my_pawn_cnt_column = 0
            rival_pawn_cnt_column = 0

            for y in range(8):
                piece = chess_pieces[x][y]

                if piece != 0:

                    if piece.color == currentColor:

                        my_score = evaluation.evaluation_current_color(board, piece, chess_pieces, x, y, currentColor, my_pieces, rival_pieces, my_pawn_cnt_column)

                    else:
                        rival_score = evaluation.evaluation_rival_color(board, piece, chess_pieces, x, y, rivalcolor, my_pieces, rival_pieces, rival_pawn_cnt_column)


            # if multiple pawn in the same column
            # pawn_cnt_column is a negative number
            if my_pawn_cnt_column < -1:
                my_score += my_pawn_cnt_column
            if rival_pawn_cnt_column > 1:
                rival_score += rival_pawn_cnt_column

        return my_score - rival_score

    @staticmethod
    def evaluate(board, currentColor):
        # material = Heuristics.get_material_score(board)

        # pawns = Heuristics.get_piece_position_score(board, pieces.Pawn.PIECE_TYPE, Heuristics.PAWN_TABLE)
        # knights = Heuristics.get_piece_position_score(board, pieces.Knight.PIECE_TYPE, Heuristics.KNIGHT_TABLE)
        # bishops = Heuristics.get_piece_position_score(board, pieces.Bishop.PIECE_TYPE, Heuristics.BISHOP_TABLE)
        # rooks = Heuristics.get_piece_position_score(board, pieces.Rook.PIECE_TYPE, Heuristics.ROOK_TABLE)
        # queens = Heuristics.get_piece_position_score(board, pieces.Queen.PIECE_TYPE, Heuristics.QUEEN_TABLE)

        # return material + pawns + knights + bishops + rooks + queens

        return Heuristics.new_evaluation_function(board, currentColor)

    # Returns the score for the position of the given type of piece.
    # A piece type can for example be: pieces.Pawn.PIECE_TYPE.
    # The table is the 2d numpy array used for the scoring. Example: Heuristics.PAWN_TABLE
    @staticmethod
    def get_piece_position_score(board, piece_type, table):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                piece = board.chess_pieces[x][y]
                if (piece != 0):
                    if (piece.piece_type == piece_type):
                        if (piece.color == pieces.Piece.WHITE):
                            white += table[x][y]
                        else:
                            black += table[7 - x][y]

        return white - black

    @staticmethod
    def get_material_score(board):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                piece = board.chess_pieces[x][y]
                if (piece != 0):
                    if (piece.color == pieces.Piece.WHITE):
                        white += piece.value
                    else:
                        black += piece.value

        return white - black

class AI:
    INFINITE = 10000000

    @staticmethod
    def get_ai_move(chessboard, invalid_moves, botColor):

        userColor = pieces.Piece.flipColor(botColor)

        best_move = 0
        best_score = AI.INFINITE
        for move in chessboard.get_possible_moves(botColor):
            if (AI.is_invalid_move(move, invalid_moves)):
                continue

            copy = board.Board.clone(chessboard)
            copy.perform_move(move)

            score = AI.alphabeta(copy, 2, -AI.INFINITE, AI.INFINITE, True, userColor)
            if (score < best_score):
                best_score = score
                best_move = move

        # Checkmate.
        if (best_move == 0):
            return 0

        copy = board.Board.clone(chessboard)
        copy.perform_move(best_move)
        if (copy.is_check(botColor)):
            invalid_moves.append(best_move)
            return AI.get_ai_move(chessboard, invalid_moves, botColor)

        return best_move

    @staticmethod
    def is_invalid_move(move, invalid_moves):
        for invalid_move in invalid_moves:
            if (invalid_move.equals(move)):
                return True
        return False

    @staticmethod
    def minimax(board, depth, maximizing):
        if (depth == 0):
            return Heuristics.evaluate(board)

        if (maximizing):
            best_score = -AI.INFINITE
            for move in board.get_possible_moves(pieces.Piece.WHITE):
                copy = board.Board.clone(board)
                copy.perform_move(move)

                score = AI.minimax(copy, depth - 1, False)
                best_score = max(best_score, score)

            return best_score
        else:
            best_score = AI.INFINITE
            for move in board.get_possible_moves(pieces.Piece.BLACK):
                copy = board.Board.clone(board)
                copy.perform_move(move)

                score = AI.minimax(copy, depth - 1, True)
                best_score = min(best_score, score)

            return best_score

    @staticmethod
    def alphabeta(chessboard, depth, a, b, maximizing, currentColor):
        if (depth == 0):
            return Heuristics.evaluate(chessboard, currentColor)

        currentColorFlipped = pieces.Piece.flipColor(currentColor)

        best_score = 0

        if (maximizing):
            best_score = -AI.INFINITE
            for move in chessboard.get_possible_moves(currentColor):
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)

                best_score = max(best_score, AI.alphabeta(copy, depth - 1, a, b, False, currentColorFlipped))
                a = max(a, best_score)
                if (b <= a):
                    break
        else:
            best_score = AI.INFINITE
            for move in chessboard.get_possible_moves(currentColor):
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)

                best_score = min(best_score, AI.alphabeta(copy, depth - 1, a, b, True, currentColorFlipped))
                b = min(b, best_score)
                if (b <= a):
                    break

        return best_score


class Move:

    def __init__(self, xfrom, yfrom, xto, yto, castling_move):
        self.xfrom = xfrom
        self.yfrom = yfrom
        self.xto = xto
        self.yto = yto
        self.castling_move = castling_move

    # Returns true iff (xfrom,yfrom) and (xto,yto) are the same.
    def equals(self, other_move):
        return self.xfrom == other_move.xfrom and self.yfrom == other_move.yfrom and self.xto == other_move.xto and self.yto == other_move.yto

    def to_string(self):
        return "(" + str(self.xfrom) + ", " + str(self.yfrom) + ") -> (" + str(self.xto) + ", " + str(self.yto) + ")"
