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

    def __str__(self) -> str:
        return self.name

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

    def copy_tiles(self) -> list[list[Tile]]:
        tiles = []

        for y in range(self.height):
            tiles.append([])

            for x in range(self.width):
                old_tile = self.tiles[y][x]

                new_tile = Tile(old_tile.name, x, y)

                new_tile.object = old_tile.object

                tiles[y].append(new_tile)

        return tiles

    def get_piece_moves(self, piece: Piece) -> list[Move]:
        all_moves = piece.move_func(self.tiles, piece)
        final_moves = []

        for m in all_moves:
            if not self.is_check(m):
                final_moves.append(m)

        return final_moves

    def get_team_pieces(self, team: TEAMS, tiles: list[list[Tile]]=None) -> list[Piece]:
        pieces = []

        tiles = tiles if tiles != None else self.tiles

        for y in range(self.height):
            for x in range(self.width):
                piece = tiles[y][x].object

                if piece != None and piece.team == team:
                    pieces.append(piece)

        return pieces

    def is_check(self, move: Move) -> bool:
        new_tiles = self.copy_tiles()

        new_tiles[move.tile.coordinate_y][move.tile.coordinate_x].object = new_tiles[move.piece.tile.coordinate_y][move.piece.tile.coordinate_x].object
        new_tiles[move.piece.tile.coordinate_y][move.piece.tile.coordinate_x].object = None

        pieces = self.get_team_pieces(TEAMS.black if move.piece.team == TEAMS.white else TEAMS.white , tiles=new_tiles)

        for piece in pieces:
            moves = piece.move_func(new_tiles, piece)

            for m in moves:
                if m.tile.object != None and m.tile.object.type == PIECE_TYPES.king:
                    return True

        return False

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

    def tile_to_str(self, tiles: list[list[Tile]]) -> str:
        return "\n".join([" ".join([str(tiles[y][x]) for x in range(len(tiles[0]))]) for y in range(len(tiles))])

    def __str__(self) -> str:
        return "\n".join([" ".join([str(self.tiles[y][x]) for x in range(self.width)]) for y in range(self.height)])
