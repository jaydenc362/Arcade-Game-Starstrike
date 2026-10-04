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
    images["enemy"] = pygame.transform.scale(
        pygame.image.load("assets/enemy.png").convert_alpha(),
        (130, 60))
    images["enemy_hurt"] = pygame.transform.scale(
        pygame.image.load("assets/enemy_hurt.png").convert_alpha(),
        (130, 60))
    images["enemy_attack"] = pygame.transform.scale(
        pygame.image.load("assets/enemy_attack.png").convert_alpha(),
        (130, 60))
    images["enemy_attack_hurt"] = pygame.transform.scale(
        pygame.image.load("assets/enemy_attack_hurt.png").convert_alpha(),
        (130, 60))