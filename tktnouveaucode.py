import pygame
import sys
import random

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PLAYER_SIZE = 30
GRAVITY = 0.6
JUMP_HEIGHT = 15
PLAYER_SPEED = 3

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))
        self.vel_y = 0
        self.jumps_remaining = 2

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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = random.randint(1, 3)

    def update(self, walls):
        self.rect.x += self.speed
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.speed *= -1
                break

def load_level_1():
    walls = pygame.sprite.Group()
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
    return walls

def load_level_2():
    walls = pygame.sprite.Group()
    platform_params = [
        (350, 50, 100, 20),
        (200, 110, 1000, 50),
        (0, 200, 50, 20),
        (500, 650, 300, 20),
        (0, 800, 400, 20),
        (500, 950, 100, 20),
        (200, 400, 200, 20),  # Nouvelle plateforme
        (500, 250, 200, 20)   # Nouvelle plateforme
    ]
    for x, y, width, height in platform_params:
        walls.add(Wall(x, y, width, height))
    return walls

def load_level_3():
    walls = pygame.sprite.Group()
    platform_params = [
        (0, SCREEN_HEIGHT - 50, 800, 50),  # Sol
        (0, 50, 800, 20),
        (200, 150, 400, 20),
        (0, 300, 200, 20),
        (400, 400, 400, 20),
        (0, 550, 200, 20),
        (500, 650, 300, 20),
        (0, 750, 100, 20),
        (0, 900, 100, 50)
    ]
    for x, y, width, height in platform_params:
        walls.add(Wall(x, y, width, height))
    return walls

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()

    player = Player()
    walls_level1 = load_level_1()
    walls_level2 = load_level_2()
    walls_level3 = load_level_3()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(walls_level1)

    current_level_walls = walls_level1

    enemies = pygame.sprite.Group()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_1:
                    all_sprites.remove(walls_level2.sprites())
                    all_sprites.remove(walls_level3.sprites())
                    all_sprites.add(walls_level1.sprites())
                    current_level_walls = walls_level1
                elif event.key == pygame.K_2:
                    all_sprites.remove(walls_level1.sprites())
                    all_sprites.remove(walls_level3.sprites())
                    all_sprites.add(walls_level2.sprites())
                    current_level_walls = walls_level2
                elif event.key == pygame.K_3:
                    all_sprites.remove(walls_level1.sprites())
                    all_sprites.remove(walls_level2.sprites())
                    all_sprites.add(walls_level3.sprites())
                    current_level_walls = walls_level3
                elif event.key == pygame.K_BACKSPACE:  # Revenir au niveau précédent
                    if current_level_walls == walls_level2:
                        all_sprites.remove(walls_level2.sprites())
                        all_sprites.add(walls_level1.sprites())
                        current_level_walls = walls_level1
                    elif current_level_walls == walls_level3:
                        all_sprites.remove(walls_level3.sprites())
                        all_sprites.add(walls_level2.sprites())
                        current_level_walls = walls_level2

        if player.rect.top >= SCREEN_HEIGHT and current_level_walls == walls_level2:
            current_level_walls = walls_level1
        elif player.rect.top >= SCREEN_HEIGHT and current_level_walls == walls_level3:
            current_level_walls = walls_level2

        if player.update(current_level_walls):
            if current_level_walls == walls_level1:
                current_level_walls = walls_level2
            elif current_level_walls == walls_level2:
                current_level_walls = walls_level3

        if current_level_walls == walls_level2 and len(enemies) < 2:
            for platform in walls_level2:
                if platform.rect.y == 400 or platform.rect.y == 250:
                    enemy = Enemy(platform.rect.centerx, platform.rect.y - 30)
                    enemies.add(enemy)
        elif current_level_walls == walls_level3 and len(enemies) < 2:
            for platform in walls_level3:
                if platform.rect.y == 300 or platform.rect.y == 550:
                    enemy = Enemy(platform.rect.centerx, platform.rect.y - 30)
                    enemies.add(enemy)

        for enemy in enemies:
            enemy.update(current_level_walls)

        all_sprites.update()

        screen.fill(WHITE)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()



