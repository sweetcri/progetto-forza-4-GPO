import tkinter as tk
from PIL import Image, ImageTk

# ---------------- COSTANTI GRAFICHE ----------------
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

TITLE_FONT = ("Impact", 56)
SUB_FONT = ("Helvetica", 14)
BTN_FONT = ("Helvetica", 18, "bold")
BTN_BG = "#1E1E1E"
BTN_HOVER = "#2A2A2A"

# ---------------- FINESTRA ----------------
root = tk.Tk()
root.title("4inLine - Gold Edition")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

# --- CARICAMENTO IMMAGINE DI SFONDO ---
try:
    bg_image_raw = Image.open("sfondo4InLine.jpg")
    bg_image_raw = bg_image_raw.resize((WINDOW_WIDTH, WINDOW_HEIGHT), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image_raw)
except Exception as e:
    print(f"Errore caricamento immagine: {e}")
    bg_photo = None

# ---------------- VARIABILI ----------------
board = [[None]*COLS for _ in range(ROWS)]
current_player = BLACK_PIECE
game_over = False
winner = None
winning_cells = []
game_started = False
is_animating = False
game_mode = None

players = []
current_player_index = 0
PLAYER_COLORS = ["#000000", "#D4AF37", "#C0392B", "#2980B9", "#27AE60", "#8E44AD", "#E67E22", "#ECF0F1"]

history = []
stats = {"Nero": 0, "Oro": 0, "Pareggio": 0, "Totali": 0}

hud_brightness = 0
hud_direction = 1
win_anim_step = 0
win_anim_direction = 1

# ---------------- UTILITY ----------------
def copy_board(b):
    return [row[:] for row in b]

def switch_screen(show):
    for f in (menu_frame, mode_frame, pvp_frame, game_frame, history_frame, stats_frame):
        f.pack_forget()
    if show == menu_frame:
        show.pack(fill="both", expand=True)
    else:
        show.pack(expand=True)

def save_history(result):
    stats["Totali"] += 1
    # Gestione nomi per statistiche
    stat_key = "Nero" if "Nero" in result else "Oro" if "Oro" in result else result
    if stat_key in stats:
        stats[stat_key] += 1
    
    history.insert(0, {
        "winner": result,
        "board": copy_board(board),
        "winning": winning_cells[:]
    })
    del history[10:] # Teniamo le ultime 10

def hover(btn, enter=True):
    btn.config(bg=BTN_HOVER if enter else BTN_BG)

# ---------------- LOGICA DI GIOCO ----------------
def start_new_game():
    global board, current_player, game_over, winner, winning_cells, game_started, ROWS, COLS
    if game_mode == "PVP":
        setup_pvp_board(len(players))
        current_player = players[0]
    else:
        ROWS, COLS = 6, 7
        board = [[None]*COLS for _ in range(ROWS)]
        current_player = BLACK_PIECE

    game_over = False
    winner = None
    winning_cells = []
    game_started = True
    draw_board()
    update_status()
    switch_screen(game_frame)

def setup_pvp_board(n):
    global ROWS, COLS, board
    extra = max(0, (n - 2)//2)
    ROWS = 6 + extra
    COLS = 7 + extra
    board = [[None]*COLS for _ in range(ROWS)]
    canvas.config(width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)

def update_status():
    if game_over:
        status_label.config(text=f"Vince {winner}", fg=GOLD)
    else:
        if game_mode == "PVP":
            status_label.config(text=f"Turno Giocatore {current_player_index + 1}", fg=current_player)
        else:
            status_label.config(text=f"Turno {'Nero' if current_player == BLACK_PIECE else 'Oro'}", 
                               fg=BLACK_PIECE if current_player == BLACK_PIECE else GOLD_PIECE)

def draw_board(custom=None, highlight=None):
    canvas.delete("all")
    b = custom if custom else board
    h = highlight if highlight else []
    for r in range(ROWS):
        for c in range(COLS):
            x1, y1 = c*CELL_SIZE, r*CELL_SIZE
            x2, y2 = x1+CELL_SIZE, y1+CELL_SIZE
            canvas.create_rectangle(x1, y1, x2, y2, fill="#1E1E1E", outline=GOLD, width=2)
            if b[r][c]:
                win = (r, c) in h
                canvas.create_oval(x1+10, y1+10, x2-10, y2-10, fill=b[r][c], 
                                 outline=WHITE if win else "", width=5 if win else 0)

def animate_drop(col, row):
    global is_animating
    is_animating = True
    x = col*CELL_SIZE + CELL_SIZE//2
    y = -40
    target_y = row*CELL_SIZE + CELL_SIZE//2
    piece = canvas.create_oval(x-30, y-30, x+30, y+30, fill=current_player, outline="")
    
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
    global current_player, game_over, winner, is_animating, current_player_index
    board[row][col] = current_player
    is_animating = False
    if check_win(row, col):
        game_over = True
        winner = f"Giocatore {current_player_index+1}" if game_mode=="PVP" else ("Nero" if current_player==BLACK_PIECE else "Oro")
        draw_board(highlight=winning_cells)
        save_history(winner)
        update_status()
        return
    draw_board()
    if all(board[0][c] for c in range(COLS)):
        game_over = True
        winner = "Pareggio"
        save_history("Pareggio")
        update_status()
        return
    
    if game_mode=="PVP":
        current_player_index = (current_player_index+1)%len(players)
        current_player = players[current_player_index]
    else:
        current_player = GOLD_PIECE if current_player==BLACK_PIECE else BLACK_PIECE
    update_status()

def check_win(row, col):
    global winning_cells
    for dx, dy in [(1,0),(0,1),(1,1),(1,-1)]:
        cells = [(row, col)]
        for direction in [1, -1]:
            step = 1
            while True:
                r, c = row + dy*step*direction, col + dx*step*direction
                if 0<=r<ROWS and 0<=c<COLS and board[r][c] == current_player:
                    cells.append((r,c))
                    step += 1
                else: break
        if len(cells) >= 4:
            winning_cells = cells[:4]
            return True
    return False

def click(e):
    if game_over or is_animating: return
    col = e.x // CELL_SIZE
    if col < COLS:
        for r in range(ROWS-1, -1, -1):
            if board[r][col] is None:
                animate_drop(col, r)
                return

# ---------------- SCHERMATE SPECIALI ----------------
def show_history():
    for w in history_list.winfo_children(): w.destroy()
    if not history:
        tk.Label(history_list, text="Nessuna partita", fg=TEXT_WHITE, bg=BG_COLOR).pack(pady=20)
    else:
        for i, h in enumerate(history):
            btn = tk.Button(history_list, text=f"{i+1}) Vincitore: {h['winner']}", 
                           bg=BTN_BG, fg=GOLD, font=("Helvetica", 12),
                           command=lambda x=h: preview_history(x))
            btn.pack(fill="x", pady=4, padx=20)
    switch_screen(history_frame)

def preview_history(h):
    global board, winning_cells, game_over, winner, ROWS, COLS
    board = copy_board(h["board"])
    ROWS, COLS = len(board), len(board[0])
    winning_cells = h["winning"]
    game_over = True
    winner = h["winner"]
    canvas.config(width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
    draw_board(highlight=winning_cells)
    update_status()
    switch_screen(game_frame)

def show_stats():
    for w in stats_frame.winfo_children(): w.destroy()
    tk.Label(stats_frame, text="STATISTICHE", font=("Impact", 42), fg=GOLD, bg=BG_COLOR).pack(pady=30)
    for k, v in stats.items():
        tk.Label(stats_frame, text=f"{k}: {v}", fg=TEXT_WHITE, bg=BG_COLOR, font=("Helvetica", 18)).pack(pady=5)
    tk.Button(stats_frame, text="INDIETRO", font=BTN_FONT, bg=BTN_BG, fg=GOLD, command=lambda: switch_screen(menu_frame)).pack(pady=30)
    switch_screen(stats_frame)

# ---------------- DEFINIZIONE FRAME ----------------
menu_frame = tk.Frame(root, bg=BG_COLOR)
mode_frame = tk.Frame(root, bg=BG_COLOR)
pvp_frame = tk.Frame(root, bg=BG_COLOR)
game_frame = tk.Frame(root, bg=BG_COLOR)
history_frame = tk.Frame(root, bg=BG_COLOR)
stats_frame = tk.Frame(root, bg=BG_COLOR)

# ---------------- MENU CON SFONDO ----------------
menu_canvas = tk.Canvas(menu_frame, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
menu_canvas.pack(fill="both", expand=True)

if bg_photo:
    menu_canvas.create_image(0, 0, image=bg_photo, anchor="nw")

#menu_canvas.create_text(WINDOW_WIDTH//2, 120, text="4 IN LINE", font=TITLE_FONT, fill=GOLD)
#menu_canvas.create_text(WINDOW_WIDTH//2, 190, text="THE GOLD EDITION", font=("Helvetica", 18, "bold"), fill=TEXT_WHITE)

def add_menu_button(text, cmd, y):
    b = tk.Button(root, text=text, font=BTN_FONT, bg=BTN_BG, fg=GOLD, width=22, relief="flat", command=cmd)
    b.bind("<Enter>", lambda e: hover(b, True))
    b.bind("<Leave>", lambda e: hover(b, False))
    menu_canvas.create_window(WINDOW_WIDTH//2, y, window=b)

add_menu_button("NUOVA PARTITA", lambda: switch_screen(mode_frame), 320)
add_menu_button("CRONOLOGIA", show_history, 400)
add_menu_button("STATISTICHE", show_stats, 480)
#menu_canvas.create_text(WINDOW_WIDTH//2, 650, text="© D&G SoftwareHouse", fill="#AAA", font=SUB_FONT)

# ---------------- SELEZIONE MODALITÀ ----------------
tk.Label(mode_frame, text="MODALITÀ", font=("Impact", 42), fg=GOLD, bg=BG_COLOR).pack(pady=40)
def mode_btn(txt, sub, m):
    f = tk.Frame(mode_frame, bg=BTN_BG, padx=10, pady=5)
    f.pack(pady=10)
    b = tk.Button(f, text=txt, font=BTN_FONT, bg=BTN_BG, fg=GOLD, width=25, relief="flat", 
                 command=lambda: [setattr(root, 'gm', m), select_mode(m)])
    b.pack()
    tk.Label(f, text=sub, fg=TEXT_WHITE, bg=BTN_BG, font=("Helvetica", 10)).pack()

def select_mode(m):
    global game_mode
    game_mode = m
    if m == "PVP": switch_screen(pvp_frame)
    else: start_new_game()

mode_btn("NORMALE", "2 Giocatori - Griglia Classica", "NORMAL")
mode_btn("PVP MULTI", "Fino a 8 Giocatori - Griglia Dinamica", "PVP")
tk.Button(mode_frame, text="INDIETRO", font=BTN_FONT, bg=BTN_BG, fg=GOLD, command=lambda: switch_screen(menu_frame)).pack(pady=20)

# ---------------- SELEZIONE GIOCATORI PVP ----------------
tk.Label(pvp_frame, text="QUANTI GIOCATORI?", font=("Impact", 36), fg=GOLD, bg=BG_COLOR).pack(pady=30)
def set_pvp(n):
    global players, current_player_index
    players = PLAYER_COLORS[:n]
    current_player_index = 0
    start_new_game()

for i in range(2, 9):
    tk.Button(pvp_frame, text=f"{i} GIOCATORI", font=BTN_FONT, bg=BTN_BG, fg=GOLD, width=20, 
             command=lambda x=i: set_pvp(x)).pack(pady=5)

# ---------------- GAME UI ----------------
game_top = tk.Frame(game_frame, bg=BG_COLOR)
game_top.pack(fill="x", pady=10)
status_label = tk.Label(game_top, text="", font=("Helvetica", 20, "bold"), bg=BG_COLOR)
status_label.pack(side="left", padx=50)
tk.Button(game_top, text="MENU", bg=BTN_BG, fg=GOLD, font=BTN_FONT, command=lambda: switch_screen(menu_frame)).pack(side="right", padx=50)

canvas = tk.Canvas(game_frame, bg=BG_COLOR, highlightthickness=0)
canvas.pack(pady=20)
canvas.bind("<Button-1>", click)

# ---------------- CRONOLOGIA UI ----------------
tk.Label(history_frame, text="CRONOLOGIA", font=("Impact", 42), fg=GOLD, bg=BG_COLOR).pack(pady=20)
history_list = tk.Frame(history_frame, bg=BG_COLOR)
history_list.pack(fill="both", expand=True)
tk.Button(history_frame, text="INDIETRO", font=BTN_FONT, bg=BTN_BG, fg=GOLD, command=lambda: switch_screen(menu_frame)).pack(pady=20)

# ---------------- AVVIO ----------------
switch_screen(menu_frame)
root.mainloop()