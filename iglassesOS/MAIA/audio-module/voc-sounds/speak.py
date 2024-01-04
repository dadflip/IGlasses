from gtts import gTTS
import playsound

def speak(texte):
    # Convertir le texte en parole
    tts = gTTS(text=texte, lang='fr')

    # Sauvegarder la parole en tant que fichier audio
    tts.save("parole.mp3")

    # Jouer le son préenregistré
    playsound.playsound("parole.mp3")

def presentation():
    speak("Bonjour, je suis votre assistante MAIA. Comment puis-je vous aider ?")

def error():
    speak("Désolé, une erreur s'est produite. Veuillez réessayer plus tard.")

def incomprehension():
    speak("Je suis désolé, je n'ai pas compris votre demande. Pouvez-vous répéter ?")

def bye():
    speak("Au revoir, à bientôt !")
    
def more_options():
    speak("Maya à votre service ! Dites commande pour découvrir les commandes disponibles")

def user_mode():
    speak("Mode utilisateur ! Je vous écoute")
