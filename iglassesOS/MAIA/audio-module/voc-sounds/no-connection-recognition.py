import vosk
import pyaudio
import socket
import time
import json
import csv  # Ajout de l'importation du module csv

# Charger les correspondances depuis le fichier no-co.txt
def load_keyword_functions():
    keyword_functions = {}
    with open('MAIA/audio-module/voc-sounds/no-co-keywords/no-co.txt', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                keyword, function_name = [entry.strip() for entry in row]
                keyword_functions[keyword] = function_name
    return keyword_functions

# Fonction pour vérifier la connectivité Internet
def check_internet_connection(host="www.google.com", port=80):
    try:
        socket.create_connection((host, port), timeout=5)
        return True
    except OSError:
        pass
    return False

# Chemin vers le modèle Vosk que vous avez téléchargé
model_path = "MAIA/audio-module/voc-sounds/no-co-lang-models/fr_FR/vosk-model-small-fr-pguyot-0.3"

# Créez un reconnaisseur Vosk avec le modèle
recognizer = vosk.KaldiRecognizer(vosk.Model(model_path), 16000)

# Configuration pour PyAudio
audio_format = pyaudio.paInt16
sample_rate = 16000
chunk_size = 5000  # Vous pouvez ajuster la taille du chunk en fonction de vos besoins

# Initialisez PyAudio
audio_stream = pyaudio.PyAudio()

# Ouvrez un flux audio depuis le microphone
stream = audio_stream.open(
    format=audio_format,
    channels=1,  # 1 canal pour l'audio mono, 2 pour l'audio stéréo
    rate=sample_rate,
    input=True,
    frames_per_buffer=chunk_size
)

print("Dites quelque chose...")

# Paramètres pour le timeout et la qualité de la reconnaissance
timeout_seconds = 10  # Timeout de 10 secondes
min_confidence = 0.8  # Confidence minimale pour une reconnaissance valide

start_time = time.time()
recognized_text = ""

# Définissez le nombre d'itérations avant de vérifier la connexion Internet
iterations_before_check = 50
current_iteration = 0
internet_connected = True  # Ajout de la variable pour suivre l'état de la connexion Internet

# Chargez les correspondances de mots-clés
keyword_functions = load_keyword_functions()

# Boucle d'acquisition et de reconnaissance vocale
while True:
    try:
        audio_chunk = stream.read(chunk_size)
        recognizer.AcceptWaveform(audio_chunk)
        result = recognizer.Result()
        print(result)

        # Mettez à jour le texte reconnu
        recognized_text += result

        # Vérifiez si la reconnaissance est suffisamment précise et si le timeout est atteint
        final_result = json.loads(result)
        if time.time() - start_time > timeout_seconds and "conf" in final_result and final_result["conf"] >= min_confidence:
            print("Reconnaissance terminée avec précision suffisante.")
            break
            
        # Affichez le texte final reconnu
        print("Texte reconnu :", recognized_text)

        # Recherchez des correspondances de mots-clés dans le texte
        for keyword, function_name in keyword_functions.items():
            if keyword in recognized_text:
                print(f"Mot-clé détecté : {keyword}")
                # Exécutez la fonction associée au mot-clé
                try:
                    module = __import__('functions', fromlist=[function_name])
                    function_to_call = getattr(module, function_name)
                    function_to_call()
                except Exception as e:
                    print(f"Erreur lors de l'exécution de la fonction : {e}")


        # Vérifiez la connexion Internet toutes les 50 itérations
        current_iteration += 1
        if current_iteration >= iterations_before_check:
            if check_internet_connection():
                if not internet_connected:
                    print("La connexion Internet s'est rétablie. Sortie de la boucle.")
                    break
                internet_connected = True
            else:
                internet_connected = False
            current_iteration = 0  # Réinitialisez le compteur après la vérification

    except KeyboardInterrupt:
        # Arrêtez la boucle en appuyant sur Ctrl+C
        break




