import pygame

# Initialize the game engine
pygame.init()

# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

# This sets the name of the window
pygame.display.set_caption("Collision Example")

# Set the background color
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))


class Ball(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # set speed
        self.velocity_x = 1
        self.velocity_y = 1

    def move(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def draw_rect(self):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)


if __name__ == "__main__":
    ball = Ball((255, 0, 0), 20, 15)
    ball.rect.x = 100
    ball.rect.y = 100

    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(ball)

    clock = pygame.time.Clock()

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ball.velocity_x = -3
                elif event.key == pygame.K_RIGHT:
                    ball.velocity_x = 3
                elif event.key == pygame.K_UP:
                    ball.velocity_y = -3
                elif event.key == pygame.K_DOWN:
                    ball.velocity_y = 3
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    ball.velocity_x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    ball.velocity_y = 0
        # Apply gravity
        #ball.velocity_y += 0.35
        ball.move()

        screen.fill((255, 255, 255))

        ball.draw_rect()

        all_sprites_list.draw(screen)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
