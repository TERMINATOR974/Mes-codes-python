import pygame
import sys
import random
import math

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600  # Changer les dimensions de l'écran selon vos préférences
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)  # Couleur de l'ennemi
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # Couleur des pièces
PLAYER_SIZE = 30
GRAVITY = 0.6
JUMP_HEIGHT = 15
PLAYER_SPEED = 5  # Augmentation de la vitesse du joueur
CAMERA_SPEED = 5  # Vitesse de déplacement de la caméra

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))
        self.vel_y = 0
        self.jumps_remaining = 2
        self.health = 100
        self.max_health = 100

    def jump(self):
        if self.jumps_remaining > 0:
            self.vel_y = -JUMP_HEIGHT
            self.jumps_remaining -= 1

    def update(self, walls):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if self.vel_y > 0:
                    self.rect.bottom = wall.rect.top
                    self.vel_y = 0
                    self.jumps_remaining = 2
                elif self.vel_y < 0:
                    self.rect.top = wall.rect.bottom
                    self.vel_y = 0

        if self.rect.top <= 0:
            return True
        return False

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(topleft=(x, y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2

    def update(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx /= distance
            dy /= distance

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        if self.rect.colliderect(player.rect):
            if dx > 0:
                player.rect.left = self.rect.right
            elif dx < 0:
                player.rect.right = self.rect.left
            if dy > 0:
                player.rect.top = self.rect.bottom
            elif dy < 0:
                player.rect.bottom = self.rect.top

def load_level_1():
    walls = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    platform_params = [
        (0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 20),
        (200, SCREEN_HEIGHT - 150, 400, 20),
        (400, SCREEN_HEIGHT - 750, 600, 20),
        (-200, SCREEN_HEIGHT - 600, 600, 20),
        (100, SCREEN_HEIGHT - 450, 600, 20),
        (0, SCREEN_HEIGHT - 300, 200, 20),
        (600, SCREEN_HEIGHT - 300, 200, 20),
        (300, 100, 200, 20)
    ]
    for x, y, width, height in platform_params:
        walls.add(Wall(x, y, width, height))
        if random.randint(1, 10) == 1:
            coins.add(Coin(x + random.randint(10, width - 10), y - 20))
    return walls, coins

def load_level_2():
    walls = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    platform_params = [
        (200, 120, 1000, 50),
        (0, 300, 50, 20),
        (500, 650, 300, 20),
        (0, 800, 400, 20),
        (500, 950, 100, 20),
        (300, SCREEN_HEIGHT//2, 200, 20)
    ]
    for x, y, width, height in platform_params:
        walls.add(Wall(x, y, width, height))
        if random.randint(1, 10) == 1:
            coins.add(Coin(x + random.randint(10, width - 10), y - 20))
    return walls, coins, pygame.sprite.Group(Enemy(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Créer l'ennemi uniquement pour ce niveau

def load_level_3():
    walls = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    platform_params = [
        (500, 150, 400, 20),
        (0, 300, 200, 20),
        (400, 400, 400, 20),
        (0, 550, 200, 20),
        (500, 650, 300, 20),
        (250, 750, 100, 20),
        (100, 900, 150, 50)
    ]
    for x, y, width, height in platform_params:
        walls.add(Wall(x, y, width, height))
        if random.randint(1, 10) == 1:
            coins.add(Coin(x + random.randint(10, width - 10), y - 20))
    return walls, coins

def draw_level_name(screen, level_number):
    font = pygame.font.SysFont(None, 36)
    level_name = f"Level {level_number}"
    text = font.render(level_name, True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(text, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()

    player = Player()
    walls_level1, coins_level1 = load_level_1()
    walls_level2, coins_level2, enemies_level2 = load_level_2()
    walls_level3, coins_level3 = load_level_3()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(walls_level1)
    all_sprites.add(coins_level1)

    last_player_x = None

    score = 0

    current_level_walls = walls_level1
    current_level_coins = coins_level1

    camera_y = 0  # Position verticale initiale de la caméra

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_1:
                    all_sprites.remove(walls_level2)
                    all_sprites.remove(walls_level3)
                    all_sprites.remove(coins_level2)
                    all_sprites.remove(coins_level3)
                    all_sprites.remove(enemies_level2)
                    all_sprites.add(walls_level1)
                    all_sprites.add(coins_level1)
                    current_level_walls = walls_level1
                    current_level_coins = coins_level1
                    if last_player_x is not None:
                        player.rect.midbottom = (last_player_x, SCREEN_HEIGHT - 10)
                elif event.key == pygame.K_2:
                    all_sprites.remove(walls_level1)
                    all_sprites.remove(walls_level3)
                    all_sprites.remove(coins_level1)
                    all_sprites.remove(coins_level3)
                    all_sprites.add(walls_level2)
                    all_sprites.add(coins_level2)
                    all_sprites.add(enemies_level2)
                    current_level_walls = walls_level2
                    current_level_coins = coins_level2
                    if last_player_x is not None:
                        player.rect.midbottom = (last_player_x, SCREEN_HEIGHT - 10)
                elif event.key == pygame.K_3:
                    all_sprites.remove(walls_level1)
                    all_sprites.remove(walls_level2)
                    all_sprites.remove(coins_level1)
                    all_sprites.remove(coins_level2)
                    all_sprites.remove(enemies_level2)
                    all_sprites.add(walls_level3)
                    all_sprites.add(coins_level3)
                    current_level_walls = walls_level3
                    current_level_coins = coins_level3
                    if last_player_x is not None:
                        player.rect.midbottom = (last_player_x, SCREEN_HEIGHT - 10)

        collected_coins = pygame.sprite.spritecollide(player, current_level_coins, True)
        score += len(collected_coins)

        if current_level_walls == walls_level2:
            enemies_level2.update(player)

            if pygame.sprite.spritecollide(player, enemies_level2, False):
                pass  # Gérer la collision avec l'ennemi ici

        screen.fill(WHITE)

        # Déplacer la caméra verticalement pour suivre le joueur
        if player.rect.top <= SCREEN_HEIGHT // 4:  # Si le joueur atteint le quart supérieur de l'écran
            camera_y -= CAMERA_SPEED
        elif player.rect.bottom >= SCREEN_HEIGHT * 3 // 4:  # Si le joueur atteint le quart inférieur de l'écran
            camera_y += CAMERA_SPEED

        # Ajuster les positions des sprites en fonction de camera_y
        for sprite in all_sprites:
            sprite.rect.y += camera_y

        all_sprites.draw(screen)
        draw_level_name(screen, 1 if current_level_walls == walls_level1 else (2 if current_level_walls == walls_level2 else 3))
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

        # Ajuster également la position du joueur par rapport à camera_y
        player.rect.y += camera_y

        player.update(current_level_walls)

        clock.tick(60)

        last_player_x = player.rect.centerx

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
