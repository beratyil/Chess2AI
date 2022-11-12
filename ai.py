import board, pieces, numpy

class Heuristics:

    # The tables denote the points scored for the position of the chess pieces on the board.

    PAWN_TABLE = numpy.array([
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    KNIGHT_TABLE = numpy.array([
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,   0,   5,   5,   0, -20, -40],
        [-30,   5,  10,  15,  15,  10,   5, -30],
        [-30,   0,  15,  20,  20,  15,   0, -30],
        [-30,   5,  15,  20,  20,  15,   0, -30],
        [-30,   0,  10,  15,  15,  10,   0, -30],
        [-40, -20,   0,   0,   0,   0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ])

    BISHOP_TABLE = numpy.array([
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,   5,   0,   0,   0,   0,   5, -10],
        [-10,  10,  10,  10,  10,  10,  10, -10],
        [-10,   0,  10,  10,  10,  10,   0, -10],
        [-10,   5,   5,  10,  10,   5,   5, -10],
        [-10,   0,   5,  10,  10,   5,   0, -10],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ])

    ROOK_TABLE = numpy.array([
        [ 0,  0,  0,  5,  5,  0,  0,  0],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    QUEEN_TABLE = numpy.array([
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10,   0,   5,  0,  0,   0,   0, -10],
        [-10,   5,   5,  5,  5,   5,   0, -10],
        [  0,   0,   5,  5,  5,   5,   0,  -5],
        [ -5,   0,   5,  5,  5,   5,   0,  -5],
        [-10,   0,   5,  5,  5,   5,   0, -10],
        [-10,   0,   0,  0,  0,   0,   0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ])

    def newEvaluationFunction(board, currentColor):
        # if there is more than one pawn => -1, if there are more than two pawn => -2
        
        totalScore = 0
        
        myScore = 0
        rivalScore = 0

        chesspieces = board.chesspiece

        myPawnScore = 0

        myRookPosition = 0
        rivalRookPosition = 0

        myPawnPromotion = 0
        rivalPawnPromotion = 0

        isMyKnightEdge = 0
        isRivalKnightEdge = 0

        for x in range(8):
            myPawnCntColumn = 0
            rivalPawnCntColumn = 0
            
            for y in range(8):
                piece = chesspieces[x][y]
                
                # 1) Material Score
                if (piece != 0):
                    if (piece.color == currentColor):
                        myScore += piece.value
                    else:
                        rivalScore += piece.value
                
                # 2) Pawn Structure
                if (piece == pieces.Pawn):
                    
                    # Multiple Pawns in Same Column
                    if (piece.color == currentColor):
                        myPawnCntColumn -= 1
                    else:
                        rivalPawnCntColumn += 1
                    
                    # Is Pawn Isolated

                    # How Close a Pawn to Prometing
                    if(piece.color == currentColor):
                        myPawnPromotion = 0
                    else:
                        rivalPawnPromotion = 0

                # 3) Knight
                if(piece == pieces.Knight):
                    
                    # Is Knight At Edges
                    if(piece.color == currentColor):
                        if(y == 7 or y == 0):
                            isMyKnightEdge -= 2
                        elif(y == 6 or y == 0):
                            isMyKnightEdge -= 1
                    else:
                        if(y == 7 or y == 0):
                            isRivalKnightEdge += 2
                        elif(y == 6 or y == 0):
                            isRivalKnightEdge += 1

                if(piece == pieces.Rook):
                    if(piece.color == currentColor):

                        if y == 0 or y == 7:
                            myRookPosition -= 1
                    
                    else:

                        if y == 0 or y == 7:
                            myRookPosition += 1

            if myPawnCntColumn < -1:
                myScore += myPawnCntColumn
            if rivalPawnCntColumn > 1:
                myScore -= rivalPawnCntColumn

    @staticmethod
    def evaluate(board, currentColor):
        material = Heuristics.get_material_score(board)

        #TODO: delete the functions below, instead write functions for
        # *Material Score (already written)
        # *Pawn Structure
        # *Total Square controlled
        # *Direction of Pieces

        pawns = Heuristics.get_piece_position_score(board, pieces.Pawn.PIECE_TYPE, Heuristics.PAWN_TABLE)
        knights = Heuristics.get_piece_position_score(board, pieces.Knight.PIECE_TYPE, Heuristics.KNIGHT_TABLE)
        bishops = Heuristics.get_piece_position_score(board, pieces.Bishop.PIECE_TYPE, Heuristics.BISHOP_TABLE)
        rooks = Heuristics.get_piece_position_score(board, pieces.Rook.PIECE_TYPE, Heuristics.ROOK_TABLE)
        queens = Heuristics.get_piece_position_score(board, pieces.Queen.PIECE_TYPE, Heuristics.QUEEN_TABLE)

        return material + pawns + knights + bishops + rooks + queens

    # Returns the score for the position of the given type of piece.
    # A piece type can for example be: pieces.Pawn.PIECE_TYPE.
    # The table is the 2d numpy array used for the scoring. Example: Heuristics.PAWN_TABLE
    @staticmethod
    def get_piece_position_score(board, piece_type, table):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                piece = board.chesspieces[x][y]
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
                piece = board.chesspieces[x][y]
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

                score = AI.minimax(copy, depth-1, False)
                best_score = max(best_score, score)

            return best_score
        else:
            best_score = AI.INFINITE
            for move in board.get_possible_moves(pieces.Piece.BLACK):
                copy = board.Board.clone(board)
                copy.perform_move(move)

                score = AI.minimax(copy, depth-1, True)
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

                best_score = max(best_score, AI.alphabeta(copy, depth-1, a, b, False, currentColorFlipped))
                a = max(a, best_score)
                if (b <= a):
                    break
        else:
            best_score = AI.INFINITE
            for move in chessboard.get_possible_moves(currentColor):
                copy = board.Board.clone(chessboard)
                copy.perform_move(move)

                best_score = min(best_score, AI.alphabeta(copy, depth-1, a, b, True, currentColorFlipped))
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
