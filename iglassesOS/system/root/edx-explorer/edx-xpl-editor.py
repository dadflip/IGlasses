import json
import os

from variables import *

def load_menu_config(filename):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)

        with open(file_path, 'r') as config_file:
            menu_config = json.load(config_file)
        return menu_config
    except FileNotFoundError:
        return None

def save_menu_config(filename, menu_config):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    with open(file_path, 'w') as config_file:
        json.dump(menu_config, config_file, indent=4)

def edit_menu_entry(menu, path, new_data):
    if len(path) == 1:
        for option in menu["options"]:
            if option["label"] == path[0]:
                option.update(new_data)
                return
    else:
        for option in menu["options"]:
            if "submenu" in option:
                if option["label"] == path[0]:
                    edit_menu_entry(option["submenu"], path[1:], new_data)

if __name__ == "__main__":
    filename = MENU_CONFIG_FILE_PATH
    menu_config = load_menu_config(filename)

    if menu_config is None:
        print(f"Erreur: Le fichier {filename} n'a pas été trouvé.")
    else:
        print("Menu actuel :")
        print(json.dumps(menu_config, indent=4))
        while True:
            entry_path = input("Entrez le chemin de l'entrée que vous souhaitez modifier (séparé par des virgules) ou 'q' pour quitter : ")
            if entry_path.lower() == 'q':
                break

            entry_path = entry_path.split(",")
            new_data = {}

            new_title = input("Nouveau titre (laissez vide pour ne pas modifier) : ")
            if new_title:
                new_data["title"] = new_title

            new_action = input("Nouvelle action (laissez vide pour ne pas modifier) : ")
            if new_action:
                new_data["action"] = new_action

            edit_menu_entry(menu_config, entry_path, new_data)

        save_menu_config(filename, menu_config)
        print(f"Menu enregistré dans le fichier {filename}.")
