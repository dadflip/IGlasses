from pocketsphinx import LiveSpeech

# Chemin vers votre fichier de grammaire JSGF
custom_grammar_path = "no-co.gram"

for phrase in LiveSpeech(dict="no-co.dict", jsgf=custom_grammar_path):
    print(f"Commande détectée: {phrase}")
    # Exécutez l'action associée à la commande ici
