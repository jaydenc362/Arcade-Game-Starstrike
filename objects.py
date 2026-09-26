# Class setup
import pygame
import random
from collisions import Collisions
WIDTH = 1920
HEIGHT = 1080

# Player class
class Player:
    def __init__(self):
        # Customizable
        self.acceleration = 1000
        self.friction = 1000
        self.max_velocity = 1000
        self.size = 100
        self.color = (255, 0, 0)
        # Uncustomizable
        self.position = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(
            self.position.x - self.size / 2,
            self.position.y - self.size / 2,
            self.size, self.size)

    def move(self, dt):
        # Controls
        keys = pygame.key.get_pressed()
        move_left = (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not (keys[pygame.K_RIGHT] or keys[pygame.K_d])
        move_right = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not (keys[pygame.K_LEFT] or keys[pygame.K_a])
        move_up = (keys[pygame.K_UP] or keys[pygame.K_w]) and not (keys[pygame.K_DOWN] or keys[pygame.K_s])
        move_down = (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not (keys[pygame.K_UP] or keys[pygame.K_w])
        if move_left:
            self.velocity.x -= self.acceleration * dt
        elif move_right:
            self.velocity.x += self.acceleration * dt
        else:
            if self.velocity.x > 0:
                self.velocity.x = max(0, self.velocity.x - self.friction * dt)
            elif self.velocity.x < 0:
                self.velocity.x = min(0, self.velocity.x + self.friction * dt)
        if move_up:
            self.velocity.y -= self.acceleration * dt
        elif move_down:
            self.velocity.y += self.acceleration * dt
        else:
            if self.velocity.y > 0:
                self.velocity.y = max(0, self.velocity.y - self.friction * dt)
            elif self.velocity.y < 0:
                self.velocity.y = min(0, self.velocity.y + self.friction * dt)
        # Enforce max velocity
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
        self.velocity.y = max(-self.max_velocity, min(self.velocity.y, self.max_velocity))
        # Apply velocity to position
        self.position += self.velocity * dt

    def shoot_laser(self):
        Laser.laser_list.append(Laser(self.position, self.velocity))

    def screen_wrap(self):
        half_size = self.size / 2
        if self.position.x < -half_size:
            self.position.x = WIDTH + half_size
        elif self.position.x > WIDTH + half_size:
            self.position.x = -half_size
        if self.position.y < -half_size:
            self.position.y = HEIGHT + half_size
        elif self.position.y > HEIGHT + half_size:
            self.position.y = -half_size

    def update_rect(self):
        self.rect = pygame.Rect(
            self.position.x - self.width / 2,
            self.position.y - self.height / 2,
            self.width, self.height)

    def update(self, dt):
        self.move(dt)
        self.screen_wrap()

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.color,
            (self.position.x - self.size / 2,
            self.position.y - self.size / 2,
            self.size, self.size))


# Laser class
class Laser:
    laser_list = []
    def __init__(self, player_position, player_velocity):
        # Customizable
        self.speed = 2000
        self.width = 100
        self.height = 10
        self.color = (255, 255, 0)
        # Uncustomizable
        self.position = player_position.copy()
        self.velocity = pygame.Vector2(player_velocity.copy().x + self.speed, 0)
        self.rect = pygame.Rect(
            self.position.x - self.width / 2,
            self.position.y - self.height / 2,
            self.width, self.height)

    def move(self, dt):
        self.position += self.velocity * dt

    def update_rect(self):
        self.rect = pygame.Rect(
            self.position.x - self.width / 2,
            self.position.y - self.height / 2,
            self.width, self.height)

    def remove(self):
        if self.position.x > WIDTH + self.width:
            Laser.laser_list.remove(self)

    def update(self, dt):
        self.move(dt)
        self.update_rect()
        self.remove()

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.color,
            (self.position.x - self.width / 2,
            self.position.y - self.height / 2,
            self.width, self.height))

# Meteor class
class Meteor:
    meteor_list = []
    def __init__(self):
        # Customizable
        self.radius = random.randint(1, 3) * 20
        self.speed = random.uniform(5, 10) * self.radius
        self.color = (100, 100, 100)
        # Uncustomizable
        self.position = pygame.Vector2(
            WIDTH + self.radius,
            random.uniform(-self.radius, HEIGHT + self.radius))
        self.velocity = pygame.Vector2(self.speed, 0)

    def move(self, dt):
        self.position -= self.velocity * dt

    def remove(self):
        # If out of bounds
        if self.position.x < -self.radius:
            Meteor.meteor_list.remove(self)
        # If touched by laser
        for laser in Laser.laser_list:
            if Collisions.circle_rect_collision(self.position, self.radius, laser.rect):
                Meteor.meteor_list.remove(self)
                break
    
    def update(self, dt):
        self.move(dt)
        self.remove()

    def draw(self, surface):
        pygame.draw.circle(
            surface, self.color,
            self.position, self.radius)

# Star class
class Star:
    star_list = []
    def __init__(self, pregenerate = False):
        # Customizable
        self.radius = random.randint(1, 2)
        self.speed = random.uniform(30, 70) * self.radius
        self.color = (255, 255, 255)
        # Uncustomizable
        self.position = pygame.Vector2(
            random.uniform(-self.radius, WIDTH + self.radius) if pregenerate else WIDTH + self.radius,
            random.uniform(-self.radius, HEIGHT + self.radius))
        self.velocity = pygame.Vector2(self.speed, 0)

    def move(self, dt):
        self.position -= self.velocity * dt

    def remove(self):
        if self.position.x < -self.radius:
            Star.star_list.remove(self)
            Star.star_list.append(Star())

    def update(self, dt):
        self.move(dt)
        self.remove()

    def draw(self, surface):
        pygame.draw.circle(
            surface, self.color,
            self.position, self.radius)