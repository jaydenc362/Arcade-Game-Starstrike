import pygame
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


# Fonts
font = pygame.font.Font(None, 70)


# Objects
from objects import Player
from objects import Laser
from objects import Star
from objects import Meteor


# Game Setup
timer_event = pygame.event.custom_type()
pygame.time.set_timer(timer_event, 2000)
wave = 0
player = Player()
for i in range(200):
    Star.star_list.append(Star(True))


# Game Loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == timer_event:
            wave += 1
            for i in range(1 + wave // 5):
                Meteor.meteor_list.append(Meteor())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot_laser()

    # FPS
    dt = clock.tick(FPS) / 1000

    # Update player
    player.update(dt)
    # Update lasers
    for laser in Laser.laser_list[:]:
        laser.update(dt)
    # Update meteors
    for meteor in Meteor.meteor_list[:]:
        meteor.update(dt)
    # Update stars
    for star in Star.star_list[:]:
        star.update(dt)
    # Update text
    text_surface = font.render("Wave: " + str(wave), True, (255, 255, 255))
            
    # Screen color
    screen.fill((0, 0, 0))

    # Draw stars
    for star in Star.star_list:
        star.draw(screen)
    # Draw lasers
    for laser in Laser.laser_list:
        laser.draw(screen)
    # Draw meteors
    for meteor in Meteor.meteor_list:
        meteor.draw(screen)
    # Draw player
    player.draw(screen)
    # Draw text
    screen.blit(text_surface, (30, 30))

    # Display
    pygame.display.flip()

# Pygame end
pygame.quit()
sys.exit()