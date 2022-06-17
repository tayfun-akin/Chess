from enum import Enum

TEAMS = Enum('TEAMS', 'white black')
MOVES = Enum('MOVES', 'capture move promote')
PIECE_TYPES = Enum('PIECE_TYPES', 'pawn rook knight bishop queen king')
