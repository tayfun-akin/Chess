from board import *
from enums import *

import tkinter as tk
from PIL import ImageTk
import gameConfig as cfg

class Engine():
    def __init__(self, config: cfg.Config) -> None:
        self.board_height = config.board_height
        self.board_width = config.board_width
        self.window_height = config.window_height
        self.window_width = config.window_width
        self.icon_size = config.icon_size
        self.colors = config.colors
        self.pieces = config.pieces
        self.layout = config.layout
        self.funcs = config.funcs

        self.window = tk.Tk()
        self.window.geometry(f"{self.window_width}x{self.window_height}")
        #my_w.wm_attributes('-transparentcolor', 'grey')

        self.board = self.init_board()
        self.canvas = self.init_canvas()

        self.turn = config.starting_team

        # For tests, delet this
        self.window.mainloop()

    def get_func(self, name: str) -> Callable:
        if name == "white_pawn":
            return self.funcs['white_pawn_func']

        if name == "black_pawn":
            return self.funcs['black_pawn_func']

        return self.funcs[name.split('_')[1] + "_func"]

    def advance_turn(self) -> TEAMS:
        ind = 0 if (self.turn.value + 1) >= len(TEAMS) else self.turn.value + 1

        new_turn = TEAMS(ind)

        self.turn = new_turn

        return new_turn

    def init_board(self) -> Board:
        board = Board(self.board_height, self.board_width)

        piece_counts = {}

        for piece_name in self.pieces:
            piece_counts[piece_name] = 0

        for y in range(board.width):
            for x in range(board.height):
                tile = board.get_tile(x, y)
                piece_name = self.layout[y][x]

                if piece_name == None:
                    continue

                piece = self.pieces[piece_name][piece_counts[piece_name]]
                piece_counts[piece_name] += 1

                piece.move_func = self.get_func(piece_name)

                tile.object = piece
                piece.tile = tile

        return board

    def init_canvas(self) -> tk.Canvas:
        if not hasattr(self, 'board') or self.board == None:
            return None

        pixel_width = self.board_width * self.icon_size
        pixel_height = self.board_height * self.icon_size

        canvas = tk.Canvas(self.window, width=pixel_width, height=pixel_height)
        canvas.place(x=(self.window_width - pixel_width) / 2, y=0, anchor='nw')

        for y in range(self.board_height):
            y1 = y * self.icon_size
            y2 = y1 + self.icon_size

            for x in range(self.board_width):
                x1 = x * self.icon_size
                x2 = x1 + self.icon_size

                color = None

                if (x + y) % 2 == 0:
                    color = self.colors['tile_light']
                else:
                    color = self.colors['tile_dark']

                tile = self.board.get_tile(x, y)

                tile.update_attributes({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'org_color': color})

                widget = None

                if tile.object != None:
                    widget = self.create_piece(tile.object, canvas)

                tile.canvas_rect = canvas.create_rectangle((x1, y1, x2, y2), fill=color)

        return canvas

    def reset_canvas(self, canvas: tk.Canvas) -> None:
        for y in range(self.board.height):
            for x in range(self.board.width):
                tile = self.board.get_tile(x, y)

                if tile.object != None:
                    tile.object.widget.configure(bg=tile.attr['org_color'])

                canvas.itemconfig(tile.canvas_rect, fill=tile.attr['org_color'])

    def paint_moves(self, canvas: tk.Canvas, tile: Tile) -> None:
        if tile.object != None:
            moves = self.board.get_piece_moves(tile.object, self.turn)

            for m in moves:
                if m.type == MOVES.capture:
                    m.tile.object.widget.configure(bg=self.colors['red'])
                    continue

                canvas.itemconfig(m.tile.canvas_rect, fill=self.colors['yellow'])

            tile.object.is_moving = True

        canvas.itemconfig(tile.canvas_rect, fill=self.colors['blue'])
        tile.object.widget.configure(bg=self.colors['blue'])
        tile.object.widget.lift()

    def create_piece(self, piece: Piece, canvas: tk.Canvas=None) -> tk.Widget:
        if canvas==None:
            canvas = self.canvas

        def init_drag(event: tk.Event):
            coor_x = int((event.widget.winfo_x() + event.x) / self.icon_size)
            coor_y = int((event.widget.winfo_y() + event.y) / self.icon_size)

            tile = self.board.get_tile(coor_x, coor_y)

            self.paint_moves(canvas, tile)

        def drag(event: tk.Event):
            if type(event.widget) != tk.Label:
                return

            widget = event.widget

            new_x = widget.winfo_x() + event.x
            new_y = widget.winfo_y() + event.y

            widget.place(x=new_x, y=new_y, anchor = "center")

        def drop(event: tk.Event):
            coor_x = int((event.widget.winfo_x() + event.x) / self.icon_size)
            coor_y = int((event.widget.winfo_y() + event.y) / self.icon_size)

            tile = self.board.get_tile(coor_x, coor_y)

            piece = self.board.get_moving()
            if piece == None:
                return

            moves = self.board.get_piece_moves(piece, self.turn)

            new_x = piece.tile.attr['x1']
            new_y = piece.tile.attr['y1']
            new_color = piece.tile.attr['org_color']
            dest = piece.tile
            moving = False

            for m in moves:
                if m.tile == tile:
                    new_x = tile.attr['x1']
                    new_y = tile.attr['y1']
                    new_color = tile.attr['org_color']
                    dest = tile
                    moving = True

                    break

            event.widget.place(x=new_x, y=new_y, anchor = "nw")
            event.widget.configure(bg=new_color)

            self.board.move_piece(piece, dest)
            self.reset_canvas(canvas)

            piece.is_moving = False

            if moving:
                self.advance_turn()

        img = ImageTk.PhotoImage(piece.icon)
        piece.icon = img

        p_label = tk.Label(canvas, borderwidth=0, highlightthickness=0, image=img, bg='grey')

        p_label.place(x=piece.tile.attr['x1'], y=piece.tile.attr['y1'], anchor = "nw")
        p_label.configure(bg=piece.tile.attr['org_color'])

        p_label.bind('<B1-Motion>', drag)
        p_label.bind('<ButtonRelease-1>', drop)
        p_label.bind('<Button-1>', init_drag)

        piece.widget = p_label

        return p_label

if __name__ == "__main__":
    eng = Engine(cfg.Chess_Config())
