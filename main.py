import board, pieces, ai
import random

# Returns a move object based on the users input. Does not check if the move is valid.
def get_user_move():
    print("Example Move: A2 A4")
    move_str = input("Your Move: ")
    move_str = move_str.replace(" ", "")

    try:
        xfrom = letter_to_xpos(move_str[0:1])
        yfrom = 8 - int(move_str[1:2]) # The board is drawn "upside down", so flip the y coordinate.
        xto = letter_to_xpos(move_str[2:3])
        yto = 8 - int(move_str[3:4]) # The board is drawn "upside down", so flip the y coordinate.
        return ai.Move(xfrom, yfrom, xto, yto, False)
    except ValueError:
        print("Invalid format. Example: A2 A4")
        return get_user_move()

# Returns a valid move based on the users input.
def get_valid_user_move(board, userColor):
    while True:
        move = get_user_move()
        valid = False
        possible_moves = board.get_possible_moves(userColor)
        # No possible moves
        if (not possible_moves):
            return 0

        for possible_move in possible_moves:
            if (move.equals(possible_move)):
                move.castling_move = possible_move.castling_move
                valid = True
                break

        if (valid):
            break
        else:
            print("Invalid move.")
    return move

# Converts a letter (A-H) to the x position on the chess board.
def letter_to_xpos(letter):
    letter = letter.upper()
    if letter == 'A':
        return 0
    if letter == 'B':
        return 1
    if letter == 'C':
        return 2
    if letter == 'D':
        return 3
    if letter == 'E':
        return 4
    if letter == 'F':
        return 5
    if letter == 'G':
        return 6
    if letter == 'H':
        return 7

    raise ValueError("Invalid letter.")


def updateSquare():
    #Update one of the black square
    #Update one of the white square

    redX = random.randint(0,7)
    redY = random.randint(0,7)

    blueX = random.randint(0,7)
    blueY = random.randint(0,7)

    #color the expected numbers

#
# Entry point.
#
board = board.Board.new()
print(board.to_string())

turnNumber = 0

#TODO: Take Color As Input
# color = input("Your Color: ")
color = pieces.Piece.WHITE

userColor = color
botColor = pieces.Piece.flipColor(userColor)

while True:

    turnNumber += 1

    if turnNumber % 5 == 0:
        updateSquare()

    move = get_valid_user_move(board, userColor)
    if (move == 0):
        if (board.is_check(userColor)):
            print("Checkmate. Black Wins.")
            break
        else:
            print("Stalemate.")
            break

    board.perform_move(move)

    print("User move: " + move.to_string())
    print(board.to_string())

    ai_move = ai.AI.get_ai_move(board, [], botColor)
    if (ai_move == 0):
        if (board.is_check(botColor)):
            print("Checkmate. White wins.")
            break
        else:
            print("Stalemate.")
            break

    board.perform_move(ai_move)
    print("AI move: " + ai_move.to_string())
    print(board.to_string())
