import numpy

import board
import pieces

main_diagonal_1 = [[0,7], [1,6], [2,5], [3,4], [4,3], [5,2],[1,6],[7,0]]
main_diagonal_2 = [[0,0], [1,1], [2,2], [3,3], [4,4], [5,5],[6,6],[7,7]]

middle_squares = [[4,4], [4,5], [5,4], [5,5]]

edges = [[0,0], [0,7], [7,0,], [7,7]]


class Heuristics:
    # The tables denote the points scored for the position of the chess pieces on the board.

    PAWN_TABLE = numpy.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ])

    KNIGHT_TABLE = numpy.array([
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 15, 20, 20, 15, 0, -30],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ])

    BISHOP_TABLE = numpy.array([
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ])

    ROOK_TABLE = numpy.array([
        [0, 0, 0, 5, 5, 0, 0, 0],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ])

    QUEEN_TABLE = numpy.array([
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ])

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

            my_rook_cnt_column = 0
            rival_rook_cnt_column = 0

            for y in range(8):
                piece = chess_pieces[x][y]

                if piece != 0:
                    
                    #----------------------------Current Color----------------------------
                    if piece.color == currentColor:
                        my_score += piece.value

                        if piece.piece_type == "P":
                            # Multiple Pawns in Same Column
                            my_pawn_cnt_column -= 1

                            # Is Pawn in Middle
                            if [x,y] in middle_squares:
                                my_score += 0.5

                            # Is Pawn Isolated
                            
                            if y < 4:
                                leftcolumnprotected = None
                                rightcolumnprotected = None
                                if x > 0:
                                    leftcolumnprotected = chess_pieces[x-1][y-1]
                                if x < 7:
                                    rightcolumnprotected = chess_pieces[x + 1][y - 1]

                                if leftcolumnprotected is None or rightcolumnprotected:
                                    my_score -= 1

                            # TODO:  Weakness of pawns near king

                            # TODO: How Close a Pawn to Promoting (Is there any piece in front)
                            if piece.color == pieces.Piece.BLACK and y < 3:
                                my_score += (y / 7)

                        elif piece.piece_type == "N":

                            # Is Knight At Edges
                            if y == 7 or y == 0 or x == 7 or x == 0:
                                my_score -= 0.25
                            elif y == 6 or y == 1 or x == 6 or x == 1:
                                my_score -= 0.125

                            # Is Knight at Outposts While Protected By a Pawn
                            if y < 4:
                                leftcolumnProtected = 0
                                rightcolumnProtected = 0

                                if x != 0:
                                    leftcolumnProtected = chess_pieces[x-1][y+1]
                                if x != 7:
                                    rightcolumnProtected = chess_pieces[x + 1][y+1]

                                if leftcolumnProtected != 0 and \
                                   leftcolumnProtected.piece_type == "P" and \
                                   leftcolumnProtected.color == currentColor or \
                                   rightcolumnProtected != 0 and \
                                   rightcolumnProtected.piece_type == "P" and \
                                   rightcolumnProtected.color == currentColor:
                                
                                    is_found_pawn = False
                                    for row in range(y,0,-1):
                                        
                                        leftcolumn = 0
                                        rightcolumn = 0

                                        if x != 0:
                                            leftcolumn = chess_pieces[x-1][row]
                                        if x != 7:
                                            rightcolumn = chess_pieces[x + 1][row]

                                        if leftcolumn != 0:
                                            if leftcolumn.piece_type == "P" and leftcolumn.color != currentColor:
                                                is_found_pawn = True
                                                break
                                        if rightcolumn != 0:
                                            if rightcolumn.piece_type == "P" and rightcolumn.color != currentColor:
                                                is_found_pawn = True
                                                break
                                    
                                    if not is_found_pawn:
                                        my_score += 1

                        elif piece.piece_type == "B":
                            #Is Bishop at a Major Diagonal
                            if [x,y] in main_diagonal_1 or [x,y] in main_diagonal_2:
                                my_score += 0.5

                            #TODO: Is Bishop Paired With Other Bishop

                            #Does Bishop in the Same Diagonal With Rival King
                            rivalking = rival_pieces.get("K")[0]
                            moves = piece.get_possible_diagonal_moves(board)
                            
                            min = 7

                            for move in moves:
                                xdif = abs(rivalking.x - move.xto)
                                ydif = abs(rivalking.y - move.yto)

                                if xdif + ydif < min:
                                    min = xdif + ydif

                            if min < 3:
                                my_score += 0.8

                        elif piece.piece_type == "R":
                            # Is Rook At Edges
                            if y == 0 or y == 7 or x == 0 or x == 7:
                                my_score -= 0.25

                            # Is Multiple Rook at Same Column
                            my_rook_cnt_column += 1

                            rooks = my_pieces.get("R")

                            for rook in rooks:
                                if rook is not piece and rook != 0:
                                    if rook.x == piece.x or rook.y == piece.y:
                                        my_score += 0.125


                            # Open or Semi Open File
                            file_situation = "open"
                            for file_index in range(y, 0, -1):
                                
                                currentpiece = chess_pieces[x][file_index]

                                if currentpiece != 0:
                                    if currentpiece.piece_type == "P" and currentpiece.color == currentColor:
                                        file_situation = "closed"
                                        break
                                    elif currentpiece.piece_type == "P" and currentpiece.color != currentColor:
                                        file_situation = "semi-open"
                                    else:
                                        continue

                            if file_situation == "open":
                                my_score += 0.75
                            elif file_situation == "semi-open":
                                my_score += 0.5

                        elif piece.piece_type == "Q":
                            continue

                        else:
                            # Weakness of pawns near king
                            continue

                    #----------------------------Rival Color----------------------------
                    else:
                        rival_score += piece.value

                        if piece == "P":
                            # Multiple Pawns in Same Column
                            rival_pawn_cnt_column -= 1

                            # Is Pawn in Middle
                            if [x,y] in middle_squares:
                                rival_score += 0.5

                            # Is Pawn Isolated
                            
                            if y > 4:
                                leftcolumnprotected = None
                                rightcolumnprotected = None
                                if x > 0:
                                    leftcolumnprotected = chess_pieces[x-1][y-1]
                                if x < 7:
                                    rightcolumnprotected = chess_pieces[x + 1][y - 1]

                                if leftcolumnprotected is None or rightcolumnprotected:
                                    rival_score -= 1

                            # TODO:  Weakness of pawns near king

                            # TODO: How Close a Pawn to Promoting (Is there any piece in front)
                            if piece.color == pieces.Piece.BLACK and y > 4:
                                rival_score += (y / 7)

                        elif piece.piece_type == "N":

                            # Is Knight At Edges
                            if y == 7 or y == 0 or x == 7 or x == 0:
                                rival_score -= 0.25
                            elif y == 6 or y == 1 or x == 6 or x == 1:
                                rival_score -= 0.125

                            # Is Knight at Outposts While Protected By a Pawn
                            if y > 4:
                                leftcolumnProtected = 0
                                rightcolumnProtected = 0

                                if x != 0:
                                    leftcolumnProtected = chess_pieces[x-1][y-1]
                                if x != 7:
                                    rightcolumnProtected = chess_pieces[x + 1][y-1]

                                if leftcolumnProtected != 0 and \
                                   leftcolumnProtected.piece_type == "P" and \
                                   leftcolumnProtected.color == rivalcolor or \
                                   rightcolumnProtected != 0 and \
                                   rightcolumnProtected.piece_type == "P" and \
                                   rightcolumnProtected.color == rivalcolor:
                                
                                    is_found_pawn = False
                                    for row in range(y,0,-1):
                                        
                                        leftcolumn = 0
                                        rightcolumn = 0

                                        if x != 0:
                                            leftcolumn = chess_pieces[x-1][row]
                                        if x != 7:
                                            rightcolumn = chess_pieces[x + 1][row]

                                        if leftcolumn != 0:
                                            if leftcolumn.piece_type == "P" and leftcolumn.color != rivalcolor:
                                                is_found_pawn = True
                                                break
                                        if rightcolumn != 0:
                                            if rightcolumn.piece_type == "P" and rightcolumn.color != rivalcolor:
                                                is_found_pawn = True
                                                break
                                    
                                    if not is_found_pawn:
                                        rival_score += 1

                        elif piece.piece_type == "B":
                            #Is Bishop at a Major Diagonal
                            if [x,y] in main_diagonal_1 or [x,y] in main_diagonal_2:
                                rival_score += 0.5

                            #TODO: Is Bishop Paired With Other Bishop

                            #Does Bishop in the Same Diagonal With Rival King
                            rivalking = rival_pieces.get("K")[0]
                            moves = piece.get_possible_diagonal_moves(board)
                            
                            min = 7

                            for move in moves:
                                xdif = abs(rivalking.x - move.xto)
                                ydif = abs(rivalking.y - move.yto)

                                if xdif + ydif < min:
                                    min = xdif + ydif

                            if min < 3:
                                rival_score += 0.8

                        elif piece.piece_type == "R":
                            # Is Rook At Edges
                            if y == 0 or y == 7 or x == 0 or x == 7:
                                rival_score -= 0.25

                            # Is Multiple Rook at Same Column
                            my_rook_cnt_column += 1

                            rooks = my_pieces.get("R")

                            for rook in rooks:
                                if rook is not piece and rook != 0:
                                    if rook.x == piece.x or rook.y == piece.y:
                                        rival_score += 0.125


                            # Open or Semi Open File
                            file_situation = "open"
                            for file_index in range(y, 0, -1):
                                
                                currentpiece = chess_pieces[x][file_index]

                                if currentpiece != 0:
                                    if currentpiece.piece_type == "P" and currentpiece.color == rivalcolor:
                                        file_situation = "closed"
                                        break
                                    elif currentpiece.piece_type == "P" and currentpiece.color != rivalcolor:
                                        file_situation = "semi-open"
                                    else:
                                        continue

                            if file_situation == "open":
                                rival_score += 0.75
                            elif file_situation == "semi-open":
                                rival_score += 0.5

                        elif piece.piece_type == "Q":
                            continue

                        else:
                            # Weakness of pawns near king
                            continue

            # if multiple pawn in the same column
            # pawn_cnt_column is a negative number
            if my_pawn_cnt_column < -1:
                my_score += my_pawn_cnt_column
            if rival_pawn_cnt_column > 1:
                rival_score += rival_pawn_cnt_column

            # if two rooks in the same column
            if my_rook_cnt_column > 1:
                rival_score += my_rook_cnt_column
            if rival_rook_cnt_column > 1:
                my_score += rival_rook_cnt_column

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
