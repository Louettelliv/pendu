"""
Script: Jeu du Pendu
Description: Ce script contient une implémentation du jeu du pendu en Python.
             Le joueur peut proposer des lettres pour deviner un mot sélectionné au hasard dans un fichier texte
             jusqu'à ce que le mot soit deviné ou que le nombre maximum de tentatives soit atteint.
Auteur: Lou-Anne Villette
Date: 23/05/2024
"""

from random import choice
from unicodedata import normalize



def select_random_word(complete_path_file="mots_pendu.txt"):
    """
        Sélectionne un mot aléatoire à partir d'un fichier texte contenant une liste de mots.
        Paramètres:
            complete_path_file (str): Chemin complet vers le fichier contenant les mots.
                                      Par défaut, "mots_pendu.txt".
        Retours:
            str: Un mot choisi aléatoirement dans le fichier.
            list: Une liste vide si le fichier n'est pas trouvé.
        """
    try:
        # Tente d'ouvrir le fichier spécifié en mode lecture avec encodage UTF-8
        with open(complete_path_file, 'r', encoding='utf8') as f:
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
    return normalize('NFD', word).encode('ASCII', 'ignore').decode('utf8')


def word_current_state(word, letters_found):
    return ' '.join(letter if letter in letters_found else '_' for letter in word)


def request_letter():
    letter = input("Entrez une lettre : ").strip().lower()
    return remove_accents(letter)


def play_hangman():
    print("Bienvenue au jeu du Pendu!")

    while True:
        complete_path_file = input('Entrez le chemin complet du fichier contenant les mots.\n\
Appuyez directement sur la touche "entrée" pour utiliser le fichier par défaut.\n')
        if not complete_path_file:
            complete_path_file = 'mots_pendu.txt'

        word = select_random_word(complete_path_file)
        if not word:
            retry = input("Voulez-vous réessayer ? (o/n): ")
            if retry == 'n':
                break

        word = remove_accents(word)
        remaining_attempts = 6
        letters_found = []
        bad_letters = []

        while remaining_attempts > 0:

            print(f"Mot à deviner : {word_current_state(word, letters_found)}")
            print(f"Lettres ratées: {', '.join(bad_letters)}")
            print(f"Chances restantes: {remaining_attempts}")

            letter = request_letter()
            if letter in word:
                letters_found.append(letter)
                print("Bonne lettre!")
                if word == word_current_state(word, letters_found).replace(" ",""):
                    print(f"Félicitations! Vous avez trouvé le mot: {word}")
                    break
            else:
                if letter not in bad_letters:
                    bad_letters.append(letter)
                    remaining_attempts -= 1
                    print("Mauvaise lettre!")
                    if remaining_attempts == 1:
                        alphabet = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()
                        alphabet_size=len(alphabet)
                        j = 0
                        for i in range(alphabet_size):
                            if alphabet[j] in word:
                                alphabet.pop(j)
                            elif alphabet[j] in bad_letters:
                                alphabet.pop(j)
                            else:
                                j += 1
                        print(f"Indice: une lettre {choice(alphabet)} n'est pas dans le mot.\n ")
                else:
                    print("Vous avez déjà essayé cette lettre.")

        if remaining_attempts == 0:
            print(f"Désolé, vous avez perdu! Le mot était: {word}")

        replay = input("Voulez-vous rejouer ? (o/n): ").strip().lower()
        if replay != 'o':
            break




if __name__ == "__main__":
    play_hangman()
