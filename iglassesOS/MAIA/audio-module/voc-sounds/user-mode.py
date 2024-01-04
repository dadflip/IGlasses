import speech_recognition as sr
import subprocess
import requests
import time
import logging

import speak

# URL pour vérifier la connectivité Internet
internet_check_url = "https://www.google.com"

# Configuration des journaux
logging.basicConfig(filename='assistant.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def is_internet_available():
    try:
        response = requests.get(internet_check_url, timeout=3)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def main():
    recognizer = sr.Recognizer()
    speak.presentation()
    speak.user_mode()
    
    while True:
        try:
            # Vérifiez la connectivité Internet
            internet_connected = is_internet_available()
        except Exception as e:
            logging.error(f"Erreur lors de la vérification de la connectivité Internet : {e}")
            internet_connected = False
        if internet_connected:
            try:
                with sr.Microphone(sample_rate=16000) as source:
                    print("En attente d'une nouvelle commande...")
                    recognizer.adjust_for_ambient_noise(source)
                    try:
                        audio = recognizer.listen(source, timeout=3)
                    except sr.WaitTimeoutError:
                        print("Aucune commande vocale détectée. Veuillez réessayer.")
                        continue
            except Exception as e:
                logging.error(f"Erreur lors de l'écoute audio : {e}")
                continue

            try:
                text = recognizer.recognize_google(audio, language="fr-FR")
                print("Vous avez dit : " + text)

                if "au revoir" in text or "quitter" in text:
                    print("Au revoir!")
                    speak.bye()
                    return
                elif "maya" in text or "Maya" in text or "Maia" in text or "activation" in text:
                    subprocess.run(["python", "MAIA/audio-module/voc-sounds/advanced-mode-recognize.py"])
                    print("Passage en mode avancé.")
                    speak.more_options()
            except Exception as e:
                logging.error(f"Erreur lors de la reconnaissance vocale : {e}")
        
        else:
            print("Pas de connexion Internet. Basculement sur no-connection-recognition.py.")
            subprocess.run(["python", "MAIA/audio-module/voc-sounds/no-connection-recognition.py"])
            time.sleep(5)  # Attendez avant de réessayer la vérification de la connexion

if __name__ == "__main__":
    main()

