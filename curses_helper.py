import curses

def init_color_pairs():
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

def draw_error_page(stdscr, header, message):
    stdscr.clear()
    stdscr.addstr(3, 3, header, curses.color_pair(2))
    stdscr.addstr(4, 3, message, curses.color_pair(3))

def draw_config_row(stdscr, dot_data, index):
    if dot_data.status:
        stdscr.addstr(1+index, 2, dot_data.name, curses.color_pair(1))
    else:
        stdscr.addstr(1+index, 2, dot_data.name, curses.color_pair(2))
