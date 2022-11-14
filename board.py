import pieces, ai
import copy
import ujson
class Board:

    WIDTH = 8
    HEIGHT = 8

    def __init__(self, chesspieces, white_king_moved, black_king_moved, whitePieces, blackPieces):
        self.chesspieces = chesspieces
        self.white_king_moved = white_king_moved
        self.black_king_moved = black_king_moved
        self.whitePieces = whitePieces
        self.blackPieces = blackPieces

    @classmethod
    def clone(cls, chessboard):
        chesspieces = [[0 for x in range(Board.WIDTH)] for y in range(Board.HEIGHT)]
        whitePieces = {
            "Pawn": [],
            "Knight": [],
            "Bishop": [],
            "Rook": [],
            "Queen": [],
            "King": [],
        }
        blackPieces = {
            "Pawn": [],
            "Knight": [],
            "Bishop": [],
            "Rook": [],
            "Queen": [],
            "King": [],
        }
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = chessboard.chesspieces[x][y]
                if (piece != 0):
                    chesspieces[x][y] = piece.clone()
                    
                    pieceRef = None

                    if piece.color == pieces.Piece.WHITE:
                        pieceRef = whitePieces
                    else:
                        pieceRef = blackPieces
                    
                    if piece.piece_type == "P":
                        temp = pieceRef["Pawn"]
                        temp.append(chesspieces[x][y])
                    elif piece.piece_type == "B":
                        pieceRef["Bishop"] = chesspieces[x][y]
                    elif piece.piece_type == "K":
                        pieceRef["Knight"] = chesspieces[x][y]
                    elif piece.piece_type == "R":
                        temp = pieceRef["Rook"]
                        temp.append(chesspieces[x][y])
                    elif piece.piece_type == "Q":
                        pieceRef["Queen"] = chesspieces[x][y]
                    elif piece.piece_type == "K":
                        pieceRef["King"] = chesspieces[x][y]

        return cls(chesspieces, chessboard.white_king_moved, chessboard.black_king_moved, whitePieces, blackPieces)

    @classmethod
    def new(cls):
        # @note: chess_pieces double array
        # @note: [i][j] => j=0 black, j=N white. || i = 0 left, i=N right
        chess_pieces = [[0 for x in range(Board.WIDTH)] for y in range(Board.HEIGHT)]
        whitePieces = {}
        blackPieces = {}
        
        # Create pawns.
        pawnArrayWhite = []
        pawnArrayBlack = []

        for x in range(Board.WIDTH):
            chess_pieces[x][Board.HEIGHT-2] = pieces.Pawn(x, Board.HEIGHT-2, pieces.Piece.WHITE)
            chess_pieces[x][1] = pieces.Pawn(x, 1, pieces.Piece.BLACK)
            
            pawnArrayWhite.append(chess_pieces[x][Board.HEIGHT-2])
            pawnArrayBlack.append(chess_pieces[x][1])
        
        whitePieces['Pawn'] = pawnArrayWhite
        blackPieces['Pawn'] = pawnArrayBlack

        # Create rooks.
        rookWhite1 = pieces.Rook(0, Board.HEIGHT-1, pieces.Piece.WHITE)
        rookWhite2 = pieces.Rook(Board.WIDTH-1, Board.HEIGHT-1, pieces.Piece.WHITE)
        rookBlack1 = pieces.Rook(0, 0, pieces.Piece.BLACK)
        rookBlack2 = pieces.Rook(Board.WIDTH-1, 0, pieces.Piece.BLACK)
        
        chess_pieces[0][Board.HEIGHT-1] = rookWhite1
        chess_pieces[Board.WIDTH-1][Board.HEIGHT-1] = rookWhite2
        chess_pieces[0][0] = rookBlack1
        chess_pieces[Board.WIDTH-1][0] = rookBlack2

        whitePieces['Rook'] = [rookWhite1, rookWhite2]
        blackPieces['Rook'] = [rookBlack1, rookBlack2]

        # Create Knights.
        knightWhite1 = pieces.Knight(1, Board.HEIGHT-1, pieces.Piece.WHITE)
        knightWhite2 = pieces.Knight(Board.WIDTH-2, Board.HEIGHT-1, pieces.Piece.WHITE)
        knightBlack1 = pieces.Knight(1, 0, pieces.Piece.BLACK)
        knightBlack2 = pieces.Knight(Board.WIDTH-2, 0, pieces.Piece.BLACK)

        chess_pieces[1][Board.HEIGHT-1] = knightWhite1
        chess_pieces[Board.WIDTH-2][Board.HEIGHT-1] = knightWhite2
        chess_pieces[1][0] = knightBlack1
        chess_pieces[Board.WIDTH-2][0] = knightBlack2

        whitePieces['Knight'] = [knightWhite1, knightWhite2]
        blackPieces['Knight'] = [knightBlack1, knightBlack2]

        # Create Bishops.
        bishopWhite1 = pieces.Bishop(2, Board.HEIGHT-1, pieces.Piece.WHITE)
        bishopWhite2 = pieces.Bishop(Board.WIDTH-3, Board.HEIGHT-1, pieces.Piece.WHITE)
        bishopBlack1 = pieces.Bishop(2, 0, pieces.Piece.BLACK)
        bishopBlack2 = pieces.Bishop(Board.WIDTH-3, 0, pieces.Piece.BLACK)

        chess_pieces[2][Board.HEIGHT-1] = bishopWhite1
        chess_pieces[Board.WIDTH-3][Board.HEIGHT-1] = bishopWhite2
        chess_pieces[2][0] = bishopBlack1
        chess_pieces[Board.WIDTH-3][0] = bishopBlack2

        whitePieces['Bishop'] = [bishopWhite1, bishopWhite2]
        blackPieces['Bishop'] = [bishopBlack1, bishopBlack2]

        # Create King & Queen.
        chess_pieces[4][Board.HEIGHT-1] = pieces.King(4, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[3][Board.HEIGHT-1] = pieces.Queen(3, Board.HEIGHT-1, pieces.Piece.WHITE)
        chess_pieces[4][0] = pieces.King(4, 0, pieces.Piece.BLACK)
        chess_pieces[3][0] = pieces.Queen(3, 0, pieces.Piece.BLACK)

        whitePieces['Queen'] = chess_pieces[3][Board.HEIGHT-1]
        blackPieces['Queen'] = chess_pieces[3][0]

        whitePieces['King'] = chess_pieces[4][Board.HEIGHT-1]
        blackPieces['King'] = chess_pieces[3][0]

        return cls(chess_pieces, False, False, whitePieces, blackPieces)

    def get_possible_moves(self, color):
        moves = []
        for x in range(Board.WIDTH):
            for y in range(Board.HEIGHT):
                piece = self.chesspieces[x][y]
                if (piece != 0):
                    if (piece.color == color):
                        moves += piece.get_possible_moves(self)

        return moves

    def perform_move(self, move):
        piece = self.chesspieces[move.xfrom][move.yfrom]
        piece.x = move.xto
        piece.y = move.yto
        self.chesspieces[move.xto][move.yto] = piece
        self.chesspieces[move.xfrom][move.yfrom] = 0

        if (piece.piece_type == pieces.Pawn.PIECE_TYPE):
            if (piece.y == 0 or piece.y == Board.HEIGHT-1):
                self.chesspieces[piece.x][piece.y] = pieces.Queen(piece.x, piece.y, piece.color)

        if (move.castling_move):
            if (move.xto < move.xfrom):
                rook = self.chesspieces[move.xfrom][0]
                rook.x = 2
                self.chesspieces[2][0] = rook
                self.chesspieces[0][0] = 0
            if (move.xto > move.xfrom):
                rook = self.chesspieces[move.xfrom][Board.HEIGHT-1]
                rook.x = Board.WIDTH-4
                self.chesspieces[Board.WIDTH-4][Board.HEIGHT-1] = rook
                self.chesspieces[move.xfrom][Board.HEIGHT-1] = 0

        if (piece.piece_type == pieces.King.PIECE_TYPE):
            if (piece.color == pieces.Piece.WHITE):
                self.white_king_moved = True
            else:
                self.black_king_moved = True

    # Returns if the given color is checked.
    def is_check(self, color):
        other_color = pieces.Piece.WHITE
        if (color == pieces.Piece.WHITE):
            other_color = pieces.Piece.BLACK

        for move in self.get_possible_moves(other_color):
            copy = Board.clone(self)
            copy.perform_move(move)

            king_found = False
            for x in range(Board.WIDTH):
                for y in range(Board.HEIGHT):
                    piece = copy.chesspieces[x][y]
                    if (piece != 0):
                        if (piece.color == color and piece.piece_type == pieces.King.PIECE_TYPE):
                            king_found = True

            if (not king_found):
                return True

        return False

    # Returns piece at given position or 0 if: No piece or out of bounds.
    def get_piece(self, x, y):
        if (not self.in_bounds(x, y)):
            return 0

        return self.chesspieces[x][y]

    def in_bounds(self, x, y):
        return (x >= 0 and y >= 0 and x < Board.WIDTH and y < Board.HEIGHT)

    def to_string(self):
        string =  "    A  B  C  D  E  F  G  H\n"
        string += "    -----------------------\n"
        for y in range(Board.HEIGHT):
            string += str(8 - y) + " | "
            for x in range(Board.WIDTH):
                piece = self.chesspieces[x][y]
                if (piece != 0):
                    string += piece.to_string()
                else:
                    string += ".. "
            string += "\n"
        return string + "\n"
