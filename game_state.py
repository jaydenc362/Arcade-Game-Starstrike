# Game state setup
import pygame
import assets
from objects import Player
from objects import Laser
from objects import Star
from objects import Meteor
from objects import Enemy
WIDTH = 1920
HEIGHT = 1080


# Game state interface
class GameState:
    def handle_events(self, events):
        pass
    def update(self, dt):
        pass
    def draw(self, screen):
        pass


# Menu game state
class MenuState(GameState):
    def __init__(self):
        self.font = pygame.font.Font(None, 120)
        self.lines = [
            "Arcade Game:",
            "Starstrike: Python Edition",
            "",
            "By Jayden Chan",
            "",
            "Press [enter] to start...",
            "Press [esc] to quit...",
        ]
        self.lines_printed = 0
        self.timer = 0
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    return PlayState()
        return self

    def update(self, dt):
        self.timer += dt
        if self.timer >= 1:
            self.timer = 0
            if self.lines_printed < len(self.lines) and self.lines[self.lines_printed] == "": # Skip empty lines
                self.lines_printed += 1
            if self.lines_printed < len(self.lines):
                self.lines_printed += 1


    def draw(self, screen):
        # Screen color
        screen.fill((0, 0, 0))
        # Draw text
        for i in range(self.lines_printed):
            text_surface = self.font.render(self.lines[i], True, (255, 255, 255))
            screen.blit(text_surface, (30, 30 + i * self.font.get_height()))
        # Display
        pygame.display.flip()


# Play game state
class PlayState(GameState):
    def __init__(self):
        # Initiate fonts
        self.font = pygame.font.Font(None, 70)
        # Initiate wave, wave event, and wave text
        self.wave = 0
        self.wave_event = pygame.event.custom_type()
        pygame.time.set_timer(self.wave_event, 3000)
        self.wave_text_surface = "Wave: "
        # Initiate player, and health
        self.player = Player()
        self.health_text_surface = "Health: "
        # Initiate lasers
        Laser.laser_list.clear()
        # Initiate stars
        Star.star_list.clear()
        for _ in range(200):
            Star.star_list.append(Star(True))
        # Initiate meteors
        Meteor.meteor_list.clear()
        # Initiate enemies
        Enemy.enemy_list.clear()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return MenuState()
                elif event.key == pygame.K_SPACE:
                    self.player.shoot_laser()
            elif event.type == self.wave_event:
                self.wave += 1
                # Spawn meteors
                for _ in range(1 + self.wave // 5):
                    Meteor.meteor_list.append(Meteor())
                # Spawn enemies
                for _ in range(0 + self.wave // 7):
                    Enemy.enemy_list.append(Enemy())
        return self

    def update(self, dt):
        # Update player
        self.player.update(dt)
        if self.player.health <= 0:
            return EndState()
        # Update lasers
        for laser in Laser.laser_list[:]:
            laser.update(dt)
        # Update enemies
        for enemy in Enemy.enemy_list[:]:
            enemy.update(dt, self.player)
        # Update meteors
        for meteor in Meteor.meteor_list[:]:
            meteor.update(dt)
        # Update stars
        for star in Star.star_list[:]:
            star.update(dt)
        # Update text
        self.wave_text_surface = self.font.render("Wave: " + str(self.wave), True, (255, 255, 255))
        self.health_text_surface = self.font.render("Health: " + str(self.player.health), True, (0, 255, 0))

    def draw(self, screen):
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
        # Draw enemies
        for enemy in Enemy.enemy_list:
            enemy.draw(screen)
        # Draw player
        self.player.draw(screen)
        # Draw text
        screen.blit(self.wave_text_surface, (30, 30))
        screen.blit(self.health_text_surface, (WIDTH - 30 - self.health_text_surface.get_width(), 30))
        # Display
        pygame.display.flip()


# End game state
class EndState(GameState):
    def __init__(self):
        self.font = pygame.font.Font(None, 120)
        self.lines = [
            "YOU LOSE!",
            "",
            "Press [enter] to restart...",
            "Press [esc] to enter menu...",
        ]
        self.lines_printed = 0
        self.timer = 0
        assets.sounds["death"].play()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return MenuState()
                elif event.key == pygame.K_RETURN:
                    return PlayState()
        return self

    def update(self, dt):
        self.timer += dt
        if self.timer >= 1:
            self.timer = 0
            if self.lines_printed < len(self.lines) and self.lines[self.lines_printed] == "": # Skip empty lines
                self.lines_printed += 1
            if self.lines_printed < len(self.lines):
                self.lines_printed += 1


    def draw(self, screen):
        # Screen color
        screen.fill((0, 0, 0))
        # Draw text
        for i in range(self.lines_printed):
            text_surface = self.font.render(self.lines[i], True, (255, 255, 255))
            screen.blit(text_surface, (30, 30 + i * self.font.get_height()))
        # Display
        pygame.display.flip()