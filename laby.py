import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
FPS = 30

# Taille des cellules et du labyrinthe initial
CELL_SIZE = 40
INITIAL_ROWS, INITIAL_COLS = 15, 20
ROWS, COLS = INITIAL_ROWS, INITIAL_COLS

# Taille minimale du labyrinthe
MIN_ROWS, MIN_COLS = 5, 5

# Temps avant réduction de la carte (en millisecondes)
TIME_BEFORE_REDUCTION = 30000

# Création de la classe Labyrinthe
class Labyrinth:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.generate_walls()

    def generate_walls(self):
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        for row in range(1, self.rows - 1, 2):
            for col in range(1, self.cols - 1, 2):
                self.grid[row][col] = 1

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Création de la classe Joueur
class Player:
    def __init__(self, image_path, start_row, start_col):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.row = start_row
        self.col = start_col

    def move(self, direction, labyrinth):
        new_row, new_col = self.row, self.col

        if direction == 'UP' and self.row > 0:
            new_row -= 1
        elif direction == 'DOWN' and self.row < labyrinth.rows - 1:
            new_row += 1
        elif direction == 'LEFT' and self.col > 0:
            new_col -= 1
        elif direction == 'RIGHT' and self.col < labyrinth.cols - 1:
            new_col += 1

        # Vérifier les collisions avec les murs
        if labyrinth.grid[new_row][new_col] == 0:
            self.row, self.col = new_row, new_col

    def draw(self, screen):
        screen.blit(self.image, (self.col * CELL_SIZE, self.row * CELL_SIZE))

# Initialisation du labyrinthe et des joueurs
labyrinth = Labyrinth(ROWS, COLS)
player1 = Player("perso1.png", 0, 0)
player2 = Player("perso2.png", ROWS - 1, COLS - 1)

# Taille de l'écran
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Initialisation de l'écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bomberman Labyrinth")

# Temps au début du jeu
start_time = pygame.time.get_ticks()

# Boucle principale
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player1.move('UP', labyrinth)
            elif event.key == pygame.K_DOWN:
                player1.move('DOWN', labyrinth)
            elif event.key == pygame.K_LEFT:
                player1.move('LEFT', labyrinth)
            elif event.key == pygame.K_RIGHT:
                player1.move('RIGHT', labyrinth)
            elif event.key == pygame.K_w:
                player2.move('UP', labyrinth)
            elif event.key == pygame.K_s:
                player2.move('DOWN', labyrinth)
            elif event.key == pygame.K_a:
                player2.move('LEFT', labyrinth)
            elif event.key == pygame.K_d:
                player2.move('RIGHT', labyrinth)

    # Vérifier le temps écoulé
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time

    # Si 30 secondes se sont écoulées, réduire la carte et réinitialiser le temps
    if elapsed_time >= TIME_BEFORE_REDUCTION and labyrinth.rows > MIN_ROWS and labyrinth.cols > MIN_COLS:
        labyrinth.rows -= 2
        labyrinth.cols -= 2

        # Ajuster la taille de l'écran
        WIDTH, HEIGHT = labyrinth.cols * CELL_SIZE, labyrinth.rows * CELL_SIZE
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Réinitialiser les joueurs aux extrémités de la nouvelle carte
        player1.row, player1.col = 0, 0
        player2.row, player2.col = labyrinth.rows - 1, labyrinth.cols - 1

        # Réinitialiser le labyrinthe centré sur l'écran
        labyrinth = Labyrinth(labyrinth.rows, labyrinth.cols)

        start_time = pygame.time.get_ticks()

    # Dessiner le labyrinthe
    screen.fill((255, 255, 255))
    labyrinth.draw(screen)

    # Dessiner les joueurs
    player1.draw(screen)
    player2.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

# Quitter Pygame
pygame.quit()
sys.exit()



