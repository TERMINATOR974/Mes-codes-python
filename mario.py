import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 10

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu de Plateforme Python")

# Position initiale du joueur
player_x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
player_y = SCREEN_HEIGHT - 2 * PLAYER_SIZE

# Vitesse du joueur
player_speed = 5
jump_count = 10
is_jumping = False

# Plateformes
platforms = [
    pygame.Rect(150, SCREEN_HEIGHT - 100, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(300, SCREEN_HEIGHT - 200, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(500, SCREEN_HEIGHT - 300, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(0, SCREEN_HEIGHT - PLATFORM_HEIGHT, SCREEN_WIDTH, PLATFORM_HEIGHT),  # Hitbox pour le sol
]

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

    # Gestion du saut
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10

    # Appliquer la gravité si le joueur n'est pas sur une plateforme
    on_ground = False
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    for platform in platforms:
        if player_rect.colliderect(platform):
            on_ground = True
            if player_y < platform.y and player_y + PLAYER_SIZE > platform.y:
                player_y = platform.y - PLAYER_SIZE
            break

    if not on_ground and player_y < SCREEN_HEIGHT - PLAYER_SIZE:
        player_y += 5

    # Effacer l'écran
    screen.fill(WHITE)

    # Dessiner les plateformes
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)

    # Dessiner le joueur
    pygame.draw.rect(screen, RED, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôler la fréquence de rafraîchissement
    pygame.time.Clock().tick(30)