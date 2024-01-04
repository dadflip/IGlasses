import curses
import os
import getpass
import hashlib
import subprocess

from variables import *

def dispatch_action(action_name, stdscr):
    actions = {
        'show_help': show_help,
        'usr_crack_function': usr_crack_function,
        'show_files': show_files,
        'list_and_execute_commands': list_and_execute_commands,
        'change_username': change_username,
        'change_password': change_password,
        'menu_config_edit': menu_config_edit,
        'maia_config': maia_config,
        'add_vocal_command':add_vocal_command,
        'exit': exit  # Assurez-vous que la fonction exit est définie ou modifiez-la en conséquence
        # Ajoutez d'autres fonctions ici
    }

    return actions.get(action_name, None)


def menu_config_edit(stdscr):
    program = ["python", "system/root/edx-explorer/edx-xpl-editor.py"]
    subprocess.run(program)


def maia_config(stdscr):
    print("not implemented yet")
    return

def add_vocal_command(stdscr):
    os.system(f'system/root/commands/add_vocal_command')


# Fonction pour changer le nom d'utilisateur
def change_username(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Changer le nom d'utilisateur")
    stdscr.addstr(2, 0, "Entrez le nouveau nom d'utilisateur: ")
    stdscr.refresh()
    new_username = stdscr.getstr(2, 31, 20).decode('utf-8')
    create_or_update_config(new_username, get_username_and_password()[1])
    stdscr.addstr(4, 0, "Nom d'utilisateur mis à jour avec succès.")
    stdscr.refresh()
    stdscr.getch()

# Fonction pour changer le mot de passe
def change_password(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Changer le mot de passe")
    stdscr.addstr(2, 0, "1. Entrez le nouveau mot de passe")
    stdscr.addstr(3, 0, "2. Crypter le mot de passe")
    stdscr.addstr(4, 0, "3. Retour")
    stdscr.refresh()
    
    while True:
        user_input = stdscr.getch()
        if user_input == ord('1'):
            get_and_save_credentials(stdscr)
            break
        elif user_input == ord('2'):
            encrypt_password_with_gnu(stdscr)
            break
        elif user_input == ord('3'):
            break


# Fonction pour créer ou mettre à jour la configuration avec le nom d'utilisateur et le mot de passe
def create_or_update_config(username, password):
    config_path = os.path.expanduser(CONFIG_FILE_PATH)
    config_dir = os.path.dirname(config_path)

    # Crée le répertoire parent s'il n'existe pas
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    with open(config_path, "w") as config_file:
        config_file.write(f"Username: {username}\nPassword: {password}")


# Fonction pour récupérer le nom d'utilisateur et le mot de passe à partir de la configuration
def get_username_and_password():
    if os.path.exists(config_path := os.path.expanduser(CONFIG_FILE_PATH)):
        with open(config_path, "r") as config_file:
            lines = config_file.readlines()
            for line in lines:
                if line.startswith("Username: "):
                    username = line.split(": ")[1].strip()
                elif line.startswith("Password: "):
                    password = line.split(": ")[1].strip()
        return username, password
    return None, None


# Fonction pour demander et enregistrer le nom d'utilisateur et le mot de passe
def get_and_save_credentials(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Saisir le nom d'utilisateur et le mot de passe")

    stdscr.addstr(2, 0, "Nom d'utilisateur: ")
    stdscr.refresh()
    username = stdscr.getstr(2, 18, 20).decode('utf-8')

    stdscr.addstr(4, 0, "Mot de passe: ")
    stdscr.refresh()
    curses.curs_set(1)  # Afficher le curseur pour la saisie du mot de passe
    password = stdscr.getstr(4, 15, 20).decode('utf-8')
    curses.curs_set(0)  # Masquer le curseur après la saisie du mot de passe

    create_or_update_config(username, password)
    stdscr.addstr(6, 0, "Nom d'utilisateur et mot de passe enregistrés.")
    stdscr.refresh()
    stdscr.getch()


# Fonction pour crypter le mot de passe à l'aide des outils GNU
def encrypt_password_with_gnu(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Crypter le mot de passe avec des outils GNU")
    stdscr.refresh()

    # Récupérer le mot de passe actuel
    username, password = get_username_and_password()

    # Utiliser openssl pour le cryptage
    try:
        encrypted_password = subprocess.check_output(["openssl", "passwd", "-1", password])
        encrypted_password = encrypted_password.decode('utf-8').strip()
        create_or_update_config(username, encrypted_password)
        stdscr.addstr(2, 0, "Mot de passe crypté avec succès.")
        stdscr.refresh()
    except subprocess.CalledProcessError:
        stdscr.addstr(2, 0, "Erreur lors du cryptage du mot de passe.")
        stdscr.refresh()

    stdscr.getch()


# Fonction pour afficher et gérer les menus de manière récursive
def show_menu(stdscr, menu, depth=0):
    current_option = 0
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, menu["title"])
        options = menu.get("options", [])
        for i, option in enumerate(options):
            if i == current_option:
                stdscr.addstr(i + 2, 0, f"> {option['label']}")
            else:
                stdscr.addstr(i + 2, 0, f"  {option['label']}")
        stdscr.refresh()
        user_input = stdscr.getch()

        if user_input == curses.KEY_UP and current_option > 0:
            current_option -= 1
        elif user_input == curses.KEY_DOWN and current_option < len(options) - 1:
            current_option += 1
        elif user_input == curses.KEY_RIGHT:
            if "submenu" in options[current_option]:
                # Renommer la variable action pour éviter la confusion avec le nom de la fonction
                submenu_action = options[current_option]["submenu"]
                show_menu(stdscr, submenu_action, depth + 1)
        elif user_input == 10:  # Touche Entrée
            selected_option = options[current_option]
            selected_action_name = selected_option.get("action")
            if selected_action_name:
                selected_action = dispatch_action(selected_action_name, stdscr)
                if selected_action:
                    selected_action(stdscr)
            elif "submenu" in selected_option:
                submenu_action = selected_option["submenu"]
                show_menu(stdscr, submenu_action, depth + 1)
            elif selected_option["label"] == "Back" and depth > 0:
                return
        elif user_input == 27:  # Touche Échap pour revenir en arrière
            if depth > 0:
                return

# Fonction pour créer ou mettre à jour la configuration avec le nom d'utilisateur et le mot de passe
def create_or_update_config(username, password):
    config_path = os.path.expanduser(CONFIG_FILE_PATH)
    config_dir = os.path.dirname(config_path)

    # Crée le répertoire parent s'il n'existe pas
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    with open(config_path, "w") as config_file:
        config_file.write(f"Username: {username}\nPassword: {password}")

# Fonction pour récupérer le nom d'utilisateur et le mot de passe à partir de la configuration
def get_username_and_password():
    config_path = os.path.expanduser(CONFIG_FILE_PATH)
    if os.path.exists(config_path):
        with open(config_path, "r") as config_file:
            lines = config_file.readlines()
            for line in lines:
                if line.startswith("Username: "):
                    username = line.split(": ")[1].strip()
                elif line.startswith("Password: "):
                    password = line.split(": ")[1].strip()
        return username, password
    return None, None

# Fonction pour demander le nom d'utilisateur et le mot de passe à l'utilisateur
def get_user_input(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Saisir le nom d'utilisateur et le mot de passe")
    
    stdscr.addstr(2, 0, "Nom d'utilisateur: ")
    stdscr.refresh()
    username = stdscr.getstr(2, 18, 20).decode('utf-8')

    stdscr.addstr(4, 0, "Mot de passe: ")
    stdscr.refresh()
    curses.curs_set(1)  # Afficher le curseur pour la saisie du mot de passe
    password = stdscr.getstr(4, 15, 20).decode('utf-8')
    curses.curs_set(0)  # Masquer le curseur après la saisie du mot de passe

    return username, password

# Fonction pour vérifier le nom d'utilisateur et le mot de passe
def check_credentials(username, password):
    saved_username, saved_password = get_username_and_password()
    return username == saved_username and password == saved_password

# Fonction pour crypter le mot de passe à l'aide des outils GNU
def encrypt_password_with_gnu(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Crypter le mot de passe avec des outils GNU")
    stdscr.refresh()

    # Récupérer le mot de passe actuel
    username, password = get_username_and_password()

    # Utiliser openssl pour le cryptage
    try:
        encrypted_password = subprocess.check_output(["openssl", "passwd", "-1", password])
        encrypted_password = encrypted_password.decode('utf-8').strip()
        create_or_update_config(username, encrypted_password)
        stdscr.addstr(2, 0, "Mot de passe crypté avec succès.")
        stdscr.refresh()
    except subprocess.CalledProcessError:
        stdscr.addstr(2, 0, "Erreur lors du cryptage du mot de passe.")
        stdscr.refresh()

    stdscr.getch()
    


def show_help():
    print("show config.edx")


def usr_crack_function():
    print("show config.edx")
    

def show_files():
    print("show config.edx")
    


def list_and_execute_commands(stdscr):
    os.system(f'system/root/commands/main/syst-commands')
