import pygame
import sys
import random


# Pygame setup
pygame.init()
WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED, vsync = 1)
pygame.display.set_caption("Jayden Chan's Arcade Game: Starstrike: Python Edition")
pygame.display.set_icon(pygame.image.load("icon.png"))
clock = pygame.time.Clock()
FPS = 60
dt = 0
running = True


# Fonts
font = pygame.font.Font(None, 100)


# Objects
from objects import Player
from objects import Laser


# Game Setup
timer_event = pygame.event.custom_type()
pygame.time.set_timer(timer_event, 2000)
wave = 0
player = Player()


# Game Loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == timer_event:
            wave += 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot_laser()

    # FPS
    dt = clock.tick(FPS) / 1000

    # Update
    player.update(dt)
    for laser in Laser.laser_list[:]:
        laser.update(dt)
        if laser.position.x > WIDTH + laser.width:
            Laser.laser_list.remove(laser)
    text_surface = font.render("Wave: " + str(wave), True, (255, 255, 255))
            
    # Screen color
    screen.fill((0, 0, 0))

    # Draw
    for laser in Laser.laser_list:
        laser.draw(screen)
    player.draw(screen)
    screen.blit(text_surface, (30, 30))

    # Display
    pygame.display.flip()

# Pygame end
pygame.quit()
sys.exit()