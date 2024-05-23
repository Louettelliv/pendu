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
        # Renvoie une liste vide pour indiquer qu'aucun mot n'a été trouvé
        return []


def remove_accents(word):
    """
    Supprime les accents d'un mot donné.
    Paramètres:
        word (str): Le mot dont les accents doivent être supprimés.
    Retours:
        str: Le mot sans accents.
    """
    return normalize('NFD', word).encode('ASCII', 'ignore').decode('utf8')
