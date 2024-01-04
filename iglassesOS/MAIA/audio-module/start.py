import requests
import time
import os

# URL d'un site Web que vous allez essayer de requêter
url = "https://www.google.com"

def is_internet_available():
    try:
        # Effectue une requête HTTP
        response = requests.get(url, timeout=3)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def launch_input_voice():
    os.system("python3 MAIA/audio-module/voc-sounds/user-mode.py")

def launch_no_connection_recognition():
    os.system("python3 MAIA/audio-module/voc-sounds/no-connection-recognition.py")

if __name__ == '__main__':
    if is_internet_available():
        # Lancer le programme input_voice.py s'il y a une connexion Internet
        launch_input_voice()
    else:
        # Lancer le programme no-connection-recognition.py s'il n'y a pas de connexion Internet
        launch_no_connection_recognition()

    # Attendez quelques secondes avant de fermer la fenêtre de console
    time.sleep(5)

