"""
Script: Jeu du Pendu
Description: Ce script contient une implémentation du jeu du pendu en Python.
             Le joueur peut proposer des lettres pour deviner un mot sélectionné au hasard dans un fichier texte
             jusqu'à ce que le mot soit deviné ou que le nombre maximum de tentatives soit atteint.
Auteur: Lou-Anne Villette
Date: 23/05/2024
"""

# Importation de la fonction choice du module random pour choisir un mot aléatoirement
from random import choice
# Importation de la fonction normalize pour gérer les accents
from unicodedata import normalize

# Définir le nombre maximum de tentatives pour deviner le mot
MAX_ATTEMPS = 6


def request_file_path():
    """
    Demande à l'utilisateur le chemin complet du fichier contenant les mots.
    Retours:
        str: Chemin complet vers le fichier contenant les mots, ou chemin du fichier par défaut.
    """
    # Demande à l'utilisateur d'entrer le chemin complet du fichier contenant les mots
    complete_file_path = input('Entrez le chemin complet du fichier contenant les mots.\n\
Appuyez directement sur la touche "entrée" pour utiliser le fichier par défaut.\n').strip()
    # Si aucun chemin n'est fourni, utilise le fichier par défaut 'mots_pendu.txt'
    if not complete_file_path:
        complete_file_path = 'mots_pendu.txt'
    return complete_file_path


def select_random_word(complete_file_path="mots_pendu.txt"):
    """
        Sélectionne un mot aléatoire à partir d'un fichier texte contenant une liste de mots.
        Paramètres:
            complete_file_path (str): Chemin complet vers le fichier contenant les mots.
                                      Par défaut, "mots_pendu.txt".
        Retours:
            str: Un mot choisi aléatoirement dans le fichier.
            list: Une liste vide si le fichier n'est pas trouvé.
        """
    try:
        # Tente d'ouvrir le fichier spécifié en mode lecture avec l'encodage UTF-8
        with open(complete_file_path, 'r', encoding='utf8') as f:
            # Lit toutes les lignes du fichier et les stocke dans une liste
            words = f.read().splitlines()
        # Renvoie un mot choisi aléatoirement dans la liste des mots
        return choice(words)
    except FileNotFoundError:
        # Capture l'exception si le fichier n'est pas trouvé
        print("Fichier non trouvé. Vérifiez le chemin complet du fichier.")


def remove_accents(word):
    """
    Supprime les accents d'un mot donné.
    Paramètres:
        word (str): Le mot dont les accents doivent être supprimés.
    Retours:
        str: Le mot sans accents.
    """
    # Utilise la normalisation Unicode pour décomposer les caractères accentués
    # Encode ensuite en ASCII pour supprimer les caractères non-ASCII
    # Décode à nouveau en UTF-8 pour obtenir une chaîne de caractères sans accents
    return normalize('NFD', word).encode('ASCII', 'ignore').decode('utf8')


def word_current_state(word, letters_found):
    """
    Retourne l'état actuel du mot à deviner en remplaçant les lettres non trouvées par des tirets.
    Paramètres:
        word (str): Le mot à deviner.
        letters_found (list): Liste des lettres déjà trouvées dans le mot.
    Retours:
        str: Le mot avec les lettres trouvées affichées et les autres cachées par des tirets.
    """
    # Pour chaque lettre dans le mot, si la lettre a été trouvée la laisser telle quelle, sinon mettre un tiret
    return ' '.join(letter if letter in letters_found else '_' for letter in word)


def request_letter():
    """
    Demande à l'utilisateur d'entrer une lettre et la retourne après avoir supprimé les accents et mis en minuscule.
    Retours:
        str: La lettre saisie par l'utilisateur, sans accents et en minuscules.
    """
    # Demande à l'utilisateur d'entrer une lettre et la stocke dans la variable 'letter'
    letter = input("Entrez une lettre : ").strip().lower()
    # Utilise la fonction remove_accents pour supprimer les accents de la lettre
    return remove_accents(letter)


def print_hint(word, bad_letters):
    """
    Affiche un indice pour aider le joueur à trouver la lettre suivante.
    Cette méthode sélectionne une lettre de l'alphabet qui n'a pas encore été essayée et non présente dans le mot,
    puis l'affiche comme indice pour le joueur.
    Paramètres:
        word (str): Le mot à deviner.
        bad_letters (list): Liste des lettres incorrectes déjà essayées par le joueur.
    """
    # Crée une liste de l'alphabet en minuscules en séparant chaque lettre
    alphabet = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()
    alphabet_size = len(alphabet)  # Taille de l'alphabet

    j = 0  # Initialise un compteur pour parcourir l'alphabet

    # Parcours de chaque lettre de l'alphabet
    for i in range(alphabet_size):
        # Vérifie si la lettre de l'alphabet courante est présente dans le mot à deviner
        if alphabet[j] in word:
            alphabet.pop(j)  # Si oui, retire cette lettre de l'alphabet (elle a déjà été trouvée)
        # Vérifie si la lettre de l'alphabet courante est déjà dans la liste des mauvaises lettres
        elif alphabet[j] in bad_letters:
            alphabet.pop(j)  # Si oui, retire cette lettre de l'alphabet (elle a déjà été essayée)
        else:
            j += 1  # Si la lettre n'est ni dans le mot ni dans les mauvaises lettres, passe à la lettre suivante

    # Après avoir parcouru l'alphabet, sélectionne une lettre aléatoire parmi les lettres restantes
    hint = choice(alphabet)

    # Ajoute la lettre sélectionnée à la liste des mauvaises lettres (pour éviter de la proposer à nouveau)
    bad_letters.append(hint)

    # Affiche l'indice pour le joueur
    print(f"Indice: la lettre {hint} n'est pas dans le mot.\n ")


def play_single_game(word):
    """
    Méthode pour jouer une seule partie du jeu du Pendu.
    Paramètres:
        word (str): Le mot à deviner.
    """
    # Supprime les accents du mot à deviner
    word = remove_accents(word)
    # Initialise le nombre de tentatives restantes
    remaining_attempts = MAX_ATTEMPS
    # Initialise une liste pour stocker les lettres trouvées
    letters_found = []
    # Initialise une liste pour stocker les mauvaises lettres
    bad_letters = []
    # Indique si un indice a déjà été donné
    hint_given = 0

    # Boucle principale du jeu
    while remaining_attempts > 0:
        # Affiche l'état actuel du mot à deviner
        print(f"Mot à deviner : {word_current_state(word, letters_found)}")
        # Affiche les lettres incorrectes déjà essayées
        print(f"Lettres ratées: {', '.join(bad_letters)}")
        # Affiche le nombre de tentatives restantes
        print(f"Chances restantes: {remaining_attempts}")

        # Donne un indice au joueur s'il ne lui reste qu'une seule tentative et s'il n'en a pas encore reçu
        if remaining_attempts == 1 and hint_given == 0:
            hint_given = 1
            print_hint(word, bad_letters)

        # Demande à l'utilisateur d'entrer une lettre
        letter = request_letter()

        # Vérifie si la lettre entrée est dans le mot
        if letter in word:
            # Si la lettre est dans le mot, l'ajoute à la liste des lettres trouvées
            letters_found.append(letter)
            print("Bonne lettre!\n")
            # Vérifie si le mot a été entièrement trouvé
            if word == word_current_state(word, letters_found).replace(" ", ""):
                print(f"Félicitations! Vous avez trouvé le mot: {word}.\n")
                break
        else:
            # Si la lettre n'est pas dans le mot, l'ajoute à la liste des mauvaises lettres
            if letter not in bad_letters:
                bad_letters.append(letter)
                remaining_attempts -= 1
                print("Mauvaise lettre!\n")
            else:
                # Si la lettre a déjà été essayée, affiche un message approprié
                print("Vous avez déjà essayé cette lettre.\n")

    # Si le joueur a épuisé toutes ses tentatives, affiche le mot et informe qu'il a perdu
    if remaining_attempts == 0:
        print(f"Désolé, vous avez perdu! Le mot était: {word}")


def play_hangman(change_file='o'):
    """
    Méthode principale pour jouer au jeu du Pendu.
    Paramètres:
        change_file (str): Indique si le joueur veut changer de fichier de mots ('o' pour oui, 'n' pour non).
                           Par défaut, 'o' pour permettre le changement de fichier.
    """
    print("Bienvenue au jeu du Pendu!")

    complete_file_path = ""  # Initialise le chemin du fichier à vide

    while True:  # Boucle principale du jeu
        if change_file == 'o':  # Vérifie si le joueur veut changer de fichier de mots
            complete_file_path = request_file_path()  # Demande le chemin du fichier

        word = select_random_word(complete_file_path)  # Sélectionne un mot aléatoire dans le fichier
        if not word:  # Si aucun mot n'est trouvé
            retry = input("Voulez-vous réessayer ? (o/n): ").strip().lower()  # Demande si le joueur veut réessayer
            print("\n")
            if retry == 'n':  # Si le joueur ne veut pas réessayer, sort de la boucle
                break
            else:
                continue  # Sinon, continue la boucle pour une nouvelle partie

        play_single_game(word)  # Joue une partie du jeu avec le mot sélectionné

        replay = input("Voulez-vous rejouer ? (o/n): ").strip().lower()  # Demande si le joueur veut rejouer
        if replay == 'o':  # Si le joueur veut rejouer
            # Demande si le joueur veut changer de fichier de mots pour la prochaine partie
            change_file = input("Voulez-vous tirer un mot dans un autre fichier ? (o/n) : ").strip().lower()
            print("\n")
        else:
            break  # Si le joueur ne veut pas rejouer, sort de la boucle et termine le jeu


if __name__ == "__main__":
    # Si le script est exécuté en tant que programme principal
    # (et non importé en tant que module dans un autre script)
    # Commence le jeu du Pendu
    play_hangman()
