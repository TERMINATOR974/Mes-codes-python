# main.py

import pygame
import sys

# Définir les constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLATFORM_WIDTH = 80
PLATFORM_HEIGHT = 10
ENEMY_WIDTH = 30
ENEMY_HEIGHT = 30
PLAYER_SPEED = 8
JUMP_COUNT = 8
ENEMY_SPEED = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Player:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT - 2 * PLAYER_HEIGHT
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.jump_count = JUMP_COUNT
        self.is_jumping = False

    def move(self, move_left, move_right):
        if move_left and self.x > 0:
            self.x -= self.speed
        if move_right and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_count = JUMP_COUNT

class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLATFORM_WIDTH
        self.height = PLATFORM_HEIGHT

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.speed = ENEMY_SPEED

    def move(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH - self.width or self.x < 0:
            self.speed = -self.speed

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jeu de Plateforme Python")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.start_time = pygame.time.get_ticks()
        self.current_level = 1
        self.player = Player()
        self.platforms = []
        self.enemies = []
        self.load_level(self.current_level)

    def load_level(self, level):
        if level == 1:
            self.platforms = [
                Platform(150, SCREEN_HEIGHT - 100),
                Platform(300, SCREEN_HEIGHT - 250),
                # Ajouter d'autres plateformes
                Platform(0, SCREEN_HEIGHT - PLATFORM_HEIGHT)  # Ajout du sol
            ]
            self.enemies = [
                Enemy(200, SCREEN_HEIGHT - 300 - ENEMY_HEIGHT),
                Enemy(400, SCREEN_HEIGHT - 700 - ENEMY_HEIGHT),
                # Ajouter d'autres ennemis
            ]

    def run(self):
        move_left = False
        move_right = False

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
                    elif event.key == pygame.K_SPACE:
                        self.player.jump()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        move_left = False
                    elif event.key == pygame.K_RIGHT:
                        move_right = False

            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000

            self.player.move(move_left, move_right)
            if self.player.is_jumping:
                self.player.jump()

            for enemy in self.enemies:
                enemy.move()

            self.screen.fill(WHITE)

            for platform in self.platforms:
                pygame.draw.rect(self.screen, BLACK, (platform.x, platform.y, platform.width, platform.height))

            for enemy in self.enemies:
                pygame.draw.rect(self.screen, RED, (enemy.x, enemy.y, enemy.width, enemy.height))

            pygame.draw.rect(self.screen, BLUE, (self.player.x, self.player.y, self.player.width, self.player.height))

            time_text = self.font.render("Time: " + str(elapsed_time), True, BLACK)
            self.screen.blit(time_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()



