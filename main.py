"""
Script: Jeu du Pendu
Description: Ce script contient une implémentation du jeu du pendu en Python.
             Le joueur peut proposer des lettres pour deviner un mot sélectionné au hasard dans un fichier texte
             jusqu'à ce que le mot soit deviné ou que le nombre maximum de tentatives soit atteint.
Auteur: Lou-Anne Villette
Date: 23/05/2024
"""

from random import choice

def select_random_word(complete_path_file="mots_pendu.txt"):
    try:
        with open(complete_path_file, 'r', encoding='utf8') as f:
            words = f.read().splitlines()
        return choice(words)
    except FileNotFoundError:
        print("Fichier non trouvé. Vérifiez le chemin complet du fichier.")
        return []
