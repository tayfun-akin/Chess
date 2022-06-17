import tkinter as tk 
from PIL import Image, ImageTk

my_w = tk.Tk()
my_w.geometry("1000x800")
#my_w.wm_attributes('-transparentcolor', 'grey')

SIZE = 100

canvas = tk.Canvas(my_w, width=800, height=800)
canvas.place(x=100, y=0, anchor='nw')

colors = ['#f5f7d7', '#68946c', '#f06262']

counter = 0

img_p = Image.open('icons/blackPawn.png').resize((SIZE, SIZE), Image.ANTIALIAS)
print(img_p.mode)
img_pawn = ImageTk.PhotoImage(img_p)

img_q = Image.open('icons/blackQueen.png').resize((SIZE, SIZE), Image.ANTIALIAS)
print(img_q.mode)
img_queen = ImageTk.PhotoImage(img_q)

board = []

for y in range(8):
    board.append([])

    y1 = y * SIZE
    y2 = y1 + SIZE

    for x in range(8):
        x1 = x * SIZE
        x2 = x1 + SIZE

        color = colors[(x + y) % 2]

        board[-1].append((x1, y1, x2, y2, color))

        canvas.create_rectangle((x1, y1, x2, y2), fill=color)

def get_tile(cur_x: int, cur_y: int) -> tuple:
    new_x = None
    new_y = None
    color = None

    for r in board:
        for t in r:
            if t[0] <= cur_x and t[2] >= cur_x:
                if t[1] <= cur_y and t[3] >= cur_y:
                    new_x = t[0]
                    new_y = t[1]
                    color = t[4]

    return (new_x, new_y, color)

def init_drag(event: tk.Event):
    widget = event.widget

    color = "#f06262"

    widget.configure(bg=color)
    widget.lift()

def drag(event: tk.Event):
    global canvas

    if type(event.widget) != tk.Label:
        return

    widget = event.widget

    new_x = widget.winfo_x() + event.x
    new_y = widget.winfo_y() + event.y

    widget.place(x=new_x, y=new_y, anchor = "center")

def drop(event: tk.Event):
    global board

    cur_x = event.widget.winfo_x() + event.x
    cur_y = event.widget.winfo_y() + event.y

    new_x, new_y, color = get_tile(cur_x, cur_y)

    event.widget.place(x=new_x, y=new_y, anchor = "nw")
    event.widget.configure(bg=color)

def create_piece(coor_x, coor_y, my_img):
    piece = tk.Label(canvas, borderwidth=0, highlightthickness=0, image=my_img, bg='grey')

    new_x, new_y, color = get_tile(coor_x, coor_y)
    piece.place(x=new_x, y=new_y, anchor = "nw")
    piece.configure(bg=color)

    piece.bind('<B1-Motion>', drag)
    piece.bind('<ButtonRelease-1>', drop)
    piece.bind('<Button-1>', init_drag)

def create_pawns():
    for i in range(8):
        create_piece(i * SIZE, 1 * SIZE, img_pawn)

def set_up_pieces():
    create_pawns()

    create_piece(3 * SIZE, 0, img_queen)

set_up_pieces()

my_w.mainloop()
