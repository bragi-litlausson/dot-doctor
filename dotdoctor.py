#!/usr/bin/env python3
import curses
from curses import wrapper

import os
from os import environ, path

import sys
import shutil

def env_exists(name):
    return name in environ
def get_env(name):
    return environ.get(name)

def init_color_pairs():
    # GREEN on BLACK
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # RED on BLACK
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    # MAGENTA on BLACK
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    # GREEN on WHITE
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_WHITE)
    # RED on WHITE
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_WHITE)

def draw_error_message(stdscr, header, message):
    stdscr.clear()
    stdscr.addstr(3, 3, header, curses.color_pair(2))
    stdscr.addstr(4, 3, message, curses.color_pair(3))
    stdscr.getch()
    exit()

def draw_config_row(stdscr, dot_data, y, is_active):
    color_pair_modifier = 0
    if is_active:
        color_pair_modifier = 5

    if dot_data.status:
        stdscr.addstr(y, 2, dot_data.name, curses.color_pair(1+color_pair_modifier))
    else:
        stdscr.addstr(y, 2, dot_data.name, curses.color_pair(2+color_pair_modifier))

class DotData:
    def __init__(self, name, relative_path, is_directory):
        self.name = name
        self.relative_path = relative_path
        self.status = False
        self.is_directory = is_directory
    def set_status(self, status):
        self.status = status

def validate_env_var():
    verify_dotdoctor_dir_env()
    validate_dotdoctor_dir()

dotdoctor_dir = ""
def verify_dotdoctor_dir_env():
    global dotdoctor_dir
    if env_exists("dotdoctor_dir"):
        dotdoctor_dir = get_env("dotdoctor_dir")
    else:
        wrapper(draw_env_missing_error)

def draw_env_missing_error(stdscr):
    init_color_pairs()
    header = "ERROR"
    message = "Environemntal variable $dotdoctor_dir is not set. Variable should contain absolute path to your config repository."
    draw_error_message(stdscr, header, message)
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
    draw_error_message(stdscr, header, message)
    stdscr.getkey()

def draw_dir_empty_error(stdscr):
    init_color_pairs()
    header = "ERROR"
    message = "{} is empty.".format(dotdoctor_dir)
    draw_error_message(stdscr, header, message)
    stdscr.getkey()

home_path = get_env("HOME")
root_path = ""
def validate_directory_structure():
    validate_root_directory()
    validate_backup_directory()

def validate_root_directory():
    global root_path, home_path
    root_path = path.join(home_path, ".dotdoctor")
    if path.exists(root_path) == False:
        os.mkdir(root_path)

def validate_backup_directory():
    global root_path
    backup_path = os.path.join(root_path, ".backup")
    if os.path.exists(backup_path) == False:
        os.mkdir(backup_path)
        backup_path = os.path.join(backup_path, ".config")
        os.mkdir(backup_path)

ignore = []
def load_ignore_file():
    global ignore, root_path
    ignore_path = os.path.join(root_path, "ignore")
    if os.path.exists(ignore_path) == False:
        with open(ignore_path, "w+") as file:
            file.write(".config\n")
            file.write("README.org\n")
            file.write("README.md\n")
            file.write("LICENSE\n")
            file.write(".git\n")
    path = os.path.abspath("./ignore")
    with open(ignore_path) as file:
        ignore = file.readlines()
        ignore = [line.rstrip() for line in ignore]

config_list = []
def create_config_list():
    global config_list, ignore
    files_list = os.listdir(dotdoctor_dir)
    for file in files_list:
        if is_file_ignored(file):
            print("Ignored: {}".format(file))
        else:
            config_list.append(DotData(file, file, os.path.isdir(os.path.join(dotdoctor_dir, file))))
    if '.config' in files_list:
        path = os.path.join(dotdoctor_dir, ".config")
        files_list = os.listdir(path)
        for file in files_list:
            if is_file_ignored(file):
                print("Ignored: {}".format(file))
            else:
                config_list.append(DotData(file, os.path.join(".config", file), os.path.isdir(os.path.join(path, file))))
    config_list.sort(key=lambda x: x.name)
def is_file_ignored(file_name):
    global ignore
    return file_name in ignore

def update_dot_data_status():
    home_path = get_env("HOME")
    for dot_data in config_list:
        dot_path = os.path.join(home_path, dot_data.relative_path)
        if os.path.exists(dot_path) and os.path.islink(dot_path):
            dot_data.set_status(True)

def initialize():
    validate_env_var()
    validate_directory_structure()
    load_ignore_file()
    create_config_list()
    update_dot_data_status()

current_index = 0
def config_list_loop(stdscr):
    curses.curs_set(False)
    init_color_pairs()
    global current_index
    while True:
        stdscr.clear()
        draw_navigation_help(stdscr)
        draw_list_of_configs(stdscr, current_index)
        if process_input(stdscr.getch()):
            break

def draw_list_of_configs(stdscr, current_index):
    rows, cols = stdscr.getmaxyx()
    for index, dot_data in enumerate(config_list):
        if len(config_list) <= rows-2:
            draw_config_row(stdscr, dot_data, index, current_index == index)
        elif current_index < 3 and index < rows-3:
            draw_config_row(stdscr, dot_data, index, current_index == index)
        elif current_index >= 3 and index > current_index -3 and index < rows -3 + current_index-2:
            draw_config_row(stdscr, dot_data, index-(current_index-2), current_index == index)

def draw_navigation_help(stdscr):
    rows, cols = stdscr.getmaxyx()
    stdscr.addstr(rows-1, 2, "[j] down | [k] up | [enter] enable/disable config")

def process_input(c):
    global current_index
    if c == ord('q'):
        return True
    if c == ord('k'):
        current_index -= 1
    if c == ord('j'):
        current_index += 1
    if c == 10:
        toggle_config()
    clamp_current_index()
    return False

def toggle_config():
    global config_list, current_index
    data = config_list[current_index]
    if data.status == False:
        activate_dot_data(data)
    else:
        deactivate_dot_data(data)

def activate_dot_data(dot_data):
    global dotdoctor_dir
    dot_data.set_status(True)
    home_path = os.path.join(get_env("HOME"), dot_data.relative_path)
    backup_path = os.path.join("./.backup", dot_data.relative_path)
    backup_path = os.path.abspath(backup_path)
    config_path = os.path.join(dotdoctor_dir, dot_data.relative_path)
    config_path = os.path.abspath(config_path)
    if os.path.exists(home_path):
        shutil.move(home_path, backup_path)
    os.symlink(config_path, home_path)

def deactivate_dot_data(dot_data):
    global dotdoctor_dir
    dot_data.set_status(False)
    home_path = os.path.join(get_env("HOME"), dot_data.relative_path)
    backup_path = os.path.join("./.backup", dot_data.relative_path)
    backup_path = os.path.abspath(backup_path)
    os.unlink(home_path)
    shutil.move(backup_path, home_path)

def clamp_current_index():
    global current_index
    if current_index < 0:
        current_index = 0
    if current_index >= len(config_list):
        current_index = len(config_list)-1

if __name__ == "__main__":
    initialize()
    wrapper(config_list_loop)
