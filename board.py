# LIMITED TO 2D

from enum import Enum
from typing import Callable

MOVES = Enum("Relocate", "Capture")

class Tile():
    def __init__(self, coordinate_x: int, coordinate_y: int, object: any) -> None:
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y

        self.object = object

    def __str__(self) -> str:
        return "[" + str(self.object) if object != None else "" + "]"

class Board():
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width

        self.tiles = []

        for y in range(height):
            self.tiles.append([])

            for x in range(width):
                new_tile = Tile(x, y)

                self.tiles[y].append(new_tile)

    def get_tile(self, coordinate_x: int, coordinate_y: int) -> Tile:
        if coordinate_x <= self.width or coordinate_y <= self.height:
            return None

        return self.tiles[coordinate_y][coordinate_x]

    def __str__(self) -> str:
        return "\n".join([" ".join([str(self.tiles[y][x]) for x in range(self.width)]) for y in range(self.height)])

class Team():
    def __init__(self, name: str, color: tuple=None) -> None:
        self.name = name
        self.color = color

class Move():
    def __init__(self, coordinate_x: int, coordinate_y: int, type: MOVES=None) -> None:
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.type = type

class Piece():
    # ICON IS AN IMAGE
    def __init__(self, name: str, icon, team: Team=None, tile: Tile=None, board: Board=None,
                move_func: Callable[[int, int], list[Move]]=None) -> None:
        self.name = name
        self.icon = icon
        self.team = team
        self.tile = tile
        self.board = board
        self.move_func = move_func

    def get_possible_moves(self) -> list[Move]:
        moves = self.move_func(self.tile.coordinate_x, self.tile.coordinate_y)

        for m in moves:
            tile = self.board.get_tile(m.coordinate_x, m.coordinate_y)

            if tile == None:
                moves.remove(m)
                continue

            if tile.object == None or tile.object.team == self.team:
                moves.remove(m)
                continue

        return moves
