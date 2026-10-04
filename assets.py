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
    # Sounds
    sounds["among_us"] = pygame.mixer.music.load("assets/sounds/among_us.mp3")
    # ^ Music volume set independently
    sounds["death"] = pygame.mixer.Sound("assets/sounds/death.mp3")
    sounds["death"].set_volume(0.5)
    sounds["pew"] = pygame.mixer.Sound("assets/sounds/pew.mp3")
    sounds["pew"].set_volume(0.5)