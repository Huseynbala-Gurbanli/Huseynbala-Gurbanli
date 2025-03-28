import pygame
import sys
import random

# Initialize Pygame
pygame.init()

mario_img = pygame.image.load("mario.png")
mario_img = pygame.transform.scale(mario_img, (40, 40))

flap_sound = pygame.mixer.Sound("flap.wav")
hit_sound = pygame.mixer.Sound("hit.wav")
point_sound = pygame.mixer.Sound("point.wav")
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Clone")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)

# Bird properties
bird_x = 100
bird_y = 300
bird_radius = 20
bird_velocity = 0
gravity = 0.5
flap_strength = -10

# Pipe properties
pipe_x = WIDTH
pipe_width = 60
pipe_gap = 150
pipe_height = 300
pipe_speed = 3
score = 0
font = pygame.font.SysFont(None, 48)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Jump on space press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = flap_strength
                flap_sound.play()

    # Physics
    bird_velocity += gravity
    bird_y += bird_velocity

    if bird_y + bird_radius > HEIGHT:
        bird_y = HEIGHT - bird_radius
        bird_velocity = 0

    # Collision with top or bottom of screen
    if bird_y - bird_radius < 0:
        bird_y = bird_radius
        bird_velocity = 0

    # Collision with pipes
    bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2)
    top_pipe_rect = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
    bottom_pipe_rect = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap - 40)

    if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
        hit_sound.play()
        bird_y = 300
        bird_velocity = 0
        pipe_x = WIDTH
        pipe_height = random.randint(100, 400)
        score = 0

    # Update pipe position
    pipe_x -= pipe_speed
    if pipe_x + pipe_width < 0:
        pipe_x = WIDTH
        pipe_height = random.randint(100, 400)

    if pipe_x + pipe_width == bird_x:
        score += 1
        point_sound.play()

    # Clear screen
    screen.fill(BLUE)

    # Draw bird
    screen.blit(mario_img, (bird_x - 20, int(bird_y) - 20))

    pygame.draw.rect(screen, (222, 184, 135), (0, HEIGHT - 40, WIDTH, 40))  # ground
    pygame.draw.rect(screen, (0, 200, 0), (pipe_x, 0, pipe_width, pipe_height))  # top pipe
    pygame.draw.rect(screen, (0, 200, 0), (pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap - 40))  # bottom pipe

    # Draw score
    score_text = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_text, (WIDTH // 2, 20))

    # Update display
    pygame.display.update()
    clock.tick(FPS)