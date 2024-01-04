import curses
import os
import getpass
import hashlib
import subprocess
import json

from edxfunctions import *
from variables import *

def load_menu_config(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    with open(file_path, 'r') as config_file:
        menu_config = json.load(config_file)
    return menu_config

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    sh, sw = stdscr.getmaxyx()

    title = "Main Menu - Press ENTER\n"
    stdscr.addstr(0, sw // 2 - len(title) // 2, title)

    ''' username, password = get_user_input(stdscr)

    if not check_credentials(username, password):
        stdscr.addstr(6, 0, "Nom d'utilisateur ou mot de passe incorrect.")
        stdscr.refresh()
        stdscr.getch()
        return
    '''

    menu_config = load_menu_config(MENU_CONFIG_FILE_PATH)
    show_menu(stdscr, menu_config)

if __name__ == '__main__':
    curses.wrapper(main)
