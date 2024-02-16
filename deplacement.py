import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mini Jeu Python")

# Position initiale du joueur
player_x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
player_y = SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2

# Vitesse du joueur
player_speed = 5

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Récupérer les touches pressées
    keys = pygame.key.get_pressed()
    
    # Déplacer le joueur en fonction des touches pressées
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_SIZE:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - PLAYER_SIZE:
        player_y += player_speed

    # Effacer l'écran
    screen.fill(WHITE)

    # Dessiner le joueur
    pygame.draw.rect(screen, RED, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôler la fréquence de rafraîchissement
    pygame.time.Clock().tick(30)