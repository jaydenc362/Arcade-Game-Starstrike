import pygame
import sys


# Pygame setup
pygame.init()
WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED, vsync = 1)
pygame.display.set_caption("Jayden Chan's Arcade Game: Starstrike: Python Edition")
pygame.display.set_icon(pygame.image.load("icon.png"))
clock = pygame.time.Clock()
FPS = 60
dt = 0
running = True


# Font
font = pygame.font.Font(None, 100)


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
            (self.position.x - self.size / 2, self.position.y - self.size / 2, self.size, self.size)
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


# Game Setup
timer_event = pygame.event.custom_type()
pygame.time.set_timer(timer_event, 2000)
wave = 0
player = Player()


# Game Loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == timer_event:
            wave += 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot_laser()

    # FPS
    dt = clock.tick(FPS) / 1000

    # Update
    player.update(dt)
    for laser in Laser.laser_list[:]:
        laser.update(dt)
        if laser.position.x > WIDTH + laser.width:
            Laser.laser_list.remove(laser)
    text_surface = font.render("Wave: " + str(wave), True, (255, 255, 255))
            
    # Screen color
    screen.fill((0, 0, 0))

    # Draw
    for laser in Laser.laser_list:
        laser.draw(screen)
    player.draw(screen)
    screen.blit(text_surface, (30, 30))

    # Display
    pygame.display.flip()

# Pygame end
pygame.quit()
sys.exit()