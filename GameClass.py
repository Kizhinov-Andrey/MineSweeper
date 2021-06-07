import tkinter as tk
import random as r


def start():
    global game
    game = Mine()
    Mine.COUNT_MINE = 100
    game.create_widgets()
    Mine.window.mainloop()


class Cell(tk.Button):
    def __init__(self, x, y, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.frame = master
        self.x = x
        self.y = y
        self.mine = False
        self.mine_around = None
        self.open = False
        self.flag = False

    def open_cell(self, event):
        if game.is_first_click():
            game.create_mine(self.x, self.y)
            game.set_not_first_click()

        if self.flag:
            pass
        elif self.have_mine():
            if not game.game_over:
                game.end_game()
            else:
                self.config(text="💣")
                self["state"] = tk.DISABLED
        else:
            self.frame.config(relief=tk.FLAT)
            self.config(text=self.mine_around)
            if self.mine_around == 0:
                self.config(text="")
            self.open = True
            self["state"] = tk.DISABLED
            if self.mine_around == 0:
                for x_diff in range(-1, 2):
                    for y_diff in range(-1, 2):
                        if not (x_diff == y_diff == 0 or self.x + x_diff < 0 or self.y + y_diff < 0
                                or self.x + x_diff >= Mine.ROW or self.y + y_diff >= Mine.COL
                                or game.get_cell(self.x + x_diff, self.y + y_diff).open):
                            game.get_cell(self.x + x_diff, self.y + y_diff).open_cell(None)

    def set_flag(self, event):
        if self.flag:
            self.config(text="")
            self.flag = False
            Mine.COUNT_MINE += 1
            Mine.count_mine_lbl.config(text=Mine.COUNT_MINE)
        else:
            self.config(text="🚩")
            self.flag = True
            Mine.COUNT_MINE -= 1
            Mine.count_mine_lbl.config(text=Mine.COUNT_MINE)

    def set_mine(self):
        self.mine = True

    def set_mine_around(self, n):
        self.mine_around = n

    def have_mine(self):
        return self.mine

    def __str__(self):
        if self.have_mine():
            return "B"
        return str(self.mine_around)


class Mine:
    # Creating main window.
    window = tk.Tk()
    window.title("MineSweeper")
    window.resizable(width=False, height=False)

    # Constants.
    ROW = 16
    COL = 30
    COUNT_MINE = 100
    # Frames
    toolbar = tk.Frame(
        width=925,
        heigh=75,
        master=window,
        relief=tk.SUNKEN,
        borderwidth=5)

    desk = tk.Frame(
        width=925,
        heigh=490,
        master=window,
        relief=tk.SUNKEN,
        borderwidth=5)

    restart_frame = tk.Frame(
        master=toolbar,
        relief=tk.RAISED,
        borderwidth=2)
    restart_btn = tk.Button(
        restart_frame,
        width=5,
        height=2,
        text="Restart",
        command=start)

    count_mine_frame = tk.Frame(
        master=toolbar,
        relief=tk.SUNKEN,
        borderwidth=2)
    count_mine_lbl = tk.Label(
        count_mine_frame,
        width=3,
        font='a_LCDNova 30',
        bg="black",
        fg="red")

    def __init__(self):
        # init buttons
        self.buttons = []
        for i in range(Mine.ROW):
            part = []
            for j in range(Mine.COL):
                btn_frame = tk.Frame(
                    master=Mine.desk,
                    relief=tk.RAISED,
                    borderwidth=3)
                btn_frame.grid(row=i, column=j)
                btn = Cell(i, j, btn_frame, width=2, font='Times_new_roman 10',)
                btn.bind("<Button-1>", btn.open_cell)
                btn.bind("<Button-3>", btn.set_flag)
                part.append(btn)
            self.buttons.append(part)
        self.first_click = True
        self.game_over = False

    def create_widgets(self):
        Mine.toolbar.pack(padx=10, pady=10)
        Mine.desk.pack(padx=10, pady=10)
        Mine.restart_frame.grid(row=0, column=1, padx=390, pady=20)
        Mine.restart_btn.pack()
        Mine.count_mine_frame.grid(row=0, column=0, padx=10)
        Mine.count_mine_lbl.config(text=Mine.COUNT_MINE)
        Mine.count_mine_lbl.pack()

        for i in range(Mine.ROW):
            for j in range(Mine.COL):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def is_first_click(self):
        return self.first_click

    def set_not_first_click(self):
        self.first_click = False

    def create_mine(self, x, y):
        mine_cords = set()
        count = 0
        while count < Mine.COUNT_MINE:
            c_x, c_y = r.randint(0, Mine.ROW - 1), r.randint(0, Mine.COL - 1)
            if not (((c_x, c_y) in mine_cords) or (c_x == x and c_y == y)):
                count += 1
                mine_cords.add((c_x, c_y))
                self.get_cell(c_x, c_y).set_mine()
        self.count_mine_around()

    def count_mine_around(self):
        for i in range(self.ROW):
            for j in range(self.COL):
                btn = self.get_cell(i, j)
                if not btn.have_mine():
                    count = 0
                    for i_diff in range(-1, 2):
                        for j_diff in range(-1, 2):
                            if not (i_diff == j_diff == 0 or i + i_diff < 0 or j + j_diff < 0
                                    or i + i_diff >= Mine.ROW or j + j_diff >= Mine.COL):
                                check_btn = self.get_cell(i + i_diff, j + j_diff)
                                if check_btn.have_mine():
                                    count += 1
                    btn.set_mine_around(count)

    def print_field(self):
        for i in range(Mine.ROW):
            for j in range(Mine.COL):
                print(self.get_cell(i, j), end='\t')
            print()

    def get_cell(self, x, y):
        return self.buttons[x][y]

    def end_game(self):
        self.game_over = True
        Mine.count_mine_lbl.config(text="END")
        for i in range(Mine.ROW):
            for j in range(Mine.COL):
                self.get_cell(i, j).open_cell(None)
