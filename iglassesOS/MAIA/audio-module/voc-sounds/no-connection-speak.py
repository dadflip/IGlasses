import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Réglez la vitesse de la synthèse vocale

def speak(text, voice="french"):
    engine.setProperty('voice', voice)
    engine.say(text)
    engine.runAndWait()

def error():
    speak("Une erreur s'est produite.")

def incomprehension():
    speak("Désolé, je n'ai pas pu comprendre ce que vous avez dit. Réessayez.")

def presentation():
    speak("Bienvenue dans l'assistant vocal.")

# Vous pouvez ajouter d'autres fonctions pour gérer différents types de messages

if __name__ == "__main__":
    presentation()  # Présentation au démarrage
    text = "Mode hors connexion"
    speak(text)

