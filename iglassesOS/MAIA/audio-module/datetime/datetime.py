from espeakng import ESpeakNG
import time

# Liste des mois
mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

# Liste des jours de la semaine
jour = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

# Fonction pour prononcer la date et l'heure
def direDateHeure():
    esng = ESpeakNG(voice='fr')
    t = time.localtime()

    s = 'Nous sommes le ' + jour[t.tm_wday]

    if t.tm_mday == 1:
        s = s + ' premier'
    else:
        s = s + ' ' + str(t.tm_mday)

    s = s + ' ' + mois[t.tm_mon - 1] + '. ' + str(t.tm_year)

    if t.tm_hour == 12:
        s = s + ' Il est midi.'
    else:
        s = s + ' Il est : ' + str(t.tm_hour) + ' heure.'

    esng.say(s, sync=True)

# Début du programme
esng = ESpeakNG()
print(esng.voices)

direDateHeure()
