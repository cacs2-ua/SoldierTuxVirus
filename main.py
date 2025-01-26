import tkinter as tk
from tkinter import PhotoImage, Canvas
import ctypes
import pyautogui
import random

class Tux:
    def __init__(self, escenario, start_x=0, start_y=0):
        self.escenario = escenario
        tux_temp = PhotoImage(file='tux.png')
        self.tux_img = tux_temp.subsample(16)
        explosion_temp = PhotoImage(file='explosion.png')
        self.explosion_img = explosion_temp.subsample(8)
        self.ref_img = self.escenario.canvas.create_image(start_x, start_y, image=self.tux_img)
        self.has_explosion = False

    def update(self):
        m_x, m_y = pyautogui.position()
        current_pos = self.escenario.canvas.coords(self.ref_img)
        pos_x, pos_y = current_pos[0], current_pos[1]
        distance_ = abs(m_x - pos_x) + abs(m_y - pos_y)
        if self.has_explosion:
            self.escenario.canvas.move(
                self.ref_img,
                random.choice([-30, 30]),
                random.choice([-30, 30])
            )
            self.escenario.canvas.itemconfig(self.ref_img, image=self.tux_img)
            for _ in range(10):
                self.escenario.new_tux(
                    random.randint(0, self.escenario.screen_width),
                    random.randint(0, self.escenario.screen_height)
                )
            self.has_explosion = False
        elif distance_ < 5:
            self.escenario.canvas.itemconfig(self.ref_img, image=self.explosion_img)
            self.has_explosion = True
        else:
            step = random.choice([1, 2, 5])
            move_x = step if m_x > pos_x else -step
            move_y = step if m_y > pos_y else -step
            self.escenario.canvas.move(self.ref_img, move_x, move_y)

class Scene:
    def __init__(self, main_window):
        self.screen_width = main_window.winfo_screenwidth()
        self.screen_height = main_window.winfo_screenheight()
        self.canvas = Canvas(
            main_window,
            width=self.screen_width,
            height=self.screen_height,
            highlightthickness=0,
            bg='white'
        )
        self.canvas.pack()
        self.characters = []

    def update(self):
        for c in self.characters:
            c.update()

    def new_tux(self, x, y):
        p = Tux(self)
        self.canvas.move(p.ref_img, x, y)
        self.characters.append(p)

class Game:
    def __init__(self):
        self.window = self.build_window()
        self.apply_transparency(self.window)
        self.scene = Scene(self.window)

    def update(self):
        self.scene.update()
        self.window.after(5, self.update)

    def build_window(self):
        w = tk.Tk()
        w.wm_attributes("-topmost", True)
        w.attributes("-fullscreen", True)
        w.overrideredirect(True)
        w.attributes('-transparentcolor', 'white')
        w.config(bg='white')
        return w

    def apply_transparency(self, target):
        WS_EX_TRANSPARENT = 0x00000020
        WS_EX_LAYERED = 0x00080000
        GWL_EXSTYLE = -20
        handle = ctypes.windll.user32.GetParent(target.winfo_id())
        style_current = ctypes.windll.user32.GetWindowLongW(handle, GWL_EXSTYLE)
        style_new = style_current | WS_EX_TRANSPARENT | WS_EX_LAYERED
        ctypes.windll.user32.SetWindowLongW(handle, GWL_EXSTYLE, style_new)

    def launch(self):
        self.update()
        self.window.mainloop()

game = Game()
game.scene.new_tux(100, 100)
game.launch()
