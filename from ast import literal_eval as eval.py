from ast import literal_eval as eval

board_size = 8
BLACK = '\u26AB'
WHITE = '\u26AA'
EMPTY = '\u2B1c'
offsets = ((0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1))

def inverse(piece):
    return BLACK if piece is WHITE else WHITE

def main():
    if input('Display instructions? [Y/N]: ').lower() == 'y':
        instructions()
    board = create_board()
    piece = BLACK
    while has_valid_move(board, piece):
        game_loop(board, piece)
        if has_valid_move(board, inverse(piece)):
            piece = inverse(piece)
    print_board(board)
    black, white = 0,0
    for row in board:
        for token in row:
            if token is WHITE: white += 1
            if token is BLACK: black += 1
    if black == white:
        print("It's a tie!")
    else:
        print()
        print('{token} is the winner!' % (BLACK if black>white else WHITE))
    return

def instructions():
    print('''
Reversi, also known as Othello, is a strategy board game for two players.
The two players alternate placing Black and White tokens on the board,
respectively, and the winner is whomever has the most tokens of their color
on the board when no legal moves remain.'''\
          )
    input('\nPress Enter to continue...')
    print('''
A legal move is one that causes other pieces to flip between White and Black.
A move causes pieces of the opposite color to flip when placed down if and
only if there is an unbroken line between it and another piece of the same
color consisting of pieces of the opposite color.'''\
          )
    input('\nPress Enter to continue...')
    print('''
To play this version, when prompted, enter the cartesian coordinates of the
location that you would like to place the piece. The upper left corner of the
board is 0,0 and the lower right is {0},{0}.'''.format(board_size-1)\
          )
    input('\nPress Enter to continue...')

def create_board():
    board = [[EMPTY for x in range(board_size)] for x in range(board_size)]
    half = board_size//2
    board[half-1][half-1] = WHITE
    board[half][half] = WHITE
    board[half-1][half] = BLACK
    board[half][half-1] = BLACK
    return board

def print_board(board):
    for row in range(len(board)):
        print(*board[row], sep='')
    return

def game_loop(board, piece):
    print()
    print_board(board)
    while(True):
        try:
            move = eval(input('Place %s where? ' % piece))
            move = tuple(reversed(move))
            # x,y -> y,x (easier to use)
            if is_valid_move(board, piece, move):
                place_piece(board, piece, move)
                return
            else:
                raise AssertionError
        except (TypeError, ValueError, IndexError, SyntaxError, AssertionError):
            #   ------------------bad  input------------------  ---bad move---
            print('Invalid move. Try again.')

def is_valid_move(board, piece, move):
    if board[move[0]][move[1]] is not EMPTY: return False
    for offset in offsets:
        check = [move[0]+offset[0], move[1]+offset[1]]
        while 0<=check[0]<board_size-1 and 0<=check[1]<board_size-1 and \
              board[check[0]][check[1]] is inverse(piece):
            check[0] += offset[0]
            check[1] += offset[1]
            if board[check[0]][check[1]] is piece:
                return True
    return False

def place_piece(board, piece, move):
    board[move[0]][move[1]] = piece
    for offset in offsets:
        check = [move[0]+offset[0], move[1]+offset[1]]
        while 0<=check[0]<board_size and 0<=check[1]<board_size:
            if board[check[0]][check[1]] is EMPTY: break
            if board[check[0]][check[1]] is piece:
                flip(board, piece, move, offset)
                break
            check[0] += offset[0]
            check[1] += offset[1]
    return

def flip(board, piece, move, offset):
    check = [move[0]+offset[0], move[1]+offset[1]]
    while(board[check[0]][check[1]] is inverse(piece)):
        board[check[0]][check[1]] = piece
        check[0] += offset[0]
        check[1] += offset[1]
    return

def has_valid_move(board, piece):
    for y in range(board_size):
        for x in range(board_size):
            if is_valid_move(board, piece, (y,x)): return True
    return False

if __name__ == '__main__':
    main()