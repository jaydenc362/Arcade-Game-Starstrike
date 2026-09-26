# Class setup
import pygame
WIDTH = 1920
HEIGHT = 1080

# Player class
class Player:
    def __init__(self):
        self.position = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 1000
        self.friction = 1000
        self.max_velocity = 1000
        self.size = 100
        self.color = (255, 0, 0)

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

    def update(self, dt):
        self.move(dt)
        self.screen_wrap()

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.color,
            (self.position.x - self.size / 2,
            self.position.y - self.size / 2,
            self.size, self.size)
        )


# Laser class
class Laser:
    laser_list = []
    def __init__(self, player_position, player_velocity):
        self.position = player_position.copy()
        self.velocity = player_velocity.copy().x + 2000
        self.width = 100
        self.height = 10
        self.color = (255, 255, 0)

    def move(self, dt):
        self.position.x += self.velocity * dt

    def update(self, dt):
        self.move(dt)

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.color,
            (self.position.x - self.width / 2, self.position.y - self.height / 2, self.width, self.height)
        )