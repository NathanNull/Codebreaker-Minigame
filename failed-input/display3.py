import unicurses as cs
from multiprocessing import Process
import ctypes as ct
from collections.abc import Callable

class Box:
    def __init__(self, window: ct.c_void_p):
        self.window = window
        self.pos = (0,0)
        self.clear()
    
    def print(self, text: str):
        w = cs.getmaxyx(self.window)[1]
        yx = cs.getyx(self.window)
        for char in text:
            if char == "\n":
                self.pos = (self.pos[0]+1, 0)
            else:
                p = [sum(t) for t in zip(yx, self.pos)]
                cs.mvwaddch(self.window, *p, char)
                self.pos = (
                    self.pos[0]+(1 if self.pos==w-2 else 0),
                    (self.pos[1]+1) % w
                )
        cs.wrefresh(self.window)

    def clear(self):
        self.pos = (0,0)
        cs.wclear(self.window)
        cs.wrefresh(self.window)

stdscr = cs.initscr()
cs.cbreak()
cs.noecho()
cs.curs_set(0)
cs.keypad(stdscr, True)

h, w = cs.getmaxyx(stdscr)
out_box = Box(cs.newwin(h-5, w, 0, 0))
ipt_box = Box(cs.newwin(5, w, h-4, 0))

ipt_box.print('wheeee')
out_box.print('ready')

def __ipt(callback: Callable[[str], None]):
    line = ""
    ch = " "
    while True:
        out_box.print('waiting')
        ch = chr(cs.getch())
        if ch == '\b':
            line = line[:-1]
            ipt_box.clear()
            ipt_box.print(line)
        elif ch == '\n':
            ipt_box.clear()
            return callback(line)
        else:
            line = line+ch
            ipt_box.print(ch)
        out_box.print("ae")

def get_input(callback: Callable[[str], None]):
    p = Process(target=__ipt, args=(callback,))
    p.run()
    return p.terminate

try:
    do_ipt = True
    while True:
        if do_ipt:
            do_ipt = False
            def l(i):
                global do_ipt
                do_ipt = True
                out_box.print(i)
            get_input(l)
        cs.napms(200)
finally:
    cs.endwin()