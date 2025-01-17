import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

class Bird:
    def __init__(self):
        self.x = SCREEN_WIDTH // 3
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, 30, 30)

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Pipe:
    def __init__(self):
        self.gap_y = random.randint(100, SCREEN_HEIGHT - 100)
        self.x = SCREEN_WIDTH
        self.top_height = self.gap_y - PIPE_GAP // 2
        self.bottom_height = SCREEN_HEIGHT - (self.gap_y + PIPE_GAP // 2)
        self.top_rect = pygame.Rect(self.x, 0, 50, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.bottom_height, 50, self.bottom_height)

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)

def main():
    bird = Bird()
    pipes = []
    last_pipe = pygame.time.get_ticks()
    score = 0
    game_active = True

    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird.flap()
                if event.key == pygame.K_SPACE and not game_active:
                    # Reset game
                    bird = Bird()
                    pipes = []
                    last_pipe = current_time
                    score = 0
                    game_active = True

        if game_active:
            # Update bird
            bird.update()

            # Generate new pipes
            if current_time - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe())
                last_pipe = current_time

            # Update and check pipes
            for pipe in pipes[:]:
                pipe.update()
                if pipe.x < -50:
                    pipes.remove(pipe)
                if pipe.x == bird.x:
                    score += 1

                # Collision detection
                if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                    game_active = False

            # Check if bird hits boundaries
            if bird.y < 0 or bird.y > SCREEN_HEIGHT:
                game_active = False

        # Draw everything
        screen.fill(BLACK)
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        if not game_active:
            game_over_text = font.render('Game Over! Press SPACE to restart', True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
