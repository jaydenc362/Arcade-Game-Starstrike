# Object setup
import pygame
import random
import math
import assets
from collisions import Collisions
WIDTH = 1920
HEIGHT = 1080


# Player object
class Player:
    def __init__(self):
        # Customizable
        self.acceleration = 1000
        self.friction = 1000
        self.max_velocity = 1000
        self.width = 174
        self.height = 81
        self.health = 3
        self.immunity_time = 2
        self.flicker_time = 0.05
        # Uncustomizable
        self.position = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(
            self.position.x - self.width / 2,
            self.position.y - self.height / 2,
            self.width, self.height)
        self.image = "player"
        self.immune = False
        self.immunity_timer = 0
        self.flicker_timer = 0

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
        if self.velocity.length() > self.max_velocity:
            self.velocity.scale_to_length(self.max_velocity)
        # Apply velocity to position
        self.position += self.velocity * dt
        # Apply screen wrap
        self.screen_wrap()
        # Apply position to rect
        self.update_rect()

    def shoot_laser(self):
        Laser.laser_list.append(Laser(self.position, self.velocity))

    def take_damage(self):
        # If touched by meteor
        for meteor in Meteor.meteor_list[:]:
            if not self.immune and Collisions.circle_rect_collision(meteor.position, meteor.radius, self.rect):
                self.health -= 1
                self.immune = True
                self.immunity_timer = self.immunity_time
                knock_back = self.calculate_knock_back(meteor)
                self.velocity += knock_back
        # If touched by enemy
            for enemy in Enemy.enemy_list[:]:
                if not self.immune and Collisions.rect_rect_collision(self.rect, enemy.rect):
                    self.health -= 1
                    self.immune = True
                    self.immunity_timer = self.immunity_time
                    knock_back = self.calculate_knock_back(enemy)
                    self.velocity += knock_back

    def calculate_knock_back(self, other):
        direction = self.position - other.position
        if direction.length() == 0:
            return pygame.Vector2(0, 0)
        normal_direction = direction.normalize()
        return normal_direction * other.velocity.length() * 5

    def deplete_immunity(self, dt):
        if self.immune:
            self.immunity_timer -= dt
            self.flicker_timer -= dt
            if self.immunity_timer <= 0:
                self.immunity_timer = 0
                self.immune = False
                self.image = "player"
            # Flicker when immune
            elif self.flicker_timer <= 0:
                self.flicker_timer = self.flicker_time
                if self.image == "player":
                    self.image = "player_hurt"
                else:
                    self.image = "player"

    def screen_wrap(self):
        half_width = self.width / 2
        half_height = self.height / 2
        if self.position.x < -half_width:
            self.position.x = WIDTH + half_width
        elif self.position.x > WIDTH + half_width:
            self.position.x = -half_width
        if self.position.y < -half_height:
            self.position.y = HEIGHT + half_height
        elif self.position.y > HEIGHT + half_height:
            self.position.y = -half_height

    def update_rect(self):
        self.rect = pygame.Rect(
            self.position.x - self.width / 2,
            self.position.y - self.height / 2,
            self.width, self.height)

    def update(self, dt):
        self.move(dt)
        self.take_damage()
        self.deplete_immunity(dt)

    def draw(self, surface):
        image = assets.images[self.image]
        surface.blit(
            image,
            (self.position.x - image.get_width() / 2,
            self.position.y - image.get_height() / 2))


# Laser object
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
        self.image = "laser"

    def move(self, dt):
        self.position += self.velocity * dt

    def update_rect(self):
        self.rect = pygame.Rect(
            self.position.x - self.width / 2,
            self.position.y - self.height / 2,
            self.width, self.height)

    def remove(self):
        # If out of bounds
        if self.position.x > WIDTH + self.width:
            Laser.laser_list.remove(self)
        # If touched by meteor logic is done in Meteor to destroy both at same time

    def update(self, dt):
        self.move(dt)
        self.update_rect()
        self.remove()

    def draw(self, surface):
        image = assets.images[self.image]
        surface.blit(
            image,
            (self.position.x - image.get_width() / 2,
            self.position.y - image.get_height() / 2))


# Meteor object
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
        self.velocity = pygame.Vector2(-self.speed, 0)

    def move(self, dt):
        self.position += self.velocity * dt

    def remove(self):
        # If out of bounds
        if self.position.x < -self.radius:
            Meteor.meteor_list.remove(self)
            return
        # If touched by laser
        for laser in Laser.laser_list[:]:
            if Collisions.circle_rect_collision(self.position, self.radius, laser.rect):
                Meteor.meteor_list.remove(self)
                Laser.laser_list.remove(laser)
                return
    
    def update(self, dt):
        self.move(dt)
        self.remove()

    def draw(self, surface):
        pygame.draw.circle(
            surface, self.color,
            self.position, self.radius)


# Star object
class Star:
    star_list = []
    def __init__(self, pregenerate = False):
        # Customizable
        self.radius = random.randint(1, 2)
        self.speed = random.uniform(30, 70) * self.radius
        self.color = (
            255 - self.radius * 50,
            255 - self.radius * 50,
            255 - self.radius * 50)
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


# Enemy Object
class Enemy:
    enemy_list = []
    def __init__(self):
        # Customizable
        self.width = 70
        self.height = 50
        self.angle = math.pi
        self.fov = 0.7
        self.range = 400
        self.acceleration = 500
        self.max_velocity = 500
        self.color = (0, 255, 0)
        self.health = 2
        self.immunity_time = 2
        self.flicker_time = 0.05
        # Uncustomizable
        self.position = pygame.Vector2(
            WIDTH + self.width,
            random.uniform(-self.height, HEIGHT + self.height))
        self.velocity = pygame.Vector2(-self.max_velocity, 0)
        self.rect = pygame.Rect(
            self.position.x - self.width / 2,
            self.position.y - self.height / 2,
            self.width, self.height)
        self.immune = False
        self.immunity_timer = 0
        self.flicker_timer = 0
        self.states = "standard"

    def move(self, dt, player):
        # Apply angle towards player
        if self.detected_player(player):
            direction = player.position - self.position
            self.angle = math.atan2(-direction.y, direction.x)
        else:
            self.angle = math.pi
        # Apply acceleration to velocity
        self.velocity.x -= self.acceleration * dt * -math.cos(self.angle)
        self.velocity.y -= self.acceleration * dt * math.sin(self.angle)
        # Enforce max velocity
        if self.velocity.length() > self.max_velocity:
            self.velocity.scale_to_length(self.max_velocity)
        # Apply velocity to position
        self.position += self.velocity * dt
        # Apply position to rect
        self.update_rect()

    def take_damage(self):
        # If touched by laser
        for laser in Laser.laser_list[:]:
            if not self.immune and Collisions.rect_rect_collision(self.rect, laser.rect):
                self.health -= 1
                self.immune = True
                self.immunity_timer = self.immunity_time
                knock_back = self.calculate_enemy_laser_knock_back(laser)
                self.velocity += knock_back

    def calculate_enemy_laser_knock_back(self, laser):
            direction = self.position - laser.position
            if direction.length() == 0:
                return pygame.Vector2(0, 0)
            normal_direction = direction.normalize()
            return normal_direction * laser.velocity.length() * 0.25
    
    def deplete_immunity(self, dt):
        if self.immune:
            self.immunity_timer -= dt
            self.flicker_timer -= dt
            if self.immunity_timer <= 0:
                self.immunity_timer = 0
                self.immune = False
                self.color = (0, 255, 0)
            # Flicker when immune
            elif self.flicker_timer <= 0:
                self.flicker_timer = self.flicker_time
                if self.color == (0, 255, 0):
                    self.color = (0, 100, 0)
                else:
                    self.color = (0, 255, 0)

    def remove(self):
        # If out of bounds
        if self.position.x < -self.width:
            Enemy.enemy_list.remove(self)
            return
        # If touched by laser
        if self.health <= 0:
            Enemy.enemy_list.remove(self)
            return

    def detected_player(self, player):
        forward = pygame.Vector2(math.cos(self.angle), -math.sin(self.angle))
        direction = (player.position - self.position)
        distance = direction.length()
        if distance == 0:
            return True
        normal = direction.normalize()
        dot = forward.dot(normal)
        return distance < self.range and dot > self.fov

    def update_rect(self):
        self.rect = pygame.Rect(
            self.position.x - self.width / 2,
            self.position.y - self.height / 2,
            self.width, self.height)
            
    def update(self, dt, player):
        self.move(dt, player)
        self.take_damage()
        self.remove()
        self.deplete_immunity(dt)

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.color,
            (self.position.x - self.width / 2,
            self.position.y - self.height / 2,
            self.width, self.height))