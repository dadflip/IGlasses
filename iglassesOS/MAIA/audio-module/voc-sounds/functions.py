# functions.py
import webbrowser
import speak

def open_browser():
    # Exemple : Ouvrir le navigateur (utilisation de la bibliothèque webbrowser)
    webbrowser.open("https://www.google.com")

def search_on_internet(query):
    speak.speak("recherche en cours...")
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

    
    
import sys

def close_application():
    sys.exit()


import os

def get_environment_info():
    environment_info = os.environ
    return environment_info

import datetime  # Importez le module datetime
def get_time_of_day():
    now = datetime.datetime.now()
    hour = now.hour
    if 6 <= hour < 12:
        speak.speak("C'est le matin.")
    elif 12 <= hour < 18:
        speak.speak("C'est l'après-midi.")
    elif 18 <= hour < 24:
        speak.speak("C'est le soir.")
    else:
        speak.speak("C'est la nuit.")


def get_current_time():
    import subprocess
    try:
        subprocess.run(["python3", "MAIA/audio-module/datetime/datetime.py"])
    except Exception as e:
        print(f"Erreur lors de l'exécution de datetime.py : {e}")
        
        
import geocoder

def get_location():
    try:
        # Utilisez la fonction `ip` de geocoder pour obtenir la localisation en fonction de l'adresse IP
        location = geocoder.ip('me')
        
        # Vérifiez si la localisation a été trouvée
        if location.ok:
            latitude = location.latlng[0]
            longitude = location.latlng[1]
            address = location.address

            speak.speak(f"Latitude: {latitude}")
            speak.speak(f"Longitude: {longitude}")
            speak.speak(f"Adresse: {address}")
        else:
            speak.speak("Impossible de trouver l'emplacement.")

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")



import pyttsx3
import speech_recognition as sr
import time
import speak

# Fonction pour lire les commandes vocales du fichier
def lire_commandes_vocales():
    speak.speak("Voici la liste des commandes système")

    # Initialisation du moteur de synthèse vocale
    engine = pyttsx3.init()

    # Initialisation de l'objet Recognizer
    recognizer = sr.Recognizer()

    with open('MAIA/audio-module/voc-sounds/keywords/keywords.txt', 'r') as file:
        lines = file.readlines()

        stop_listening = recognizer.listen_in_background(sr.Microphone(), callback)
        
        for line in lines:
            command = line.split(',')[0].strip()
            print(f"Commande vocale : {command}")
            speak.speak(command)  # Utilisez la fonction parler de speak pour la synthèse vocale
            # Attendez un moment pour que la synthèse vocale se termine
            time.sleep(1)  # Vous pouvez ajuster la durée en secondes

        # Attendez que l'utilisateur dise "stop"
        while True:
            if stop_listening.done:
                break

# Fonction de rappel pour détecter "stop"
def callback(recognizer, audio):
    try:
        stop_command = recognizer.recognize_google(audio, language="fr-FR")
        if "stop" in stop_command.lower():
            print("Commande vocale 'stop' détectée. Arrêt du listing.")
            recognizer.stop_listening()  # Arrêtez la reconnaissance
    except sr.UnknownValueError:
        pass  # Ignorer si la reconnaissance échoue
