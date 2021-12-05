import os
#os.environ["KIVY_NO_CONSOLELOG"] = "1" # prevents kivy debug messages from appearing

from converter import *
from board import *
from engine import *
from constants import *


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.core.text import Label
from kivy.clock import Clock
from kivy.graphics import (Rectangle, Line, Color)

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', False)

board_frame = 0
loaded = False
coloring = False

color_dict = {
    "red": (1, 0, 0, 1),
    "green": (0, 1, 0, 1),
    "blue": (0, 0, 1, 0)
}


class MainWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.init, .2)
    def init(self, _):
        sudoku_board = Drawable()
        sudoku_board.size_hint = (1.74, 1)
        sudoku_nav = SudokuNav()
        
        self.ids.sudoku.add_widget(sudoku_board)
        self.ids.sudoku.add_widget(sudoku_nav)

    def load_sudoku(self, string):
        global loaded, board_frame, coloring
        loaded = True
        board_frame = 0
        coloring = False
        board = Board(string, 0)
        engine = Engine(board, 0)
        self.states = engine.states
        App.get_running_app().root.ids.sudoku.children[1].draw_frame(False)


class Drawable(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.init, .2)


    def draw_frame(self, default):
        if not default:
            states = App.get_running_app().root.states
        
        FORCED_SIZE = 761
        unit = FORCED_SIZE / 9 #single cell width
        small_unit = unit / 3 #candidate width
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(size=(FORCED_SIZE, FORCED_SIZE), pos=self.pos)
            Color(0.4, 0.4, 0.4, 1)
            for x in range(1, 9):
                Line(points=(unit * x, 0, unit * x, unit * 9 ), width = 1.5)
                Line(points=(0, unit * x, unit * 9, unit * x), width = 1.5)
            Color(0, 0, 0, 1)
            for x in range(1, 3):
                Line(points=(unit * x * 3, 0, unit * x * 3, unit * 9 ), width = 1.8)
                Line(points=(0, unit * x * 3, unit * 9, unit * x * 3), width = 1.8)
            
            if default:
                board = [[[x for x in range(1, 10)] for y in range(1, 10)] for z in range(1, 10)]
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    if default:
                        cell = board[row][col]
                    elif board_frame != 0:
                        cell = states[board_frame][1][row][col]
                    else:
                        cell = states[board_frame][row][col]
                    if len(cell) == 1:
                        num = Label(text=str(cell[0]), font_size=75, color=(0, 0, 0, 1))
                        num.refresh()
                        pos = (col * unit, (8 - row) * unit)
                        offset_center = (20, -5)
                        prop_pos = tuple(map(lambda i, j: i + j, pos, offset_center))
                        Rectangle(texture=num.texture, size=num.texture.size, pos=prop_pos)
                    else:
                        for cand in cell:
                            num = Label(text=str(cand), font_size=25)
                            num.refresh()
                            pos = (col * unit, (8 - row) * unit)
                            offset_center = (35, 28)
                            offset_num = self.get_offset(cand, small_unit)
                            prop_pos = tuple(map(lambda i, j, k: i + j + k, pos, offset_center, offset_num))
                            Color(0, 0, 0, 1)
                            Rectangle(texture=num.texture, size=num.texture.size, pos=prop_pos)

    def draw_color(self):
        global color_dict
        FORCED_SIZE = 761
        unit = FORCED_SIZE / 9 #single cell width
        small_unit = unit / 3 #candidate width
        with self.canvas:
            states = App.get_running_app().root.states
            if len(states[board_frame + 1]) == 3 and isinstance(states[board_frame + 1][2], list):
                positions = states[board_frame + 1][2]
                for pos in positions:
                    cell = pos[0]
                    color = pos[1]
                    numbers = pos[2]
                    color_big = False
                    if len(pos) > 3 and pos[3] == 'big_number':
                        color_big = True
                    if color_big:
                        Color(*color_dict[color])
                        num = Label(text=str(numbers[0]), font_size=75, bold=True)
                        num.refresh()
                        temp_pos = (cell[1] * unit, (8 - cell[0]) * unit)
                        offset_center = (20, -5)
                        prop_pos = tuple(map(lambda i, j: i + j, temp_pos, offset_center))
                        Rectangle(texture=num.texture, size=num.texture.size, pos=prop_pos)
                    else:
                        for number in numbers:
                            Color(*color_dict[color])
                            num = Label(text=str(number), font_size=25, bold=True)
                            num.refresh()
                            temp_pos = (cell[1] * unit, (8 - cell[0]) * unit)
                            offset_center = (35, 28)
                            offset_num = self.get_offset(number, small_unit)
                            prop_pos = tuple(map(lambda i, j, k: i + j + k, temp_pos, offset_center, offset_num))
                            Rectangle(texture=num.texture, size=num.texture.size, pos=prop_pos)

    def get_offset(self, number, small_unit):
        if number == 1:
            return (-small_unit, small_unit)
        elif number == 2:
            return (0, small_unit)
        elif number == 3:
            return (small_unit, small_unit)
        elif number == 4:
            return (-small_unit, 0)
        elif number == 5:
            return (0, 0)
        elif number == 6:
            return (small_unit, 0)
        elif number == 7:
            return (-small_unit, -small_unit)
        elif number == 8:
            return (0, -small_unit)
        elif number == 9:
            return (small_unit, -small_unit)

    def init(self, _):
        self.draw_frame(True)


class SudokuNav(Widget):
    def next(self):
        global board_frame, loaded, coloring
        if loaded and board_frame < len(App.get_running_app().root.states) - 1:
            if not coloring:
                coloring = not coloring
                board_frame += 1
                self.ids.technique_info.text = App.get_running_app().root.states[board_frame][0] + " removed"
                App.get_running_app().root.ids.sudoku.children[1].draw_frame(False)
            elif board_frame > 0:
                coloring = not coloring
                self.ids.technique_info.text = App.get_running_app().root.states[board_frame + 1][0] + " coloring"
                App.get_running_app().root.ids.sudoku.children[1].draw_color()
    def prev(self):
        global board_frame, loaded
        if loaded:
            board_frame -= 1
            if board_frame < 0:
                board_frame = 0
            if board_frame == 0:
                self.ids.technique_info.text = 'Technique used to eliminate candidates will be displayed here'
            elif board_frame > 0:
                self.ids.technique_info.text = App.get_running_app().root.states[board_frame][0]
            App.get_running_app().root.ids.sudoku.children[1].draw_frame(False)


class MyPopup(Popup):
    def test(self, sudoku_string):
        App.get_running_app().root.load_sudoku(sudoku_string)


class SudokuSolverApp(App):
    def build(self):
        return MainWidget()


SudokuSolverApp().run()