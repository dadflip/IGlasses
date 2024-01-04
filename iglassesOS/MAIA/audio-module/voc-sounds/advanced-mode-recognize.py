import csv
import subprocess
import time
import os
import requests
import speech_recognition as sr
from gtts import gTTS
import speak

# URL d'un site Web pour la vérification de la connexion Internet
internet_check_url = "https://www.google.com"

def is_internet_available():
    try:
        response = requests.get(internet_check_url, timeout=3)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

# Charger les correspondances depuis le fichier keywords.txt
def load_keyword_functions():
    keyword_functions = {}
    with open('MAIA/audio-module/voc-sounds/keywords/keywords.txt', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                keyword, function_name = [entry.strip() for entry in row]
                keyword_functions[keyword] = function_name
    return keyword_functions

# Initialisation de l'objet Recognizer
recognizer = sr.Recognizer()

# Variable de drapeau pour indiquer si une commande a été détectée
command_detected = False

def listen_and_respond():
    speak.more_options()
    global command_detected  # Déclarez la variable comme globale

    with sr.Microphone(sample_rate=16000) as source:
        os.system("python3 MAIA/audio-module/voc-sounds/speak.py parler 'Je vous écoute'")
        print("En attente d'une nouvelle commande...")
        recognizer.adjust_for_ambient_noise(source)

        while not command_detected:
            try:
                # Vérifiez la disponibilité de la connexion Internet
                internet_connected = is_internet_available()
                if not internet_connected:
                    print("Pas de connexion Internet. Attente de rétablissement...")
                    subprocess.run(["python3", "MAIA/audio-module/voc-sounds/no-connection-recognition.py"])
                    while not is_internet_available():
                        time.sleep(5)
                    print("Connexion Internet rétablie.")
                    os.system("python3 MAIA/audio-module/voc-sounds/speak.py presentation")  # Redonnez la présentation de l'assistant
                    
                audio = recognizer.listen(source, timeout=3)
                text = recognizer.recognize_google(audio, language="fr-FR")
                print("Vous avez dit : " + text)

                # Recherchez des correspondances de mots-clés dans le texte
                for keyword, function_name in keyword_functions.items():
                    if keyword in text:
                        print(f"Mot-clé détecté : {keyword}")
                        command_detected = True  # Définissez le drapeau pour indiquer que la commande a été détectée
                        # Exécutez la fonction associée au mot-clé
                        try:
                            module = __import__('functions', fromlist=[function_name])
                            function_to_call = getattr(module, function_name)
                            function_to_call()
                        except Exception as e:
                            print(f"Erreur lors de l'exécution de la fonction : {e}")
                        command_detected = False

            except sr.WaitTimeoutError:
                continue  # Passez au cycle suivant si aucune commande n'a été détectée

            except sr.UnknownValueError:
                #speak.incomprehension()
                print("Désolé, je n'ai pas pu comprendre ce que vous avez dit. Réessayez.")

            except sr.RequestError as e:
                os.system("python3 MAIA/audio-module/voc-sounds/speak.py erreur")
                print("Erreur lors de la demande à l'API Google : {0}".format(e))

if __name__ == '__main__':
    keyword_functions = load_keyword_functions()
    listen_and_respond()
    speak.user_mode()

