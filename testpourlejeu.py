import pygame
import sys
import random

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
PLAYER_SPEED = 6
JUMP_VELOCITY = -10
GRAVITY = 0.4
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

# Charger les images
player_image = pygame.image.load('perso1.png').convert_alpha()
platform_image = pygame.image.load('longbrick.png').convert_alpha()
enemy_image = pygame.image.load('fonddebrique.png').convert_alpha()

# Redimensionner les images pour correspondre aux dimensions requises
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
platform_image = pygame.transform.scale(platform_image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_WIDTH, ENEMY_HEIGHT))


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def jump(self):
        if self.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.velocity_y = JUMP_VELOCITY

    def apply_gravity(self):
        if self.rect.y < SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.velocity_y += GRAVITY

    def draw(self):
        screen.blit(player_image, (self.rect.x, self.rect.y))


class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)

    def move(self):
        self.rect.x -= ENEMY_SPEED

    def draw(self):
        screen.blit(enemy_image, (self.rect.x, self.rect.y))


# Position initiale du joueur
player = Player(50, SCREEN_HEIGHT - 2 * PLAYER_HEIGHT)

# Plateformes
platforms = [
    pygame.Rect(150, SCREEN_HEIGHT - 100, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(300, SCREEN_HEIGHT - 250, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(100, SCREEN_HEIGHT - 400, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(500, SCREEN_HEIGHT - 550, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(300, SCREEN_HEIGHT - 700, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(500, SCREEN_HEIGHT - 850, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(200, SCREEN_HEIGHT - 1000, PLATFORM_WIDTH, PLATFORM_HEIGHT),
    pygame.Rect(600, SCREEN_HEIGHT - 1150, PLATFORM_WIDTH, PLATFORM_HEIGHT),
]

# Ennemis
enemies = [
    Enemy(200, SCREEN_HEIGHT - 300 - ENEMY_HEIGHT),
    Enemy(400, SCREEN_HEIGHT - 700 - ENEMY_HEIGHT),
    Enemy(600, SCREEN_HEIGHT - 1100 - ENEMY_HEIGHT),
]

# Variables pour le chrono
font = pygame.font.Font(None, 36)
start_time = pygame.time.get_ticks()


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()


def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


# Boucle principale du jeu
while True:
    handle_events()

    # Mouvement du joueur
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.velocity_x = -PLAYER_SPEED
    elif keys[pygame.K_RIGHT]:
        player.velocity_x = PLAYER_SPEED
    else:
        player.velocity_x = 0

    # Appliquer la gravité
    player.apply_gravity()

    # Mettre à jour la position du joueur
    player.update()

    # Détection de collision avec les plateformes
    on_ground = False
    for platform in platforms:
        if player.rect.colliderect(platform):
            if player.velocity_y > 0:
                player.rect.bottom = platform.top
                player.velocity_y = 0
                on_ground = True
            elif player.velocity_y < 0:
                player.rect.top = platform.bottom
                player.velocity_y = 0

    # Détection de collision avec les ennemis
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            print("Game Over")
            pygame.quit()
            sys.exit()

    # Déplacer les ennemis
    for enemy in enemies:
        enemy.move()

    # Effacer l'écran
    screen.fill(WHITE)

    # Dessiner les plateformes
    for platform in platforms:
        screen.blit(platform_image, platform)

    # Dessiner les ennemis
    for enemy in enemies:
        enemy.draw()

    # Dessiner le joueur
    player.draw()

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôler la fréquence de rafraîchissement
    pygame.time.Clock().tick(60)


