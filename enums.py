from enum import Enum

class TEAMS(Enum):
    white = 0
    black = 1

class MOVES(Enum):
    capture = 0
    move = 1
    promote = 2

class PIECE_TYPES(Enum):
    pawn = 0
    rook = 1
    knight = 2
    bishop = 3
    queen = 4
    king = 5
