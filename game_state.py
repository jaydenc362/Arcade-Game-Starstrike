# Game state setup
import pygame
from objects import Player
from objects import Laser
from objects import Star
from objects import Meteor


# Game state class
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
            "Starstriker",
            "",
            "By Jayden Chan",
            "Press [enter] to start..."
        ]
        self.lines_printed = 0
        self.timer = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
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


# Play game state
class PlayState(GameState):
    def __init__(self):
        # Initiate fonts
        self.font = pygame.font.Font(None, 70)
        # Initiate wave, wave event, and wave text
        self.wave = 0
        self.wave_event = pygame.event.custom_type()
        pygame.time.set_timer(self.wave_event, 2000)
        self.text_surface = self.font.render("Wave: " + str(self.wave), True, (255, 255, 255))
        # Initiate player
        self.player = Player()
        # Initiate lasers
        Laser.laser_list.clear()
        # Initiate stars
        Star.star_list.clear()
        for _ in range(200):
            Star.star_list.append(Star(True))
        # Initiate meteors
        Meteor.meteor_list.clear()

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
                for _ in range(1 + self.wave // 5):
                    Meteor.meteor_list.append(Meteor())
        return self

    def update(self, dt):
        # Update player
        self.player.update(dt)
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
        self.text_surface = self.font.render("Wave: " + str(self.wave), True, (255, 255, 255))

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
        # Draw player
        self.player.draw(screen)
        # Draw text
        screen.blit(self.text_surface, (30, 30))
        # Display
        pygame.display.flip()