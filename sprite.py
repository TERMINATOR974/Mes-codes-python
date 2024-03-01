
import pygame
import sys
from pygame.locals import *

pygame.init()

# Initialisation de la fenêtre
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Animation de Sprites')

# Chargement des sprites
sprite1 = pygame.image.load('image1.png').convert_alpha()
sprite2 = pygame.image.load('image2.png').convert_alpha()
sprite3 = pygame.image.load('image3.png').convert_alpha()
sprite4 = pygame.image.load('image4.png').convert_alpha()
sprite5 = pygame.image.load('image5.png').convert_alpha()

sprites = [sprite1, sprite2, sprite3, sprite4, sprite5]

# Initialisation des variables
clock = pygame.time.Clock()
current_sprite_index = 0
frame_count = 0
change_interval = 10  # Changer de sprite toutes les 10 frames

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Logique pour changer de sprite
    frame_count += 1
    if frame_count % change_interval == 0:
        current_sprite_index = (current_sprite_index + 1) % len(sprites)

    # Affichage du sprite actuel
    window.fill((255, 255, 255))  # Fond blanc
    window.blit(sprites[current_sprite_index], (width // 2, height // 2))

    pygame.display.flip()
    clock.tick(60)  # Limiter le framerate à 60 FPS


