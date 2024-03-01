import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 40  # Largeur du personnage ajustée pour une meilleure hitbox
PLAYER_HEIGHT = 40  # Hauteur du personnage ajustée pour une meilleure hitbox
PLATFORM_WIDTH = 80  # Largeur des plateformes réduite
PLATFORM_HEIGHT = 10  # Hauteur des plateformes réduite
PLATFORM_GAP = 150  # Espacement vertical entre les plateformes
TP_WIDTH = 50
TP_HEIGHT = 20
ENEMY_WIDTH = 30
ENEMY_HEIGHT = 30
WALL_WIDTH = 20

# Vitesse et saut du joueur
PLAYER_SPEED = 8  # Augmenter la vitesse du joueur
JUMP_COUNT = 8  # Augmenter le nombre de sauts
GRAVITY = 0.5  # Gravité pour rendre le personnage glissant
SLIDE_SPEED = 3  # Vitesse de glissement
ENEMY_SPEED = 3  # Vitesse de déplacement de l'ennemi

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu de Plateforme Python")

# Charger les images
player_image = pygame.image.load('perso1.png').convert()
platform_image = pygame.image.load('coble.png').convert()
enemy_image = pygame.image.load('longbrick.png').convert()
background_image = pygame.image.load('fond.jpg').convert()

# Redimensionner les images pour correspondre aux dimensions requises
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
platform_image = pygame.transform.scale(platform_image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_WIDTH, ENEMY_HEIGHT))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Position initiale du joueur
player_x = 50
player_y = SCREEN_HEIGHT - 2 * PLAYER_HEIGHT  # Modifier pour le placer en bas à gauche

# Vitesse du joueur
player_speed = PLAYER_SPEED
jump_count = JUMP_COUNT
is_jumping = False

# Déplacement horizontal du joueur
move_left = False
move_right = False

# Plateformes
platforms_level1 = [
    pygame.Rect(150, SCREEN_HEIGHT - 100, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(300, SCREEN_HEIGHT - 250, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(100, SCREEN_HEIGHT - 400, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(500, SCREEN_HEIGHT - 550, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(300, SCREEN_HEIGHT - 700, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(500, SCREEN_HEIGHT - 850, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(200, SCREEN_HEIGHT - 1000, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(600, SCREEN_HEIGHT - 1150, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(250, 250, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(0, SCREEN_HEIGHT - PLATFORM_HEIGHT, SCREEN_WIDTH, PLATFORM_HEIGHT),  # Hitbox pour le sol
    pygame.Rect(350, 150, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(450, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(250, 450, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(550, 600, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(100, 750, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(650, 900, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
]

platforms_level2 = [
    pygame.Rect(350, 100, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(200, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(550, 350, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(650, 650, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(250, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(600, 950, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(0, SCREEN_HEIGHT - PLATFORM_HEIGHT, SCREEN_WIDTH, PLATFORM_HEIGHT),  # Hitbox pour le sol
    pygame.Rect(350, 450, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(400, 250, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(150, 150, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(450, 600, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(200, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(500, 350, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
]

platforms_level3 = [
    pygame.Rect(200, 100, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(500, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(300, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(100, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(600, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(400, 600, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(0, SCREEN_HEIGHT - PLATFORM_HEIGHT, SCREEN_WIDTH, PLATFORM_HEIGHT),  # Hitbox pour le sol
    pygame.Rect(350, 350, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(150, 550, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(550, 250, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(450, 450, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(250, 150, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(650, 650, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
]

# Téléporteurs pour passer au niveau suivant
teleporter_level1_to_2 = pygame.Rect(350, 0, TP_WIDTH, TP_HEIGHT)
teleporter_level2_to_3 = pygame.Rect(350, 0, TP_WIDTH, TP_HEIGHT)

current_level = 1  # Niveau actuel

# Ennemis
enemies_level1 = [
    pygame.Rect(200, SCREEN_HEIGHT - 300 - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT),
    pygame.Rect(400, SCREEN_HEIGHT - 700 - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT),
    pygame.Rect(600, SCREEN_HEIGHT - 1100 - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT),
]

enemies_level2 = [
    pygame.Rect(300, SCREEN_HEIGHT - 500 - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT),
    pygame.Rect(500, SCREEN_HEIGHT - 900 - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT),
    pygame.Rect(700, SCREEN_HEIGHT - 300 - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT),
]

enemies_level3 = [
    pygame.Rect(200, SCREEN_HEIGHT - 200 - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT),
    pygame.Rect(400, SCREEN_HEIGHT - 400 - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT),
    pygame.Rect(600, SCREEN_HEIGHT - 600 - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT),
]

# Variables pour le chrono
font = pygame.font.Font(None, 36)
start_time = pygame.time.get_ticks()

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False

    # Calcul du temps écoulé
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

    # Déplacer le joueur en fonction des touches pressées
    if move_left and player_x > 0:
        player_x -= player_speed
    if move_right and player_x < SCREEN_WIDTH - PLAYER_WIDTH:
        player_x += player_speed

    # Gestion du saut
    if not is_jumping:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            is_jumping = True
            jump_count = JUMP_COUNT  # Réinitialiser le nombre de sauts
    else:
        if jump_count >= -JUMP_COUNT:  # Réduire la hauteur du saut
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False

    # Appliquer la gravité uniquement si le joueur n'est pas sur une plateforme
    on_ground = False
    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    if current_level == 1:
        for platform in platforms_level1[:-1]:  # Ne pas vérifier la collision avec le sol pour le moment
            if player_rect.colliderect(platform):
                on_ground = True
                if player_y < platform.y and player_y + PLAYER_HEIGHT > platform.y:
                    player_y = platform.y - PLAYER_HEIGHT
                break

        # Vérifier la collision avec le sol
        if player_rect.colliderect(platforms_level1[-1]):
            on_ground = True
            if player_y < platforms_level1[-1].y and player_y + PLAYER_HEIGHT > platforms_level1[-1].y:
                player_y = platforms_level1[-1].y - PLAYER_HEIGHT

        # Vérifier si le joueur atteint le téléporteur
        if player_rect.colliderect(teleporter_level1_to_2):
            current_level = 2
            player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
            player_y = SCREEN_HEIGHT - 2 * PLAYER_HEIGHT

    elif current_level == 2:
        for platform in platforms_level2[:-1]:  # Ne pas vérifier la collision avec le sol pour le moment
            if player_rect.colliderect(platform):
                on_ground = True
                if player_y < platform.y and player_y + PLAYER_HEIGHT > platform.y:
                    player_y = platform.y - PLAYER_HEIGHT
                break

        # Vérifier la collision avec le sol
        if player_rect.colliderect(platforms_level2[-1]):
            on_ground = True
            if player_y < platforms_level2[-1].y and player_y + PLAYER_HEIGHT > platforms_level2[-1].y:
                player_y = platforms_level2[-1].y - PLAYER_HEIGHT

        # Vérifier si le joueur atteint le téléporteur
        if player_rect.colliderect(teleporter_level2_to_3):
            current_level = 3
            player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
            player_y = SCREEN_HEIGHT - 2 * PLAYER_HEIGHT

    elif current_level == 3:
        for platform in platforms_level3[:-1]:  # Ne pas vérifier la collision avec le sol pour le moment
            if player_rect.colliderect(platform):
                on_ground = True
                if player_y < platform.y and player_y + PLAYER_HEIGHT > platform.y:
                    player_y = platform.y - PLAYER_HEIGHT
                break

        # Vérifier la collision avec le sol
        if player_rect.colliderect(platforms_level3[-1]):
            on_ground = True
            if player_y < platforms_level3[-1].y and player_y + PLAYER_HEIGHT > platforms_level3[-1].y:
                player_y = platforms_level3[-1].y - PLAYER_HEIGHT

    # Gérer les mouvements des ennemis
    if current_level == 1:
        for enemy in enemies_level1:
            enemy.x += ENEMY_SPEED
            if enemy.x > SCREEN_WIDTH - ENEMY_WIDTH or enemy.x < 0:
                ENEMY_SPEED = -ENEMY_SPEED

            # Vérifier la collision entre le joueur et l'ennemi
            if player_rect.colliderect(enemy):
                # Game over si le joueur entre en collision avec un ennemi
                print("Game Over")
                pygame.quit()
                sys.exit()

    elif current_level == 2:
        for enemy in enemies_level2:
            enemy.x += ENEMY_SPEED
            if enemy.x > SCREEN_WIDTH - ENEMY_WIDTH or enemy.x < 0:
                ENEMY_SPEED = -ENEMY_SPEED

            # Vérifier la collision entre le joueur et l'ennemi
            if player_rect.colliderect(enemy):
                # Game over si le joueur entre en collision avec un ennemi
                print("Game Over")
                pygame.quit()
                sys.exit()

    elif current_level == 3:
        for enemy in enemies_level3:
            enemy.x += ENEMY_SPEED
            if enemy.x > SCREEN_WIDTH - ENEMY_WIDTH or enemy.x < 0:
                ENEMY_SPEED = -ENEMY_SPEED

            # Vérifier la collision entre le joueur et l'ennemi
            if player_rect.colliderect(enemy):
                # Game over si le joueur entre en collision avec un ennemi
                print("Game Over")
                pygame.quit()
                sys.exit()

    if not on_ground and player_y < SCREEN_HEIGHT - PLAYER_HEIGHT:
        player_y += 5

    # Afficher l'arrière-plan
    screen.blit(background_image, (0, 0))

    # Dessiner les plateformes en fonction du niveau actuel
    if current_level == 1:
        for platform in platforms_level1:
            screen.blit(platform_image, platform)

        # Dessiner les ennemis
        for enemy in enemies_level1:
            screen.blit(enemy_image, enemy)

        # Dessiner le joueur
        screen.blit(player_image, (player_x, player_y))

        # Dessiner le téléporteur vers le niveau 2
        pygame.draw.rect(screen, YELLOW, teleporter_level1_to_2)

    elif current_level == 2:
        for platform in platforms_level2:
            screen.blit(platform_image, platform)

        # Dessiner les ennemis
        for enemy in enemies_level2:
            screen.blit(enemy_image, enemy)

        # Dessiner le joueur
        screen.blit(player_image, (player_x, player_y))

        # Dessiner le téléporteur vers le niveau 3
        pygame.draw.rect(screen, YELLOW, teleporter_level2_to_3)

    elif current_level == 3:
        for platform in platforms_level3:
            screen.blit(platform_image, platform)

        # Dessiner les ennemis
        for enemy in enemies_level3:
            screen.blit(enemy_image, enemy)

        # Dessiner le joueur
        screen.blit(player_image, (player_x, player_y))

    # Dessiner le chrono
    time_text = font.render("Time: " + str(elapsed_time), True, BLACK)
    screen.blit(time_text, (10, 10))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôler la fréquence de rafraîchissement
    pygame.time.Clock().tick(30)




