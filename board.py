# LIMITED TO 2D
from enums import PIECE_TYPES, TEAMS

from enum import Enum
from typing import Any, Callable
from PIL import Image
from copy import deepcopy
import tkinter as tk

def generate_tile_name(x: int, y: int) -> str:
    lettering = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    new_y = 8 - y
    new_x = lettering[x]

    return f"{x}{y}"

class Tile():
    # DETERMINE THE DATA TYPE
    def __init__(self, name: str, coordinate_x: int, coordinate_y: int, obj: Any=None, canvas_rect=None, org_color:str=None, attr: dict={}) -> None:
        self.name = name
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y

        self.object = obj
        self.canvas_rect = canvas_rect
        self.org_color = org_color
        self.attr = deepcopy(attr)

    def update_attributes(self, attr: dict) -> None:
        for val in attr:
            self.attr[val] = attr[val]

    def __str__(self) -> str:
        return "[" + (str(self.object) if self.object != None else "") + "]"

class Piece():
    def __init__(self, name: str, type: Enum, icon: Image, team: TEAMS=None, tile: Tile=None,
                move_func: Callable[[int, int], list]=None, widget: tk.Widget=None) -> None:
        self.name = name
        self.type = type
        self.icon = icon
        self.team = team
        self.tile = tile
        self.move_func = move_func
        self.widget = widget

        self.has_moved = False
        self.is_moving = False
        self.is_captured = False

class Move():
    def __init__(self, piece: Piece, tile: Tile=None, type: Enum=None) -> None:
        self.piece = piece
        self.tile = tile
        self.type = type

class Board():
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width

        self.tiles = []

        for y in range(height):
            self.tiles.append([])

            for x in range(width):
                new_tile = Tile(generate_tile_name(x, y), x, y)

                self.tiles[y].append(new_tile)

# DOES NOT WORK YET
#------------------------------------------------------------------------------------------------

    def get_team_pieces(self, team: TEAMS) -> list[Piece]:
        pieces = []

        for y in self.height:
            for x in self.width:
                piece = self.tiles[y][x].object

                if piece.team == team:
                    pieces.append(piece)

        return pieces

    def is_check(self, move: Move) -> bool:
        new_board = Board(self.height, self.width)
        new_board.tiles = deepcopy(self.tiles)

        new_board.move_piece(move=move)

        pieces = new_board.get_team_pieces(move.piece.team)

        for piece in pieces:
            moves = piece.move_func(new_board, piece)

            for move in moves:
                if move.tile.object != None and move.tile.object.type == PIECE_TYPES.king:
                    return True

        return False

#------------------------------------------------------------------------------------------------

    def capture_piece(self, piece: Piece) -> None:
        piece.is_captured = True
        piece.tile.object = None

        piece.tile = None
        piece.widget.destroy()
        piece.widget = None

    # Move has priority if both dest and move given
    def move_piece(self, piece: Piece=None, dest: Tile=None, move: Move=None) -> None:
        if move != None:
            dest = move.tile
            piece = move.piece

        old_tile = piece.tile

        if old_tile != dest:            
            piece.has_moved = True

        old_tile.object = None

        if dest.object != None:
            self.capture_piece(dest.object)

        dest.object = piece
        piece.tile = dest

    def get_tile(self, coordinate_x: int, coordinate_y: int) -> Tile:
        if not (coordinate_x in range(self.width) and coordinate_y in range(self.height)):
            return None

        return self.tiles[coordinate_y][coordinate_x]

    def get_moving(self) -> Piece:
        for row in self.tiles:
            for tile in row:
                if tile.object != None:
                    if tile.object.is_moving:
                        return tile.object

        return None

    def __str__(self) -> str:
        return "\n".join([" ".join([str(self.tiles[y][x]) for x in range(self.width)]) for y in range(self.height)])
