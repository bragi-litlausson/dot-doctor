#!/usr/bin/env python3

import os
from environ_helper import (env_exists, get_env)
from curses_helper import (init_color_pairs, draw_error_page)
from dotdata import DotData

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

def validate_dotdoctor_dir():
    if os.path.exists(dotdoctor_dir) == False:
        wrapper(draw_dir_missing_error)
    if len(os.listdir(dotdoctor_dir)) == 0:
        wrapper(draw_dir_empty_error)
def draw_dir_missing_error(stdscr):
    init_color_pairs()
    header = "ERROR"
    message = "{} does not exist.".format(dotdoctor_dir)
    draw_error_page(stdscr, header, message)
    stdscr.getkey()
def draw_dir_empty_error(stdscr):
    init_color_pairs()
    header = "ERROR"
    message = "{} is empty.".format(dotdoctor_dir)
    draw_error_page(stdscr, header, message)
    stdscr.getkey()

def create_config_list():
    global config_list
    config_list = []
    files_list = os.listdir(dotdoctor_dir)
    for file in files_list:
        if file != ".config":
            config_list.append(DotData(file, file, False))
    if '.config' in os.listdir(dotdoctor_dir):
        path = os.path.join(dotdoctor_dir, ".config")
        files_list = os.listdir(path)
        for file in files_list:
            config_list.append(DotData(file, os.path.join(".config", file), False))

def update_dot_data_status():
    home_path = get_env("HOME")
    for dot_data in config_list:
        dot_path = os.path.join(home_path, dot_data.relative_path)
        if os.path.exists(dot_path) and os.path.islink(dot_path):
            dot_data.set_status(True)

if __name__ == "__main__":
    get_dotdoctor_dir_path()
    validate_dotdoctor_dir()
    create_config_list()
    update_dot_data_status()
