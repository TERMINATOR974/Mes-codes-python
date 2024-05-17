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
GREEN = (0, 255, 0)  # Couleur pour la barre de vie
PLAYER_SIZE = 30
GRAVITY = 0.6
JUMP_HEIGHT = 15

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel_y = 0
        self.jumps_remaining = 2  # Nombre de sauts restants (1 saut simple + 1 double saut)
        self.health = 100  # Points de vie du joueur
        self.max_health = 100  # Points de vie maximum du joueur

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

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Vérifier les collisions avec les murs
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                # Si le joueur touche un mur par le haut, le placer en dessous du mur
                if self.vel_y > 0:
                    self.rect.bottom = wall.rect.top
                    self.vel_y = 0
                    self.jumps_remaining = 2  # Réinitialiser les sauts lorsque le joueur touche le sol
                # Si le joueur touche un mur par le bas, le placer au-dessus du mur
                elif self.vel_y < 0:
                    self.rect.top = wall.rect.bottom
                    self.vel_y = 0

        # Limiter le joueur à l'écran en y position
        if self.rect.y >= SCREEN_HEIGHT - PLAYER_SIZE:
            self.rect.y = SCREEN_HEIGHT - PLAYER_SIZE
            self.vel_y = 0
            self.jumps_remaining = 2  # Réinitialiser les sauts lorsque le joueur touche le sol

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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=BLACK):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = random.choice([-2, 2])

    def update(self, walls):
        self.rect.x += self.vel_x

        # Vérifier les collisions avec les murs
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if self.vel_x > 0:
                    self.rect.right = wall.rect.left
                else:
                    self.rect.left = wall.rect.right
                self.vel_x *= -1

def load_level_1(player):
    walls = pygame.sprite.Group()

    # Création des murs du niveau 1
    walls.add(Wall(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 20))  # Ajout de la plateforme marquant le sol
    walls.add(Wall(200, SCREEN_HEIGHT - 150, 400, 20))  # Supprimez les plateformes en bas
    walls.add(Wall(400, SCREEN_HEIGHT - 750, 600, 20))
    walls.add(Wall(-200, SCREEN_HEIGHT - 600, 600, 20))
    walls.add(Wall(100, SCREEN_HEIGHT - 450, 600, 20))
    walls.add(Wall(0, SCREEN_HEIGHT - 300, 200, 20))
    walls.add(Wall(600, SCREEN_HEIGHT - 300, 200, 20))

    # Plateforme en haut au milieu
    walls.add(Wall(300, 100, 200, 20))

    # Porte de sortie du niveau 1
    exit_door_level1 = ExitDoor(390, 70, 20, 20, 2)
    walls.add(exit_door_level1)

    # Spawn du joueur
    player.rect.x = SCREEN_WIDTH // 2
    player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE

    return walls

def load_level_2(player):
    walls = pygame.sprite.Group()

    # Définir les paramètres pour la génération des plateformes du niveau 2
    platform_params = [
        (0, 50, 800, 20),  # Plateforme de départ
        (200, 110, 1000, 50),  # Plateforme à droite 2
        (0, 200, 50, 20),  # Plateforme à gauche
        (0, 500, 400, 20),  # Plateforme à gauche
        (500, 650, 300, 20),  # Plateforme à droite
        (0, 800, 400, 20),  # Plateforme au milieu inférieure
        (0, 950, 800, 50)  # Plateforme en bas
    ]

    # Ajouter les plateformes en fonction des paramètres
    for x, y, width, height in platform_params:
        walls.add(Wall(x, y, width, height))

    # Ajouter la sortie
    new_exit_door = ExitDoor(750, 80, 20, 20, 3)
    walls.add(new_exit_door)

    # Spawn du joueur
    player.rect.x = SCREEN_WIDTH // 2
    player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE

    return walls

def load_level_3(player):
    walls = pygame.sprite.Group()

    # Définir les paramètres pour la génération des plateformes du niveau 3
    platform_params = [
        (0, 50, 800, 20),   # Plateforme de départ
        (200, 150, 400, 20),  # Plateforme à droite
        (0, 300, 200, 20),  # Plateforme à gauche
        (400, 400, 400, 20),  # Plateforme à droite
        (0, 550, 200, 20),  # Plateforme à gauche
        (500, 650, 300, 20),  # Plateforme à droite
        (0, 750, 800, 20),   # Plateforme au milieu inférieure
        (0, 900, 800, 50)    # Plateforme en bas
    ]

    # Ajouter les plateformes en fonction des paramètres
    for x, y, width, height in platform_params:
        walls.add(Wall(x, y, width, height))

    # Ajouter la sortie vers le niveau 4
    new_exit_door = ExitDoor(750, 80, 20, 20, 4)
    walls.add(new_exit_door)

    # Spawn du joueur
    player.rect.x = SCREEN_WIDTH // 2
    player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE

    return walls

def load_level_4(player):
    walls = pygame.sprite.Group()

    # Plateformes horizontales
    horizontal_platforms = [
        (0, SCREEN_HEIGHT - 50, 400, 20),
        (500, SCREEN_HEIGHT - 150, 300, 20),
        (200, SCREEN_HEIGHT - 300, 400, 20),
        (0, SCREEN_HEIGHT - 500, 300, 20),
        (500, SCREEN_HEIGHT - 650, 300, 20),
        (0, SCREEN_HEIGHT - 800, 400, 20),
        (400, SCREEN_HEIGHT - 950, 400, 20)
    ]

    for x, y, width, height in horizontal_platforms:
        walls.add(Wall(x, y, width, height))

    # Génération des ennemis
    for _ in range(5):
        enemy = Enemy(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 200), 20, 20)
        walls.add(enemy)

    # Spawn du joueur
    player.rect.x = SCREEN_WIDTH // 2
    player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE

    return walls

def start_menu(screen):
    font = pygame.font.Font(None, 36)
    menu_items = ["Jouer", "Options", "Quitter"]
    selected_item = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    return selected_item

        screen.fill(WHITE)
        for i, item in enumerate(menu_items):
            color = WHITE if i != selected_item else RED
            text = font.render(item, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40))
            screen.blit(text, text_rect)

        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()

    while True:
        menu_choice = start_menu(screen)

        if menu_choice == 0:  # Jouer
            player = Player()
            walls_level1 = load_level_1(player)
            walls_level2 = load_level_2(player)
            walls_level3 = load_level_3(player)
            walls_level4 = load_level_4(player)

            all_sprites = pygame.sprite.Group()
            all_sprites.add(player)
            all_sprites.add(walls_level1)

            current_level_walls = walls_level1

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
                            all_sprites.remove(walls_level4)
                            all_sprites.add(walls_level1)
                            current_level_walls = walls_level1
                            # Téléportation du joueur au bas milieu du niveau 1
                            player.rect.x = SCREEN_WIDTH // 2
                            player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE
                        elif event.key == pygame.K_2:
                            all_sprites.remove(walls_level1)
                            all_sprites.remove(walls_level3)
                            all_sprites.remove(walls_level4)
                            all_sprites.add(walls_level2)
                            current_level_walls = walls_level2
                            # Téléportation du joueur au bas milieu du niveau 2
                            player.rect.x = SCREEN_WIDTH // 2
                            player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE
                        elif event.key == pygame.K_3:
                            all_sprites.remove(walls_level1)
                            all_sprites.remove(walls_level2)
                            all_sprites.remove(walls_level4)
                            all_sprites.add(walls_level3)
                            current_level_walls = walls_level3
                            # Téléportation du joueur au bas milieu du niveau 3
                            player.rect.x = SCREEN_WIDTH // 2
                            player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE
                        elif event.key == pygame.K_4:
                            all_sprites.remove(walls_level1)
                            all_sprites.remove(walls_level2)
                            all_sprites.remove(walls_level3)
                            all_sprites.add(walls_level4)
                            current_level_walls = walls_level4
                            # Téléportation du joueur au bas milieu du niveau 4
                            player.rect.x = SCREEN_WIDTH // 2
                            player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE

                # Vérifier si le joueur atteint la sortie
                if pygame.sprite.spritecollide(player, current_level_walls, False):
                    for wall in current_level_walls:
                        if pygame.sprite.collide_rect(player, wall) and isinstance(wall, ExitDoor):
                            # Charger le niveau suivant
                            if wall.destination_level == 1:
                                all_sprites.remove(walls_level2)
                                all_sprites.remove(walls_level3)
                                all_sprites.remove(walls_level4)
                                all_sprites.add(walls_level1)
                                current_level_walls = walls_level1
                                # Téléportation du joueur au bas milieu du niveau 1
                                player.rect.x = SCREEN_WIDTH // 2
                                player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE
                            elif wall.destination_level == 2:
                                all_sprites.remove(walls_level1)
                                all_sprites.remove(walls_level3)
                                all_sprites.remove(walls_level4)
                                all_sprites.add(walls_level2)
                                current_level_walls = walls_level2
                                # Téléportation du joueur au bas milieu du niveau 2
                                player.rect.x = SCREEN_WIDTH // 2
                                player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE
                            elif wall.destination_level == 3:
                                all_sprites.remove(walls_level1)
                                all_sprites.remove(walls_level2)
                                all_sprites.remove(walls_level4)
                                all_sprites.add(walls_level3)
                                current_level_walls = walls_level3
                                # Téléportation du joueur au bas milieu du niveau 3
                                player.rect.x = SCREEN_WIDTH // 2
                                player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE
                            elif wall.destination_level == 4:
                                all_sprites.remove(walls_level1)
                                all_sprites.remove(walls_level2)
                                all_sprites.remove(walls_level3)
                                all_sprites.add(walls_level4)
                                current_level_walls = walls_level4
                                # Téléportation du joueur au bas milieu du niveau 4
                                player.rect.x = SCREEN_WIDTH // 2
                                player.rect.y = SCREEN_HEIGHT - PLAYER_SIZE

                # Mettre à jour les ennemis
                for enemy in all_sprites:
                    if isinstance(enemy, Enemy):
                        enemy.update(current_level_walls)

                all_sprites.update(current_level_walls)

                screen.fill(WHITE)
                all_sprites.draw(screen)

                # Dessiner la barre de vie
                pygame.draw.rect(screen, GREEN, (10, 10, player.health, 10))  # Rectangle représentant la barre de vie
                pygame.display.flip()

                clock.tick(60)

        elif menu_choice == 1:  # Options
            # Code pour les options (à implémenter)
            pass

        elif menu_choice == 2:  # Quitter
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
.