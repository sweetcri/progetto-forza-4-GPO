import tkinter as tk

#costanti della grafica-------------------------------------
BG_COLOR = "#121212"
GOLD = "#D4AF37"
WHITE = "#FFFFFF"
TEXT_WHITE = "#EAEAEA"
BLACK_PIECE = "#000000"
GOLD_PIECE = "#D4AF37"

ROWS, COLS = 6, 7
CELL_SIZE = 80
WINDOW_WIDTH, WINDOW_HEIGHT = 900, 700
DROP_SPEED = 14

#schermata---------------------------------------------
root = tk.Tk()
root.title("4inLine")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

#variabili--------------------------------------------------
board = [[None]*COLS for _ in range(ROWS)]
current_player = BLACK_PIECE
game_over = False
winner = None
winning_cells = []
game_started = False
is_animating = False

history = []
stats = {"Nero": 0, "Oro": 0, "Pareggio": 0, "Totali": 0}

def copy_board(b):
    return [row[:] for row in b]

def switch_screen(show):
    for f in (menu_frame, game_frame, history_frame, stats_frame):
        f.pack_forget()
    show.pack(expand=True)

def save_history(result):
    stats["Totali"] += 1
    if result in stats:
        stats[result] += 1

    history.insert(0, {
        "winner": result,
        "board": copy_board(board),
        "winning": winning_cells[:]
    })
    del history[5:]

#menu------------------------------------------------------
def update_menu_buttons():
    for w in menu_buttons.winfo_children():
        w.destroy()

    tk.Button(menu_buttons, text="Nuova Partita",
              font=("Helvetica",18,"bold"),
              bg=GOLD, fg="black",
              command=start_new_game).pack(pady=12)

    if game_started:
        tk.Button(menu_buttons, text="Continua Partita",
                  font=("Helvetica",15,"bold"),
                  bg="#1E1E1E", fg=GOLD,
                  command=lambda: switch_screen(game_frame)).pack(pady=8)

    tk.Button(menu_buttons, text="Cronologia Partite",
              font=("Helvetica",15,"bold"),
              bg="#1E1E1E", fg=TEXT_WHITE,
              command=show_history).pack(pady=8)

    tk.Button(menu_buttons, text="Statistiche",
              font=("Helvetica",15,"bold"),
              bg="#1E1E1E", fg=TEXT_WHITE,
              command=show_stats).pack(pady=8)

# gioco--------------------------------------------------------------------------
def start_new_game():
    global board, current_player, game_over, winner, winning_cells, game_started
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
            x1, y1 = c*CELL_SIZE, r*CELL_SIZE
            x2, y2 = x1+CELL_SIZE, y1+CELL_SIZE

            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="#1E1E1E",
                outline=GOLD,
                width=2
            )

            if b[r][c]:
                win = (r, c) in h
                canvas.create_oval(
                    x1+10, y1+10, x2-10, y2-10,
                    fill=b[r][c],
                    outline=WHITE if win else "",
                    width=5 if win else 0
                )

def animate_drop(col, row):
    global is_animating
    is_animating = True

    x = col * CELL_SIZE + CELL_SIZE//2
    y = -40
    target_y = row * CELL_SIZE + CELL_SIZE//2

    piece = canvas.create_oval(
        x-30, y-30, x+30, y+30,
        fill=current_player, outline=""
    )

    def fall():
        nonlocal y
        if y < target_y:
            y += DROP_SPEED
            canvas.move(piece, 0, DROP_SPEED)
            root.after(10, fall)
        else:
            canvas.delete(piece)
            finalize_drop(col, row)

    fall()

def finalize_drop(col, row):
    global current_player, game_over, winner, is_animating

    board[row][col] = current_player
    is_animating = False

    if check_win(row, col):
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

def drop_piece(col):
    if game_over or is_animating:
        return
    for r in range(ROWS-1, -1, -1):
        if board[r][col] is None:
            animate_drop(col, r)
            return

def check_win(row, col):
    global winning_cells
    directions = [(1,0),(0,1),(1,1),(1,-1)]

    for dx, dy in directions:
        cells = [(row, col)]

        r, c = row+dy, col+dx
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == current_player:
            cells.append((r, c))
            r += dy
            c += dx

        r, c = row-dy, col-dx
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == current_player:
            cells.insert(0, (r, c))
            r -= dy
            c -= dx

        if len(cells) >= 4:
            winning_cells = cells[:4]
            return True

    winning_cells = []
    return False

def click(e):
    drop_piece(e.x // CELL_SIZE)

# cronoligia--------------------------------------
def show_history():
    for w in history_list.winfo_children():
        w.destroy()

    if not history:
        tk.Label(history_list, text="Nessuna partita salvata",
                 fg=TEXT_WHITE, bg=BG_COLOR,
                 font=("Helvetica",14)).pack(pady=20)
    else:
        for i, h in enumerate(history):
            tk.Button(history_list,
                      text=f"{i+1}) Vincitore: {h['winner']}",
                      bg="#1E1E1E", fg=GOLD,
                      command=lambda x=h: preview_history(x)).pack(fill="x", pady=6)

    switch_screen(history_frame)

def preview_history(h):
    global board, winning_cells, game_over, winner
    board = copy_board(h["board"])
    winning_cells = h["winning"]
    game_over = True
    winner = h["winner"]
    draw_board(highlight=winning_cells)
    update_status()
    switch_screen(game_frame)

#statistiche-----------------------------------------
def show_stats():
    for w in stats_frame.winfo_children():
        w.destroy()

    tk.Label(stats_frame, text="Statistiche Giocatori",
             font=("Helvetica",26,"bold"),
             fg=GOLD, bg=BG_COLOR).pack(pady=30)

    for k in ["Totali", "Nero", "Oro", "Pareggio"]:
        tk.Label(stats_frame,
                 text=f"{k}: {stats[k]}",
                 font=("Helvetica",16),
                 fg=TEXT_WHITE,
                 bg=BG_COLOR).pack(pady=6)

    tk.Button(stats_frame, text="Indietro",
              bg="#1E1E1E", fg=GOLD,
              command=lambda: (update_menu_buttons(), switch_screen(menu_frame))
              ).pack(pady=30)

    switch_screen(stats_frame)

#vari frame------------------------------------------
menu_frame = tk.Frame(root, bg=BG_COLOR)
game_frame = tk.Frame(root, bg=BG_COLOR)
history_frame = tk.Frame(root, bg=BG_COLOR)
stats_frame = tk.Frame(root, bg=BG_COLOR)

#menu--------------------------------------------
tk.Label(menu_frame, text="4inLine",
         font=("Times New Roman",42,"bold"),
         fg=GOLD, bg=BG_COLOR).pack(pady=30)

tk.Label(menu_frame, text="D&G SoftwareHouse",
         font=("Calibri",16),
         fg=TEXT_WHITE, bg=BG_COLOR).pack()

menu_buttons = tk.Frame(menu_frame, bg=BG_COLOR)
menu_buttons.pack(pady=40)
update_menu_buttons()

#gioco----------------------------------------------
top = tk.Frame(game_frame, bg=BG_COLOR)
top.pack(fill="x")

status_label = tk.Label(top, font=("Helvetica",16,"bold"),
                        fg=TEXT_WHITE, bg=BG_COLOR)
status_label.pack(side="left", padx=20)

tk.Button(top, text="Menu", bg="#1E1E1E", fg=GOLD,
          command=lambda: (update_menu_buttons(), switch_screen(menu_frame))
          ).pack(side="right", padx=20)

canvas = tk.Canvas(game_frame,
                   width=COLS*CELL_SIZE,
                   height=ROWS*CELL_SIZE,
                   bg=BG_COLOR)
canvas.pack()
canvas.bind("<Button-1>", click)

tk.Label(history_frame, text="Cronologia Partite",
         font=("Helvetica",26,"bold"),
         fg=GOLD, bg=BG_COLOR).pack(pady=20)

history_list = tk.Frame(history_frame, bg=BG_COLOR)
history_list.pack(expand=True)

tk.Button(history_frame, text="Indietro",
          bg="#1E1E1E", fg=GOLD,
          command=lambda: (update_menu_buttons(), switch_screen(menu_frame))
          ).pack(pady=20)

# avvio-------------------------------------------
switch_screen(menu_frame)
root.mainloop()
