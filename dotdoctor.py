#!/usr/bin/env python3

from environ_helper import (env_exists, get_env)
from curses_helper import (init_color_pairs, draw_error_page)

import curses
from curses import wrapper

def get_dotdoctor_dir_path():
    if env_exists("dotdoctor_dir"):
        global dotdoctor_dir
        dotdoctor_dir = get_env("dotdoctor_dir")
    else:
        wrapper(draw_env_missing_error)
def draw_env_missing_error(stdscr):
    init_color_pairs()
    header = "ERROR"
    message = "Environemntal variable $dotdoctor_dir is not set."
    draw_error_page(stdscr, header, message)
    stdscr.getkey()

get_dotdoctor_dir_path()
