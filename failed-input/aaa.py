import unicurses as uc

def create_newwin(height, width, starty, startx):
    local_win = uc.newwin(height, width, starty, startx)
    uc.box(local_win, 0, 0)
    uc.wrefresh(local_win)
    return local_win

def destroy_win(local_win):
    uc.wborder(
        local_win, uc.CCHAR(' '),
        uc.CCHAR(' '), uc.CCHAR(' '),
        uc.CCHAR(' '), uc.CCHAR(' '),
        uc.CCHAR(' '), uc.CCHAR(' '),
        uc.CCHAR(' ')
    )
    uc.wrefresh(local_win)
    uc.delwin(local_win)

stdscr = uc.initscr()
uc.cbreak()
uc.noecho()
uc.curs_set(0)
uc.keypad(stdscr, True)

height = 3
width = 10
LINES, COLS = uc.getmaxyx(stdscr)
starty = int((LINES - height) / 2)
startx = int((COLS - width) / 2)
uc.addstr("Use cursor keys to move the window, press Q to exit")
uc.refresh()

my_win = create_newwin(height, width, starty, startx)

ch = 0
while (ch != uc.CCHAR('q')) and (ch != uc.CCHAR('Q')):
    ch = uc.getch()
    if ch == ord('a'):
        if startx - 1 >= 0:
            destroy_win(my_win)
            startx -= 1
            my_win = create_newwin(height, width, starty, startx)
    elif ch == ord('d'):
        if startx + width < COLS:
            destroy_win(my_win)
            startx += 1
            my_win = create_newwin(height, width, starty, startx)
    elif ch == ord('w'):
        if starty - 1 > 0:
            destroy_win(my_win)
            starty -= 1
            my_win = create_newwin(height, width, starty, startx)
    elif ch == ord('s'):
        if starty + height < LINES:
            destroy_win(my_win)
            starty += 1
            my_win = create_newwin(height, width, starty, startx)

uc.endwin()