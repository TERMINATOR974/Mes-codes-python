import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLATFORM_WIDTH = 80
PLATFORM_HEIGHT = 10
PLATFORM_GAP = 150
TP_WIDTH = 50
TP_HEIGHT = 20
ENEMY_WIDTH = 30
ENEMY_HEIGHT = 30
WALL_WIDTH = 20

# Vitesse et saut du joueur
PLAYER_SPEED = 8
JUMP_COUNT = 8
GRAVITY = 0.5
SLIDE_SPEED = 3
ENEMY_SPEED = 3

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
player_x = 50
player_y = SCREEN_HEIGHT - 2 * PLAYER_HEIGHT

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
    pygame.Rect(250, 250, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(0, SCREEN_HEIGHT - PLATFORM_HEIGHT, SCREEN_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(350, 150, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(450, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(250, 450, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(550, 600, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(100, 750, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(650, 900, PLATFORM_WIDTH, PLATFORM_HEIGHT),
]

platforms_level2 = [
    pygame.Rect(350, 100, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(200, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(550, 350, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(650, 650, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(250, 800, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(600, 950, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(0, SCREEN_HEIGHT - PLATFORM_HEIGHT, SCREEN_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(350, 450, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(400, 250, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(150, 150, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(450, 600, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(200, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(500, 350, PLATFORM_WIDTH, PLATFORM_HEIGHT),
]

platforms_level3 = [
    pygame.Rect(200, 100, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(500, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(300, 300, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(100, 400, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(600, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(400, 600, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(0, SCREEN_HEIGHT - PLATFORM_HEIGHT, SCREEN_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(350, 350, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(150, 550, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(550, 250, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(450, 450, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(250, 150, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(650, 650, PLATFORM_WIDTH, PLATFORM_HEIGHT),
]

# Téléporteurs pour passer au niveau suivant
teleporter_level1_to_2 = pygame.Rect(350, 0, TP_WIDTH, TP_HEIGHT)
teleporter_level2_to_3 = pygame.Rect(350, 0, TP_WIDTH, TP_HEIGHT)

current_level = 1

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

    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

    if move_left and player_x > 0:
        player_x -= player_speed
    if move_right and player_x < SCREEN_WIDTH - PLAYER_WIDTH:
        player_x += player_speed

    if not is_jumping:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            is_jumping = True
            jump_count = JUMP_COUNT
    else:
        if jump_count >= -JUMP_COUNT:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False

    on_ground = False
    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    if current_level == 1:
        for platform in platforms_level1[:-1]:
            if player_rect.colliderect(platform):
                on_ground = True
                if player_y + PLAYER_HEIGHT <= platform.y + 10:
                    player_y = platform.y - PLAYER_HEIGHT
                break

        if player_rect.colliderect(platforms_level1[-1]):
            on_ground = True
            if player_y < platforms_level1[-1].y and player_y + PLAYER_HEIGHT > platforms_level1[-1].y:
                player_y = platforms_level1[-1].y - PLAYER_HEIGHT

        if player_rect.colliderect(teleporter_level1_to_2):
            current_level = 2
            player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
            player_y = SCREEN_HEIGHT - 2 * PLAYER_HEIGHT

    elif current_level == 2:
        for platform in platforms_level2[:-1]:
            if player_rect.colliderect(platform):
                on_ground = True
                if player_y + PLAYER_HEIGHT <= platform.y + 10:
                    player_y = platform.y - PLAYER_HEIGHT
                break

        if player_rect.colliderect(platforms_level2[-1]):
            on_ground = True
            if player_y < platforms_level2[-1].y and player_y + PLAYER_HEIGHT > platforms_level2[-1].y:
                player_y = platforms_level2[-1].y - PLAYER_HEIGHT

        if player_rect.colliderect(teleporter_level2_to_3):
            current_level = 3
            player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
            player_y = SCREEN_HEIGHT - 2 * PLAYER_HEIGHT

    elif current_level == 3:
        for platform in platforms_level3[:-1]:
            if player_rect.colliderect(platform):
                on_ground = True
                if player_y + PLAYER_HEIGHT <= platform.y + 10:
                    player_y = platform.y - PLAYER_HEIGHT
                break

        if player_rect.colliderect(platforms_level3[-1]):
            on_ground = True
            if player_y < platforms_level3[-1].y and player_y + PLAYER_HEIGHT > platforms_level3[-1].y:
                player_y = platforms_level3[-1].y - PLAYER_HEIGHT

    if not on_ground and player_y < SCREEN_HEIGHT - PLAYER_HEIGHT:
        player_y += 5

    screen.fill(WHITE)

    if current_level == 1:
        for platform in platforms_level1:
            pygame.draw.rect(screen, BLACK, platform)

        for enemy in enemies_level1:
            pygame.draw.rect(screen, RED, enemy)

        pygame.draw.rect(screen, YELLOW, teleporter_level1_to_2)

    elif current_level == 2:
        for platform in platforms_level2:
            pygame.draw.rect(screen, BLACK, platform)

        for enemy in enemies_level2:
            pygame.draw.rect(screen, RED, enemy)

        pygame.draw.rect(screen, YELLOW, teleporter_level2_to_3)

    elif current_level == 3:
        for platform in platforms_level3:
            pygame.draw.rect(screen, BLACK, platform)

        for enemy in enemies_level3:
            pygame.draw.rect(screen, RED, enemy)

    screen.blit(player_image, (player_x, player_y))

    time_text = font.render("Time: " + str(elapsed_time), True, BLACK)
    screen.blit(time_text, (10, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(30)
