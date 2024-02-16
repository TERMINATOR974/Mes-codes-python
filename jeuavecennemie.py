import pygame
import sys
import random
import math

# Initialisation de Pygame
pygame.init()

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
ENEMY_SIZE = 30
NUM_ENEMIES = 0  # Démarre avec zéro ennemi
MAX_ENEMIES = 5  # Nombre maximal d'ennemis à l'écran
ENEMY_SPAWN_INTERVAL = 10  # Interval de spawn des ennemis en secondes
PLAYER_LIVES = 3
MAX_REPULSE_COUNT = 3

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu avec Ennemis Python")

# Position initiale du joueur
player_x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
player_y = SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2

# Position initiale des ennemis
enemies = []

# Vitesse du joueur
player_speed = 5

# Vitesse des ennemis
enemy_speed = 2

# Fonction pour calculer la distance entre deux points
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Minuterie pour le spawn des ennemis
spawn_timer = 0

# Compteur pour les utilisations de la capacité de repoussement
repulse_count = MAX_REPULSE_COUNT

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

    # Repousser les ennemis si la touche Espace est pressée (avec limite de 3 utilisations)
    if keys[pygame.K_SPACE] and repulse_count > 0:
        for i in range(len(enemies)):
            enemy_x, enemy_y = enemies[i]
            if distance(player_x, player_y, enemy_x, enemy_y) < 100:  # Répulsion si l'ennemi est à moins de 100 pixels
                angle = math.atan2(player_y - enemy_y, player_x - enemy_x)
                enemy_x -= 2 * enemy_speed * math.cos(angle)
                enemy_y -= 2 * enemy_speed * math.sin(angle)
                enemies[i] = (enemy_x, enemy_y)
        repulse_count -= 1

    # Décrémenter le compteur de la minuterie
    spawn_timer -= 1

    # Déplacer les ennemis vers le joueur
    for i in range(len(enemies)):
        enemy_x, enemy_y = enemies[i]
        angle = math.atan2(player_y - enemy_y, player_x - enemy_x)
        enemy_x += enemy_speed * math.cos(angle)
        enemy_y += enemy_speed * math.sin(angle)
        enemies[i] = (enemy_x, enemy_y)

        # Vérifier si l'ennemi atteint le joueur
        if distance(player_x, player_y, enemy_x, enemy_y) < PLAYER_SIZE:
            print("Vous avez été touché !")
            PLAYER_LIVES -= 1
            print(f"Vies restantes : {PLAYER_LIVES}")
            enemies.remove((enemy_x, enemy_y))

    # Minuterie pour le spawn des ennemis
    if spawn_timer <= 0 and len(enemies) < MAX_ENEMIES:
        enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        enemy_y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
        enemies.append((enemy_x, enemy_y))
        spawn_timer = ENEMY_SPAWN_INTERVAL * 30  # Convertir les secondes en frames

    # Réinitialiser le compteur de la capacité de repoussement après 3 utilisations
    if repulse_count <= 0:
        repulse_count = MAX_REPULSE_COUNT

    # Effacer l'écran
    screen.fill(WHITE)

    # Dessiner le joueur
    pygame.draw.rect(screen, RED, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

    # Dessiner les ennemis
    for enemy_x, enemy_y in enemies:
        pygame.draw.rect(screen, BLUE, (enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôler la fréquence de rafraîchissement
    pygame.time.Clock().tick(30)