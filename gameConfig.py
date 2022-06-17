from board import Piece, Board, Move, Tile
from PIL import Image
from copy import deepcopy
from enums import PIECE_TYPES, TEAMS, MOVES

class Config():
    def __init__(self, settings: dict) -> None:
        self.board_height = settings['board_height']
        self.board_width = settings['board_width']
        self.window_height = settings['window_height']
        self.window_width = settings['window_width']
        self.icon_size = settings['icon_size']
        self.colors = settings['colors']
        self.pieces = settings['pieces']
        self.layout = settings['layout']
        self.funcs = settings['funcs']

class Chess_Config(Config):
    def __init__(self) -> None:
        # ADD 'CHECK' CHECK FOR FUNCTIONS

        directory = 'icons/'

        def add_to_pieces(pieces, piece, count):
            name = piece.name
            pieces[name] = []

            for _ in range(count):
                pieces[name].append(deepcopy(piece))

        SIZE = 100

        def white_pawn_func(board: Board, piece: Piece) -> list(MOVES):
            def get_next(count, sway=0) -> Tile:
                tile = piece.tile

                new_x = tile.coordinate_x if tile.coordinate_x + sway not in range(0, board.width) else tile.coordinate_x + sway

                new_tile = board.get_tile(new_x, tile.coordinate_y - count)

                if new_tile == None:
                    return None

                if not int(tile.name[1]) == int(new_tile.name[1]) + count:
                    new_tile = board.get_tile(new_x, tile.coordinate_y + count)

                return new_tile

            moves = []

            cur_x = piece.tile.coordinate_x
            cur_y = piece.tile.coordinate_y

            if not piece.has_moved:
                new_tile = get_next(2)

                if new_tile != None:
                    if new_tile.object == None:
                        moves.append(Move(piece, new_tile, MOVES.move))
            
            new_tile = get_next(1)
            if new_tile != None and new_tile.object == None:
                moves.append(Move(piece, new_tile, MOVES.move))

            new_tile = get_next(1, 1)
            if new_tile != None and new_tile.object != None and new_tile.object.team != piece.team:
                moves.append(Move(piece, new_tile, MOVES.capture))

            new_tile = get_next(1, -1)
            if new_tile != None and new_tile.object != None and new_tile.object.team != piece.team:
                moves.append(Move(piece, new_tile, MOVES.capture))

            return moves

        def black_pawn_func(board: Board, piece: Piece) -> list(MOVES):
            def get_next(count, sway=0) -> Tile:
                tile = piece.tile

                new_x = tile.coordinate_x if tile.coordinate_x + sway not in range(0, board.width) else tile.coordinate_x + sway

                new_tile = board.get_tile(new_x, tile.coordinate_y + count)

                if new_tile == None:
                    return None

                if not int(tile.name[1]) == int(new_tile.name[1]) - count:
                    new_tile = board.get_tile(new_x, tile.coordinate_y - count)

                return new_tile

            moves = []

            cur_x = piece.tile.coordinate_x
            cur_y = piece.tile.coordinate_y

            if not piece.has_moved:
                new_tile = get_next(2)

                if new_tile != None:
                    if new_tile.object == None:
                        moves.append(Move(piece, new_tile, MOVES.move))
            
            new_tile = get_next(1)
            if new_tile != None and new_tile.object == None:
                moves.append(Move(piece, new_tile, MOVES.move))

            new_tile = get_next(1, 1)
            if new_tile != None and new_tile.object != None and new_tile.object.team != piece.team:
                moves.append(Move(piece, new_tile, MOVES.capture))

            new_tile = get_next(1, -1)
            if new_tile != None and new_tile.object != None and new_tile.object.team != piece.team:
                moves.append(Move(piece, new_tile, MOVES.capture))

            return moves

        def knight_func(board: Board, piece: Piece) -> list(MOVES):
            dirs = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]

            moves = []

            for direction in dirs:
                tile = board.get_tile(piece.tile.coordinate_x + direction[1], piece.tile.coordinate_y  + direction[0])

                if tile == None:
                    continue

                if tile.object == None:
                    moves.append(Move(piece, tile, MOVES.move))
                    continue

                if tile.object.team == piece.team:
                    continue
                
                moves.append(Move(piece, tile, MOVES.capture))

            return moves

        def bishop_func(board: Board, piece: Piece) -> list(MOVES):
            dirs = [(-1, 1), (1, 1), (1, -1), (-1, -1)]

            moves = []

            for direction in dirs:
                for i in range(1, 8):
                    tile = board.get_tile(piece.tile.coordinate_x + direction[1] * i, piece.tile.coordinate_y  + direction[0] * i)

                    if tile == None:
                        break

                    if tile.object == None:
                        moves.append(Move(piece, tile, MOVES.move))
                        continue

                    if tile.object.team == piece.team:
                        break

                    moves.append(Move(piece, tile, MOVES.capture))
                    break

            return moves

        def rook_func(board: Board, piece: Piece) -> list(MOVES):
            dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

            moves = []

            for direction in dirs:
                for i in range(1, 8):
                    tile = board.get_tile(piece.tile.coordinate_x + direction[1] * i, piece.tile.coordinate_y  + direction[0] * i)

                    if tile == None:
                        break

                    if tile.object == None:
                        moves.append(Move(piece, tile, MOVES.move))
                        continue

                    if tile.object.team == piece.team:
                        break

                    moves.append(Move(piece, tile, MOVES.capture))
                    break

            return moves

        def queen_func(board: Board, piece: Piece) -> list(MOVES):
            dirs = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]

            moves = []

            for direction in dirs:
                for i in range(1, 8):
                    tile = board.get_tile(piece.tile.coordinate_x + direction[1] * i, piece.tile.coordinate_y  + direction[0] * i)

                    if tile == None:
                        break

                    if tile.object == None:
                        moves.append(Move(piece, tile, MOVES.move))
                        continue

                    if tile.object.team == piece.team:
                        break

                    moves.append(Move(piece, tile, MOVES.capture))
                    break

            return moves

        def king_func(board: Board, piece: Piece) -> list(MOVES):
            dirs = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]

            moves = []

            for direction in dirs:
                tile = board.get_tile(piece.tile.coordinate_x + direction[1], piece.tile.coordinate_y  + direction[0])

                if tile == None:
                    break

                if tile.object == None:
                    moves.append(Move(piece, tile, MOVES.move))
                    continue

                if tile.object.team == piece.team:
                    break

                moves.append(Move(piece, tile, MOVES.capture))

            return moves

        white_pawn_png = Image.open(directory + 'whitePawn.png').resize((SIZE, SIZE), Image.ANTIALIAS)
        white_pawn = Piece('white_pawn', PIECE_TYPES.pawn, white_pawn_png, team=TEAMS.white)
        white_rook_png = Image.open(directory + 'whiteRook.png').resize((SIZE, SIZE), Image.ANTIALIAS)
        white_rook = Piece('white_rook', PIECE_TYPES.rook, white_rook_png, team=TEAMS.white)
        white_knight_png = Image.open(directory + 'whiteKnight.png').resize((SIZE, SIZE), Image.ANTIALIAS)
        white_knight = Piece('white_knight', PIECE_TYPES.knight, white_knight_png, team=TEAMS.white)
        white_bishop_png = Image.open(directory + 'whiteBishop.png').resize((SIZE, SIZE), Image.ANTIALIAS)
        white_bishop = Piece('white_bishop', PIECE_TYPES.bishop, white_bishop_png, team=TEAMS.white)
        white_queen_png = Image.open(directory + 'whiteQueen.png').resize((SIZE, SIZE), Image.ANTIALIAS)
        white_queen = Piece('white_queen', PIECE_TYPES.queen, white_queen_png, team=TEAMS.white)
        white_king_png = Image.open(directory + 'whiteKing.png').resize((SIZE, SIZE), Image.ANTIALIAS)
        white_king = Piece('white_king', PIECE_TYPES.king, white_king_png, team=TEAMS.white)

        black_pawn_png = Image.open(directory + 'blackPawn.png').resize((SIZE, SIZE), Image.ANTIALIAS)
        black_pawn = Piece('black_pawn', PIECE_TYPES.pawn, black_pawn_png, team=TEAMS.black)
        black_rook_png = Image.open(directory + 'blackRook.png').resize((SIZE, SIZE), Image.ANTIALIAS)
        black_rook = Piece('black_rook', PIECE_TYPES.rook, black_rook_png, team=TEAMS.black)
        black_knight_png = Image.open(directory + 'blackKnight.png').resize((SIZE, SIZE), Image.ANTIALIAS)
        black_knight = Piece('black_knight', PIECE_TYPES.knight, black_knight_png, team=TEAMS.black)
        black_bishop_png = Image.open(directory + 'blackBishop.png').resize((SIZE, SIZE), Image.ANTIALIAS)
        black_bishop = Piece('black_bishop', PIECE_TYPES.bishop, black_bishop_png, team=TEAMS.black)
        black_queen_png = Image.open(directory + 'blackQueen.png').resize((SIZE, SIZE), Image.ANTIALIAS)
        black_queen = Piece('black_queen', PIECE_TYPES.queen, black_queen_png, team=TEAMS.black)
        black_king_png = Image.open(directory + 'blackKing.png').resize((SIZE, SIZE), Image.ANTIALIAS)
        black_king = Piece('black_king', PIECE_TYPES.king, black_king_png, team=TEAMS.black)

        pieces = {}

        add_to_pieces(pieces, white_pawn, 8)
        add_to_pieces(pieces, black_pawn, 8)
        add_to_pieces(pieces, white_rook, 2)
        add_to_pieces(pieces, black_rook, 2)
        add_to_pieces(pieces, white_knight, 2)
        add_to_pieces(pieces, black_knight, 2)
        add_to_pieces(pieces, white_bishop, 2)
        add_to_pieces(pieces, black_bishop, 2)
        add_to_pieces(pieces, white_queen, 1)
        add_to_pieces(pieces, black_queen, 1)
        add_to_pieces(pieces, white_king, 1)
        add_to_pieces(pieces, black_king, 1)

        colors = {'tile_dark': '#68946c', 'tile_light': '#f5f7d7', 'red': '#f06262', 'blue': '#a1adff', 'yellow': '#f7e77c'}
        layout = [['black_rook', 'black_knight', 'black_bishop', 'black_queen', 'black_king', 'black_bishop', 'black_knight', 'black_rook'],
                ['black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn'],
                [None, None, None, None, None, None, None, None,],
                [None, None, None, None, None, None, None, None,],
                [None, None, None, None, None, None, None, None,],
                [None, None, None, None, None, None, None, None,],
                ['white_pawn', 'white_pawn', 'white_pawn', 'white_pawn','white_pawn', 'white_pawn', 'white_pawn', 'white_pawn'],
                ['white_rook', 'white_knight', 'white_bishop', 'white_queen', 'white_king', 'white_bishop', 'white_knight', 'white_rook']
                ]

        funcs = {'white_pawn_func': white_pawn_func, 'black_pawn_func': black_pawn_func, 'knight_func': knight_func, 'bishop_func': bishop_func,
                'rook_func': rook_func, 'queen_func': queen_func, 'king_func': king_func, 'king_func': king_func}

        variables = {
            'board_height': 8,
            'board_width': 8,
            'window_height': 800,
            'window_width': 1000,
            'icon_size': SIZE,
            'colors': colors,
            'pieces': pieces,
            'layout': layout,
            'funcs': funcs
        }

        super().__init__(variables)
