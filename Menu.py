#pip install curses-menu
#pip install windows-curses --for Windows
import curses
import sys
import os

class CursesMenu(object):

    INIT = {'type' : 'init'}

    def __init__(self, menu_options):
        self.screen = curses.initscr()
        self.menu_options = menu_options
        self.selected_option = 0
        self._previously_selected_option = None
        self.running = True

        #init curses and curses input
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0) #Hide cursor
        self.screen.keypad(1)

        #set up color pair for highlighted option
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.hilite_color = curses.color_pair(1)
        self.normal_color = curses.A_NORMAL

    def prompt_selection(self, parent=None):
        if parent is None:
            lastoption = "Exit"
        else:
            lastoption = "Return to previous menu ({})".format(parent['title'])

        option_count = len(self.menu_options['options'])

        input_key = None

        ENTER_KEY = ord('\n')
        while input_key != ENTER_KEY:
            if self.selected_option != self._previously_selected_option:
                self._previously_selected_option = self.selected_option

            self.screen.border(0)
            self._draw_title()
            for option in range(option_count):
                if self.selected_option == option:
                    self._draw_option(option, self.hilite_color)
                else:
                    self._draw_option(option, self.normal_color)

            if self.selected_option == option_count:
                self.screen.addstr(5 + option_count, 4, "{:2} - {}".format(option_count+1,
                    lastoption), self.hilite_color)
            else:
                self.screen.addstr(5 + option_count, 4, "{:2} - {}".format(option_count+1,
                    lastoption), self.normal_color)

            max_y, max_x = self.screen.getmaxyx()
            if input_key is not None:
                self.screen.addstr(max_y-3, max_x - 5, "{:3}".format(self.selected_option))
            self.screen.refresh()

            # Teclas Adicionais
            input_key = self.screen.getch()
            down_keys = [curses.KEY_DOWN, ord('j')]
            up_keys = [curses.KEY_UP, ord('k')]
            exit_keys = [ord('q')]

            if input_key in down_keys:
                if self.selected_option < option_count:
                    self.selected_option += 1
                else:
                    self.selected_option = 0

            if input_key in up_keys:
                if self.selected_option > 0:
                    self.selected_option -= 1
                else:
                    self.selected_option = option_count

            if input_key in exit_keys:
                self.selected_option = option_count #auto select exit and return
                break

        return self.selected_option

    def _draw_option(self, option_number, style):
        self.screen.addstr(5 + option_number,
                           4,
                           "{:2} - {}".format(option_number+1, self.menu_options['options'][option_number]['title']),
                           style)

    def _draw_title(self):
        self.screen.addstr(2, 2, self.menu_options['title'], curses.A_STANDOUT)
        self.screen.addstr(4, 2, self.menu_options['subtitle'], curses.A_BOLD)

    def display(self):
        selected_option = self.prompt_selection()
        i, _ = self.screen.getmaxyx()
        curses.endwin()
        os.system('cls') #Linux 
        if selected_option < len(self.menu_options['options']):
            selected_opt = self.menu_options['options'][selected_option]
            return selected_opt
        else:
            self.running = False
            return {'title' : 'Exit', 'type' : 'exitmenu'}

menu = {'title' : 'Virtual Coach' ,
        'type' : 'menu',
        'subtitle' : 'Features'}

option_1 = {'title' : 'Restart Learning',
            'type' : 'command',
            'command' : 'python Delete.py'}

option_2 = {'title' : 'Inform training position',
            'type' : 'command',
            'command' : 'python GetInformation.py'}

option_3 = {'title' : 'Execute Learning',
            'type' : 'command',
            'command' : 'python LearningModel.py'}

option_4 = {'title' : 'Test Learning',
            'type' : 'command',
            'command' : 'python TestLearning.py'}  

option_5 = {'title' : 'Prediction of Calories Burned',
            'type' : 'command',
            'command' : 'python Prediction.py'}   

option_6 = {'title' : 'Heart Rate Monitor',
            'type' : 'command',
            'command' : 'python Monitor.py'}   
      
option_7 = {'title' : 'Information about Miband',
            'type' : 'command',
            'command' : 'python Personal.py'}                       

menu['options'] = [option_1,option_2,option_3,option_4,option_5, option_6]

m = CursesMenu(menu)
selected_action = m.display()

if selected_action['type'] != 'exitmenu':
    os.system(selected_action['command'])
