import pygame
import sys
import random

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000  # Augmenter la hauteur de la fenêtre
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PLAYER_SIZE = 30
GRAVITY = 0.6
JUMP_HEIGHT = 15

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - PLAYER_SIZE  # Initialiser le joueur au bas de l'écran
        self.vel_y = 0

    def jump(self):
        self.vel_y = -JUMP_HEIGHT

    def update(self, walls):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Vérifier les collisions avec les murs
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                # Si le joueur touche un mur par le haut, le placer en dessous du mur
                if self.vel_y > 0:
                    self.rect.bottom = wall.rect.top
                    self.vel_y = 0
                # Si le joueur touche un mur par le bas, le placer au-dessus du mur
                elif self.vel_y < 0:
                    self.rect.top = wall.rect.bottom
                    self.vel_y = 0

        # Limiter le joueur à l'écran en y position
        if self.rect.y >= SCREEN_HEIGHT - PLAYER_SIZE:
            self.rect.y = SCREEN_HEIGHT - PLAYER_SIZE
            self.vel_y = 0

def load_level_2(player):
    walls = pygame.sprite.Group()

    # Ajoutez les nouvelles plateformes pour le deuxième niveau
    for y in range(50, SCREEN_HEIGHT, 100):  # Ajouter plus de plateformes vers le haut
        for x in range(0, SCREEN_WIDTH, random.randint(50, 150)):  # Disposition asymétrique
            walls.add(Wall(x, y, random.randint(50, 150), 20))  # Taille variable des plateformes

    # Ajoutez la nouvelle sortie pour le deuxième niveau
    new_exit_door = Wall(390, 70, 20, 20, color=YELLOW)
    walls.add(new_exit_door)

    # Réinitialisez la position du joueur dans le niveau 2
    player.rect.x = (SCREEN_WIDTH - PLAYER_SIZE) // 2
    player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE

    return walls, player

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=BLACK):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()

    player = Player()
    walls_level1 = pygame.sprite.Group()
    walls_level2 = pygame.sprite.Group()

    # Création des murs du niveau 1
    walls_level1.add(Wall(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 20))  # Ajout de la plateforme marquant le sol
    walls_level1.add(Wall(200, SCREEN_HEIGHT - 150, 400, 20))  # Supprimez les plateformes en bas
   
    walls_level1.add(Wall(400, SCREEN_HEIGHT - 750, 600, 20))
    walls_level1.add(Wall(-200, SCREEN_HEIGHT - 600, 600, 20))
    walls_level1.add(Wall(100, SCREEN_HEIGHT - 450, 600, 20))
    walls_level1.add(Wall(0, SCREEN_HEIGHT - 300, 200, 20))
    walls_level1.add(Wall(600, SCREEN_HEIGHT - 300, 200, 20))
    
    # Plateforme en haut au milieu
    walls_level1.add(Wall(300, 100, 200, 20))

    # Porte de sortie du niveau 1
    exit_door_level1 = Wall(390, 70, 20, 20, color=YELLOW)
    walls_level1.add(exit_door_level1)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(walls_level1)

    current_level_walls = walls_level1
    level2_loaded = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        if pygame.sprite.spritecollide(player, current_level_walls, False):
            for wall in current_level_walls:
                if pygame.sprite.collide_rect(player, wall) and wall.image.get_at((0, 0)) == YELLOW:
                    if not level2_loaded:
                        walls_level2, player = load_level_2(player)
                        all_sprites.add(walls_level2)
                        level2_loaded = True
                        current_level_walls = walls_level2

        all_sprites.update(current_level_walls)

        screen.fill(WHITE)
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()




