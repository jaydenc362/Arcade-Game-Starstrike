# Main setup
import pygame
import game_state
import sys


# Pygame setup
pygame.init()
WIDTH = 1920
HEIGHT = 1080
flags = pygame.SCALED | pygame.RESIZABLE
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags, vsync = 1)
pygame.display.set_caption("Jayden Chan's Arcade Game: Starstrike: Python Edition")
pygame.display.set_icon(pygame.image.load("icon.png"))
clock = pygame.time.Clock()
FPS = 60
dt = 0
running = True
current_state = game_state.MenuState()


# Game Loop
while running:
    # Events
    events = pygame.event.get()
    result = current_state.handle_events(events)
    if result == False: # Check for game state switch triggered by handle_events()
        running = False
    else:
        current_state = result

    # FPS
    dt = clock.tick(FPS) / 1000

    # Run game state
    result = current_state.update(dt)
    current_state.draw(screen)
    if result != None: # Check for game state switch triggered by update()
        current_state = result


# Pygame end
pygame.quit()
sys.exit()

# ============================
# UNIT 2 MATH & AI EXPLANATION
# ============================

# Vectors
# Storing position and velocity of objects

# Distance
# Calculating detection range

# Normalization
# Calculating normal direction meteor hits player, multiplied by meteor's velocity to create knockback vector

# Angles / sine / cosine
# Affects velocity direction when targeting player

# Velocity and acceleration
# Player acceleration scaler is added to player velocity vector, which is then added to player position vector

# Dot product
# Calculating detection within fov

# AI decision-making
# TO BE IMPLEMENTED IN ENEMY OBJECTS