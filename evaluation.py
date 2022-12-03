import numpy

import board
import pieces

main_diagonal_1 = [[0,7], [1,6], [2,5], [3,4], [4,3], [5,2],[1,6],[7,0]]
main_diagonal_2 = [[0,0], [1,1], [2,2], [3,3], [4,4], [5,5],[6,6],[7,7]]

middle_squares = [[4,4], [4,5], [5,4], [5,5]]

edges = [[0,0], [0,7], [7,0,], [7,7]]

def evaluation_current_color(board, piece, chess_pieces, x, y, currentcolor, my_pieces, rival_pieces, my_pawn_cnt_column):
    my_score = piece.value

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
                leftcolumnProtected.color == currentcolor or \
                rightcolumnProtected != 0 and \
                rightcolumnProtected.piece_type == "P" and \
                rightcolumnProtected.color == currentcolor:
            
                is_found_pawn = False
                if y != 0:
                    for row in range(y-1,-1,-1):
                        
                        leftcolumn = 0
                        rightcolumn = 0

                        if x != 0:
                            leftcolumn = chess_pieces[x-1][row]
                        if x != 7:
                            rightcolumn = chess_pieces[x + 1][row]

                        if leftcolumn != 0:
                            if leftcolumn.piece_type == "P" and leftcolumn.color != currentcolor:
                                is_found_pawn = True
                                break
                        if rightcolumn != 0:
                            if rightcolumn.piece_type == "P" and rightcolumn.color != currentcolor:
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

        if rivalking != 0:
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
        
        # Are Rooks At Same Row or Column
        rooks = my_pieces.get("R")

        for rook in rooks:
            if rook is not piece and rook != 0:
                if rook.x == piece.x or rook.y == piece.y:
                    my_score += 0.125


        # Open or Semi Open File
        file_situation = "open"
        for file_index in range(0, 8):
            
            currentpiece = chess_pieces[x][file_index]

            if currentpiece != 0:
                if currentpiece.piece_type == "P" and currentpiece.color == currentcolor:
                    file_situation = "closed"
                    break
                elif currentpiece.piece_type == "P" and currentpiece.color != currentcolor:
                    file_situation = "semi-open"
                else:
                    continue

        if file_situation == "open":
            my_score += 0.75
        elif file_situation == "semi-open":
            my_score += 0.5

    elif piece.piece_type == "Q":
        pass
    else:
        # Weakness of pawns near king
        pass
    return my_score

def evaluation_rival_color(board, piece, chess_pieces, x, y, rivalcolor, my_pieces, rival_pieces, rival_pawn_cnt_column):
    rival_score = piece.value

    if piece.piece_type == "P":
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
                if y != 7:
                    for row in range(y+1, 8):
                        
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
        myking = my_pieces.get("K")[0]

        if myking != 0:
            moves = piece.get_possible_diagonal_moves(board)
            
            min = 7

            for move in moves:
                xdif = abs(myking.x - move.xto)
                ydif = abs(myking.y - move.yto)

                if xdif + ydif < min:
                    min = xdif + ydif

            if min < 3:
                rival_score += 0.8

    elif piece.piece_type == "R":
        # Is Rook At Edges
        if y == 0 or y == 7 or x == 0 or x == 7:
            rival_score -= 0.25

        # Are Rooks At Same Row or Column
        rooks = rival_pieces.get("R")

        for rook in rooks:
            if rook is not piece and rook != 0:
                if rook.x == piece.x or rook.y == piece.y:
                    rival_score += 0.125

        # Open or Semi Open File
        file_situation = "open"
        for file_index in range(0, 8):
            
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
        pass

    else:
        # Weakness of pawns near king
        pass
    
    return rival_score

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