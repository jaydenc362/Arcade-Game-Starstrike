# Assets setup
import pygame


# Asset managers
images = {}
sounds = {}


# Load assets
def load_assets():
    # Images
    images["icon"] = pygame.image.load("assets/images/icon.png")
    images["player"] = pygame.transform.scale(
        pygame.image.load("assets/images/player.png").convert_alpha(),
        (174, 81))
    images["player_hurt"] = pygame.transform.scale(
        pygame.image.load("assets/images/player_hurt.png").convert_alpha(),
        (174, 81))
    images["laser"] = pygame.transform.scale(
        pygame.image.load("assets/images/laser.png").convert_alpha(),
        (100, 10))
    images["enemy"] = pygame.transform.scale(
        pygame.image.load("assets/images/enemy.png").convert_alpha(),
        (130, 60))
    images["enemy_hurt"] = pygame.transform.scale(
        pygame.image.load("assets/images/enemy_hurt.png").convert_alpha(),
        (130, 60))
    images["enemy_attack"] = pygame.transform.scale(
        pygame.image.load("assets/images/enemy_attack.png").convert_alpha(),
        (130, 60))
    images["enemy_attack_hurt"] = pygame.transform.scale(
        pygame.image.load("assets/images/enemy_attack_hurt.png").convert_alpha(),
        (130, 60))
    images["boom"] = pygame.transform.scale(
        pygame.image.load("assets/images/boom.png").convert_alpha(),
        (110, 110))
    # Sounds (music loaded and played independently)
    sounds["death"] = pygame.mixer.Sound("assets/sounds/death.ogg")
    sounds["death"].set_volume(0.5)
    sounds["pew"] = pygame.mixer.Sound("assets/sounds/pew.ogg")
    sounds["pew"].set_volume(0.5)
    sounds["boom"] = pygame.mixer.Sound("assets/sounds/boom.ogg")
    sounds["boom"].set_volume(0.3)
    sounds["damage"] = pygame.mixer.Sound("assets/sounds/damage.ogg")
    sounds["damage"].set_volume(0.5)