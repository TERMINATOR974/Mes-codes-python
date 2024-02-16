#!/usr/bin/env python
# coding: utf-8
#
# Tom's Pong
# A simple pong game with realistic physics and AI
# http://tom.acrewoods.net/projects/pong
#
# Released under the GNU General Public License

VERSION = "0.4"

try:
    import sys
    import random
    import math
    import os
    from socket import *
    import pygame
    from pygame.locals import *
except ImportError as err:
    print("Impossible de charger le module. %s" % (err))
    sys.exit(2)
 
def main():
    # Initialisation de la fenêtre d'affichage
    pygame.init()
    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption('Programme Pygame de base')
 
    # Remplissage de l'arrière-plan
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
 
    # Affichage d'un texte
    font = pygame.font.Font(None, 36)
    text = font.render("Salut tout le monde", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = background.get_rect().centery
    background.blit(text, textpos)
 
    # Afficher le tout dans la fenêtre
    screen.blit(background, (0, 0))
    pygame.display.flip()
 
    # Boucle d'évènements
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
 
        screen.blit(background, (0, 0))
        pygame.display.flip()
 
if __name__ == '__main__': main()


def __init__(self):
    # Initialisation de la balle
    largeur, hauteur= 600, 400
    balle_taille = 10
    balle_vitesse = [5.00, 5.00] #vitesse initiale de la balle
    balle = pygame.Rect(largeur // 2 - balle_taille // 2, hauteur // 2 - balle_taille // 2, balle_taille, balle_taille)

def update(self):
    # Mettre à jour la position de la balle
    pass

    # Vérifier si la balle touche les bords
    pass

def main():
    # Initialiser l'environnement du jeu ici

    # Créer un nouvel objet, instance de la classe Ball
    ball = Ball()

    while True:
        # Vérifier les entrées utilisateur

        # Appel de la méthode update() de la balle
        ball.update()

# Si vous avez des fonctions spécifiques pour charger des modules ou gérer des ressources,
# assurez-vous de les ajouter dans les sections appropriées du code.