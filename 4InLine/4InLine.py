import tkinter as tk

BG_COLOR = "#121212"
GOLD = "#D4AF37"
WHITE = "#EAEAEA"
BLACK_PIECE = "#000000"
GOLD_PIECE = "#D4AF37"

ROWS, COLS = 6, 7
CELL_SIZE = 80
WINDOW_WIDTH, WINDOW_HEIGHT = 900, 700

root = tk.Tk()
root.title("4inLine")
root.configure(bg=BG_COLOR)
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.resizable(False, False)

board = [[None]*COLS for _ in range(ROWS)]
current_player = BLACK_PIECE
game_over = False
winner = None
winning_cells = []
game_started = False
history = []

def copy_board(b):
    return [row[:] for row in b]

def save_history(result):
    history.insert(0, {
        "winner": result,
        "board": copy_board(board),
        "winning_cells": winning_cells[:]
    })
    del history[5:]

def switch_screen(show):
    menu_frame.pack_forget()
    game_frame.pack_forget()
    history_frame.pack_forget()
    show.pack(expand=True)

# menu_______________________________________________________
def update_menu_buttons():
    for w in menu_buttons_frame.winfo_children():
        w.destroy()

    tk.Button(
        menu_buttons_frame, text="Nuova Partita",
        font=("Helvetica",18,"bold"),
        bg=GOLD, fg="black",
        padx=35, pady=12,
        command=start_new_game
    ).pack(pady=12)

    if game_started:
        tk.Button(
            menu_buttons_frame, text="Continua Partita",
            font=("Helvetica",16,"bold"),
            bg="#1E1E1E", fg=GOLD,
            padx=30, pady=10,
            command=lambda: switch_screen(game_frame)
        ).pack(pady=8)

    tk.Button(
        menu_buttons_frame, text="Cronologia Partite",
        font=("Helvetica",15,"bold"),
        bg="#1E1E1E", fg=WHITE,
        padx=28, pady=10,
        command=show_history
    ).pack(pady=20)

# __________________________________________________________
def start_new_game():
    global board, current_player, game_over, winner, game_started, winning_cells
    board = [[None]*COLS for _ in range(ROWS)]
    current_player = BLACK_PIECE
    game_over = False
    winner = None
    winning_cells = []
    game_started = True
    draw_board()
    update_status()
    switch_screen(game_frame)

def update_status():
    if game_over:
        status_label.config(text=f"Vince il Giocatore {winner}")
    else:
        status_label.config(
            text=f"Turno Giocatore {'Nero' if current_player == BLACK_PIECE else 'Oro'}"
        )

def draw_board(custom=None, highlight=None):
    canvas.delete("all")
    b = custom if custom else board
    h = highlight if highlight else []

    for r in range(ROWS):
        for c in range(COLS):
            x1,y1 = c*CELL_SIZE, r*CELL_SIZE
            x2,y2 = x1+CELL_SIZE, y1+CELL_SIZE
            canvas.create_rectangle(
                x1,y1,x2,y2,
                fill="#1E1E1E",
                outline=GOLD,
                width=2
            )

            if b[r][c]:
                is_win = (r,c) in h
                canvas.create_oval(
                    x1+10,y1+10,x2-10,y2-10,
                    fill=b[r][c],
                    outline=GOLD if is_win else "",
                    width=5 if is_win else 0
                )

def drop_piece(col):
    global current_player, game_over, winner, winning_cells
    if game_over:
        return

    for r in range(ROWS-1,-1,-1):
        if board[r][col] is None:
            board[r][col] = current_player

            if check_win(r,col):
                game_over = True
                winner = "Nero" if current_player == BLACK_PIECE else "Oro"
                draw_board(highlight=winning_cells)
                save_history(winner)
                update_status()
                return

            draw_board()

            if all(board[0][c] for c in range(COLS)):
                game_over = True
                winner = "Pareggio"
                save_history("Pareggio")
                status_label.config(text="Pareggio")
                return

            current_player = GOLD_PIECE if current_player == BLACK_PIECE else BLACK_PIECE
            update_status()
            return

def check_win(row,col):
    global winning_cells
    directions = [(1,0),(0,1),(1,1),(1,-1)]

    for dx,dy in directions:
        cells = [(row,col)]

        r,c = row+dy, col+dx
        while 0<=r<ROWS and 0<=c<COLS and board[r][c]==current_player:
            cells.append((r,c))
            r+=dy; c+=dx

        r,c = row-dy, col-dx
        while 0<=r<ROWS and 0<=c<COLS and board[r][c]==current_player:
            cells.insert(0,(r,c))
            r-=dy; c-=dx

        if len(cells) >= 4:
            winning_cells = cells[:4]
            return True

    winning_cells = []
    return False

def click(e):
    drop_piece(e.x//CELL_SIZE)

# sezione cronologia__________________________________________
def show_history():
    for w in history_list.winfo_children():
        w.destroy()

    if not history:
        tk.Label(history_list, text="Nessuna partita salvata",
                 fg=WHITE, bg=BG_COLOR, font=("Helvetica",14)).pack(pady=20)
    else:
        for i,h in enumerate(history):
            tk.Button(
                history_list,
                text=f"{i+1}) Vincitore: {h['winner']}",
                bg="#1E1E1E", fg=GOLD,
                command=lambda x=h: preview_history(x)
            ).pack(fill="x", padx=20, pady=6)

    switch_screen(history_frame)

def preview_history(h):
    global board, winning_cells, game_over, winner
    board = copy_board(h["board"])
    winning_cells = h["winning_cells"]
    game_over = True
    winner = h["winner"]
    draw_board(highlight=winning_cells)
    update_status()
    switch_screen(game_frame)

menu_frame = tk.Frame(root, bg=BG_COLOR)

tk.Label(
    menu_frame,
    text="4inLine",
    font=("Times New Roman",42,"bold"),
    fg=GOLD,
    bg=BG_COLOR
).pack(pady=30)

tk.Label(
    menu_frame,
    text="D&G SoftwareHouse",
    font=("Calibri",16),
    fg=WHITE,
    bg=BG_COLOR
).pack()

menu_buttons_frame = tk.Frame(menu_frame, bg=BG_COLOR)
menu_buttons_frame.pack(pady=40)
update_menu_buttons()



game_frame = tk.Frame(root, bg=BG_COLOR)

top = tk.Frame(game_frame, bg=BG_COLOR)
top.pack(fill="x")

tk.Button(
    top, text="Menu",
    bg="#1E1E1E", fg=GOLD,
    command=lambda: (update_menu_buttons(), switch_screen(menu_frame))
).pack(side="right", padx=15)

status_label = tk.Label(
    top, font=("Helvetica",16,"bold"),
    fg=WHITE, bg=BG_COLOR
)
status_label.pack(side="left", padx=30)

canvas = tk.Canvas(
    game_frame,
    width=COLS*CELL_SIZE,
    height=ROWS*CELL_SIZE,
    bg=BG_COLOR
)
canvas.pack()
canvas.bind("<Button-1>", click)



history_frame = tk.Frame(root, bg=BG_COLOR)

tk.Label(
    history_frame,
    text="Cronologia Partite",
    font=("Helvetica",26,"bold"),
    fg=GOLD, bg=BG_COLOR
).pack(pady=20)

history_list = tk.Frame(history_frame, bg=BG_COLOR)
history_list.pack(expand=True)

tk.Button(
    history_frame,
    text="Indietro al Menu",
    bg="#1E1E1E", fg=GOLD,
    command=lambda: (update_menu_buttons(), switch_screen(menu_frame))
).pack(pady=20)

# avvia gioco
switch_screen(menu_frame)
root.mainloop()
