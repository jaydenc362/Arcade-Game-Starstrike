# Assets setup
import pygame


# Asset managers
images = {}
sounds = {}


# Load assets
def load_assets():
    images["icon"] = pygame.image.load("assets/icon.png")
    images["player"] = pygame.transform.scale(
        pygame.image.load("assets/player.png").convert_alpha(),
        (174, 81))
    images["player_hurt"] = pygame.transform.scale(
        pygame.image.load("assets/player_hurt.png").convert_alpha(),
        (174, 81))
    images["laser"] = pygame.transform.scale(
        pygame.image.load("assets/laser.png").convert_alpha(),
        (100, 10))