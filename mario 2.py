import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 40  # Largeur du personnage ajustée pour une meilleure hitbox
PLAYER_HEIGHT = 60  # Hauteur du personnage ajustée pour une meilleure hitbox
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20  # Hauteur des plateformes
PLATFORM_GAP = 150  # Espacement vertical entre les plateformes
TP_WIDTH = 50
TP_HEIGHT = 20

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

# Position initiale du joueur
player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
player_y = SCREEN_HEIGHT - 2 * PLAYER_HEIGHT

# Vitesse du joueur
player_speed = 5
jump_count = 7  # Réduire le nombre de sauts
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
    pygame.Rect(0, SCREEN_HEIGHT - PLATFORM_HEIGHT, SCREEN_WIDTH, PLATFORM_HEIGHT),  # Hitbox pour le sol
    pygame.Rect(350, 150, PLATFORM_WIDTH, PLATFORM_HEIGHT)  # Nouvelle plateforme
]

platforms_level2 = [
    pygame.Rect(350, 50, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(200, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(550, 350, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(650, 650, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(250, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(600, 950, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(0, SCREEN_HEIGHT - PLATFORM_HEIGHT, SCREEN_WIDTH, PLATFORM_HEIGHT),  # Hitbox pour le sol
    pygame.Rect(350, 450, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
    pygame.Rect(400, 250, PLATFORM_WIDTH, PLATFORM_HEIGHT),  # Nouvelle plateforme
]

# Téléporteur pour passer au niveau suivant
teleporter = pygame.Rect(350, 0, TP_WIDTH, TP_HEIGHT)

current_level = 1  # Niveau actuel

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
            jump_count = 7  # Réinitialiser le nombre de sauts
    else:
        if jump_count >= -7:  # Réduire la hauteur du saut
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
        if player_rect.colliderect(teleporter):
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

    if not on_ground and player_y < SCREEN_HEIGHT - PLAYER_HEIGHT:
        player_y += 5

    # Effacer l'écran
    screen.fill(WHITE)

    # Dessiner les plateformes en fonction du niveau actuel
    if current_level == 1:
        # Supprimer les plateformes qui sont en dehors du cadre du niveau 1
        platforms_level1 = [platform for platform in platforms_level1 if platform.y + PLATFORM_HEIGHT >= 0]
        for platform in platforms_level1:
            pygame.draw.rect(screen, GREEN, platform)

        # Dessiner le téléporteur vers le niveau 2
        pygame.draw.rect(screen, YELLOW, teleporter)

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

        # Dessiner les plateformes du niveau 2
        for platform in platforms_level2:
            pygame.draw.rect(screen, GREEN, platform)

    # Dessiner le joueur
    pygame.draw.rect(screen, RED, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôler la fréquence de rafraîchissement
    pygame.time.Clock().tick(30)

