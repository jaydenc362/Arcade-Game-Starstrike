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
    if result == False:
        running = False
    else:
        current_state = result

    # FPS
    dt = clock.tick(FPS) / 1000

    # Run game state
    current_state.update(dt)
    current_state.draw(screen)


# Pygame end
pygame.quit()
sys.exit()