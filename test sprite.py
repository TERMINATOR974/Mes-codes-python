import pygame
from pygame.locals import *
import sys
import random

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class SardJump:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.player_width = 50
        self.player_height = 50
        self.plateform_width = 100
        self.plateform_height = 20

        self.cameray = 0
        self.playerx = 400
        self.playery = 400
        self.xmovement = 0
        self.jump = 0
        self.direction = 0
        self.gravity = 0

        self.platforms = [[400, 500]]
        self.score = 0

    def run(self):
        clock = pygame.time.Clock()
        self.generatePlatforms()
        while True:
            self.screen.fill(WHITE)
            font = pygame.font.SysFont(None, 30)
            text = font.render("Score : " + str(self.score), False, (0, 0, 0))
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

            self.updatePlayer()
            self.drawPlatforms()
            self.updatePlatforms()
            self.screen.blit(text, (550, 50))
            pygame.display.flip()
            pygame.display.set_caption("SardJump")

    def updatePlayer(self):
        if self.playerx > 850:
            self.playerx = -50
        elif self.playerx < -50:
            self.playerx = 850
        self.playerx += self.xmovement
        if self.playery - self.cameray <= 200:
            self.cameray -= 10

        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.xmovement < 10:
                self.xmovement += 1
                self.direction = 0
        elif key[K_LEFT]:
            if self.xmovement > -10:
                self.xmovement -= 1
                self.direction = 1

        if not self.jump:
            self.playery += self.gravity
            self.gravity += 1
        elif self.jump:
            self.playery -= self.jump
            self.jump -= 1

    def generatePlatforms(self):
        y = 700
        while y > -100:
            x = random.randint(0, 900)
            self.platforms.append((x, y))
            y -= 100

    def drawPlatforms(self):
        for plat in self.platforms:
            pygame.draw.rect(self.screen, RED, [plat[0], plat[1] - self.cameray, self.plateform_width, self.plateform_height])

    def updatePlatforms(self):
        for p in self.platforms:
            player_rect = pygame.Rect(self.playerx, self.playery, self.player_width, self.player_height)
            platform_rect = pygame.Rect(p[0], p[1] - self.cameray, self.plateform_width, self.plateform_height)
            if player_rect.colliderect(platform_rect) and self.gravity and self.playery < (p[1] - self.cameray):
                self.jump = 15
                self.gravity = 0
        if self.playery - self.cameray <= 200:
            self.cameray -= 10
            self.score += 1

if __name__ == "__main__":
    game = SardJump()
    game.run()


