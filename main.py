import pygame
import sys

# Pygame Setup
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My First Pygame")
clock = pygame.time.Clock()
FPS = 60
running = True

# Game Loop
while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update

    # Screen Color
    screen.fill((0, 0, 0))

    # Draw

    # Display
    pygame.display.flip()

    # FPS
    clock.tick(FPS)

pygame.quit()
sys.exit()