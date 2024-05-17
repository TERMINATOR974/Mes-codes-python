import pygame
import sys
import random

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PLAYER_SIZE = 30
ENEMY_SIZE = 20
HEALTHBAR_WIDTH = 100
HEALTHBAR_HEIGHT = 10
GRAVITY = 0.6
JUMP_HEIGHT = 15
ENEMY_SPEED = 8
ENEMY_DAMAGE = 5  # Nouveau paramètre pour les dégâts des ennemis

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
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
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.jump()

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

        if self.rect.y >= SCREEN_HEIGHT - PLAYER_SIZE:
            self.rect.y = SCREEN_HEIGHT - PLAYER_SIZE
            self.vel_y = 0
            self.jumps_remaining = 2

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = ENEMY_SPEED
        self.vel_y = ENEMY_SPEED

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.vel_x = -self.vel_x
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.vel_y = -self.vel_y

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=BLACK):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class ExitDoor(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, destination_level, color=YELLOW):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.destination_level = destination_level

class HealthSquare(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def load_level_1():
    walls = pygame.sprite.Group()
    walls.add(Wall(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 20))
    walls.add(Wall(200, SCREEN_HEIGHT - 150, 400, 20))
    walls.add(Wall(400, SCREEN_HEIGHT - 750, 600, 20))
    walls.add(Wall(-200, SCREEN_HEIGHT - 600, 600, 20))
    walls.add(Wall(100, SCREEN_HEIGHT - 450, 600, 20))
    walls.add(Wall(0, SCREEN_HEIGHT - 300, 200, 20))
    walls.add(Wall(600, SCREEN_HEIGHT - 300, 200, 20))
    walls.add(Wall(300, 100, 200, 20))
    exit_door_level1 = ExitDoor(390, 70, 20, 20, 2)
    walls.add(exit_door_level1)
    health_squares = pygame.sprite.Group()
    health_squares.add(HealthSquare(200, SCREEN_HEIGHT - 200))
    health_squares.add(HealthSquare(600, SCREEN_HEIGHT - 200))
    enemies = pygame.sprite.Group()
    enemies.add(Enemy(300, SCREEN_HEIGHT - 100))
    enemies.add(Enemy(500, SCREEN_HEIGHT - 100))
    return walls, health_squares, enemies

def load_level_2():
    walls = pygame.sprite.Group()
    walls.add(Wall(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 20))
    walls.add(Wall(200, SCREEN_HEIGHT - 150, 400, 20))
    walls.add(Wall(0, SCREEN_HEIGHT - 300, 200, 20))
    walls.add(Wall(600, SCREEN_HEIGHT - 300, 200, 20))
    walls.add(Wall(300, 350, 200, 20))  # Nouvelle plateforme au milieu du niveau 2
    walls.add(Wall(0, 50, 800, 20))
    exit_door_level2 = ExitDoor(750, 80, 20, 20, 3)
    walls.add(exit_door_level2)
    health_squares = pygame.sprite.Group()
    health_squares.add(HealthSquare(200, SCREEN_HEIGHT - 200))
    health_squares.add(HealthSquare(600, SCREEN_HEIGHT - 200))
    enemies = pygame.sprite.Group()
    enemies.add(Enemy(100, SCREEN_HEIGHT - 100))
    enemies.add(Enemy(400, SCREEN_HEIGHT - 400))
    enemies.add(Enemy(300, SCREEN_HEIGHT - 300))
    return walls, health_squares, enemies

def load_level_3():
    walls = pygame.sprite.Group()
    platform_params = [
        (0, 50, 800, 20),
        (200, 150, 400, 20),
        (0, 300, 200, 20),
        (400, 400, 400, 20),
        (0, 550, 200, 20),
        (500, 650, 300, 20),
        (0, 750, 500, 20),
        (0, 900, 600, 50)
    ]
    for x, y, width, height in platform_params:
        walls.add(Wall(x, y, width, height))
    exit_door_level3 = ExitDoor(750, 80, 20, 20, 1)
    walls.add(exit_door_level3)
    health_squares = pygame.sprite.Group()
    health_squares.add(HealthSquare(200, SCREEN_HEIGHT - 200))
    health_squares.add(HealthSquare(600, SCREEN_HEIGHT - 200))
    enemies = pygame.sprite.Group()
    enemies.add(Enemy(300, SCREEN_HEIGHT - 200))
    enemies.add(Enemy(500, SCREEN_HEIGHT - 400))
    enemies.add(Enemy(100, SCREEN_HEIGHT - 400))
    enemies.add(Enemy(200, SCREEN_HEIGHT - 200))
    return walls, health_squares, enemies

def start_screen(screen):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 106)
    text = font.render("CUBY ADVENTURE", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

    button_font = pygame.font.Font(None, 34)
    play_text = button_font.render("Play", True, WHITE)
    play_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.draw.rect(screen, RED, play_rect, border_radius=5)
    screen.blit(play_text, play_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return True

def end_screen(screen):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text = font.render("Jeu en cours de création, bientôt plus de contenus :)", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()

    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    if not start_screen(screen):
        pygame.quit()
        sys.exit()

    current_level = 1
    current_level_walls, health_squares, enemies = load_level_1()
    all_sprites.add(current_level_walls.sprites())
    all_sprites.add(health_squares.sprites())
    all_sprites.add(enemies.sprites())
    player.rect.x = SCREEN_WIDTH // 2
    player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_1:
                    current_level = 1
                    current_level_walls, health_squares, enemies = load_level_1()
                    all_sprites.empty()
                    all_sprites.add(player)
                    all_sprites.add(current_level_walls.sprites())
                    all_sprites.add(health_squares.sprites())
                    all_sprites.add(enemies.sprites())
                    player.rect.x = SCREEN_WIDTH // 2
                    player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE
                elif event.key == pygame.K_2:
                    current_level = 2
                    current_level_walls, health_squares, enemies = load_level_2()
                    all_sprites.empty()
                    all_sprites.add(player)
                    all_sprites.add(current_level_walls.sprites())
                    all_sprites.add(health_squares.sprites())
                    all_sprites.add(enemies.sprites())
                    player.rect.x = SCREEN_WIDTH // 2
                    player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE
                elif event.key == pygame.K_3:
                    current_level = 3
                    current_level_walls, health_squares, enemies = load_level_3()
                    all_sprites.empty()
                    all_sprites.add(player)
                    all_sprites.add(current_level_walls.sprites())
                    all_sprites.add(health_squares.sprites())
                    all_sprites.add(enemies.sprites())
                    player.rect.x = SCREEN_WIDTH // 2
                    player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE

        player.update(current_level_walls)
        enemies.update()

        if pygame.sprite.spritecollide(player, enemies, False):
            player.health -= ENEMY_DAMAGE

        if pygame.sprite.spritecollide(player, health_squares, True):
            player.health = min(player.health + 20, player.max_health)

        for wall in current_level_walls:
            if pygame.sprite.collide_rect(player, wall) and isinstance(wall, ExitDoor):
                current_level = wall.destination_level
                if current_level == 1:
                    current_level_walls, health_squares, enemies = load_level_1()
                elif current_level == 2:
                    current_level_walls, health_squares, enemies = load_level_2()
                elif current_level == 3:
                    current_level_walls, health_squares, enemies = load_level_3()
                all_sprites.empty()
                all_sprites.add(player)
                all_sprites.add(current_level_walls.sprites())
                all_sprites.add(health_squares.sprites())
                all_sprites.add(enemies.sprites())
                player.rect.x = SCREEN_WIDTH // 2
                player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE

        screen.fill(WHITE)
        all_sprites.draw(screen)

        pygame.draw.rect(screen, RED, (10, 10, player.health, HEALTHBAR_HEIGHT))
        pygame.draw.rect(screen, BLACK, (10, 10, HEALTHBAR_WIDTH, HEALTHBAR_HEIGHT), 2)

        pygame.display.flip()
        clock.tick(60)

        if current_level == 3:
            end_screen(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
