# Main setup
import pygame
import game_state
import assets
import sys


# Pygame setup
pygame.init()
WIDTH = 1920
HEIGHT = 1080
flags = pygame.SCALED | pygame.RESIZABLE
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags, vsync = 1)
assets.load_assets()
pygame.display.set_caption("Jayden Chan's Arcade Game: Starstrike: Python Edition")
pygame.display.set_icon(assets.images["icon"])
clock = pygame.time.Clock()
FPS = 60
dt = 0
running = True
current_state = game_state.MenuState()


# Game Loop
while running:
    # Events
    events = pygame.event.get()
    result = current_state.handle_events(events)
    if result == False: # Check for game state switch triggered by handle_events()
        running = False
    else:
        current_state = result

    # FPS
    dt = clock.tick(FPS) / 1000

    # Run game state
    result = current_state.update(dt)
    current_state.draw(screen)
    if result != None: # Check for game state switch triggered by update()
        current_state = result


# Pygame end
pygame.quit()
sys.exit()


# ============================
# UNIT 2 MATH & AI EXPLANATION
# ============================

# Vectors:
### Vectors are used here to store the positions and velocities of objects.
### Their components are used to calculate collisions too.

# Distance:
### Distance is used to calculate whether or not an enemy is within range of the player.
### Distance is used to calculate collisions too.

# Normalization:
### Normalization is used to find the direction where objects would bounce after colliding.
### These normalized vectors are multiplied by a customized factor to create a knockback velocity vector.
### The knockback velocity vector is then added to the velocity of the object bouncing away.

# Angles / sine / cosine:
### Angles are used to make enemies move towards the player when detected.
### The angle is calculated first for its components to be used.
### Sine affects the X velocity, while cosine affects the Y velocity.

# Velocity and acceleration:
### Acceleration is stored as a scalar.
### Acceleration is added to the player and enemies velocities.
### Finally, velocity is added to the object's position.
### This makes movement smooth.

# Dot product:
### Dot product is used to calculate if the enemy can see the player within it's FOV.
### The dot product is compared to the FOV value.
### If the dot product is greater than the FOV value, the player is within the enemy's FOV.

# AI decision making:
### AI decision making is used to determine what behavior the enemy should be doing.
### The state is determined first, by whether or not a player is detected.
### In the enemy update function, the code is divided by states.
### If the enemy detects a player, change the angle to follow the player.
### If not, set the angle back to standard.