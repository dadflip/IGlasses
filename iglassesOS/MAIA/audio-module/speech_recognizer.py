import vosk
import sys
import os
import wave
import json

def recognize_speech(audio_file, model_path, timeout):
    if not os.path.exists(model_path):
        raise Exception(f"Le modèle '{model_path}' n'existe pas.")
    
    # Créez un reconnaisseur Vosk
    vosk_model = vosk.Model(model_path)
    rec = vosk.KaldiRecognizer(vosk_model, 16000)

    # Ouvrez le fichier audio
    audio = wave.open(audio_file, 'rb')

    # Paramètres du timeout (en secondes)
    timeout_limit = timeout
    start_time = time.time()

    # Effectuez la reconnaissance vocale
    result = {"text": ""}
    while True:
        data = audio.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result["text"] += rec.Result()
        if time.time() - start_time > timeout_limit:
            break

    result["text"] += rec.FinalResult()
    return json.loads(result["text"])

if __name__ == '__main__':
    audio_file = 'audio.wav'
    model_path = 'voc-sounds/no-co-lang-models/fr_FR/vosk-model-small-fr-pguyot-0.3'
    timeout = 10  # Timeout de 10 secondes

    try:
        recognized_text = recognize_speech(audio_file, model_path, timeout)
        print("Texte reconnu :", recognized_text)
    except Exception as e:
        print(f"Erreur : {e}")

