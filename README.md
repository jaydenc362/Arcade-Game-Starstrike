Hi!

I proudly present:
STARSTRIKER: PYTHON EDITION

A remake of the classic 2026 BXSCI AtomHacks XII scratch.mit.edu submission STARSTRIKER

This rendition takes many of BXSCI AI Coding teacher Ms. Qiu's labs into one simple game,
combining meteor objects and collisions with NPC detection.

Controls:
- WASD / ARROWS to move
- SPACE to shoot
- TAB to enable hitboxes

I am aware of any bugs that I cannot fix caused by Pygame. I understand I could fix them, but I do not possess the knowledge to do so.

============================
UNIT 2 MATH & AI EXPLANATION
============================

Vectors:
- Vectors are used here to store the positions and velocities of objects.
- Their components are used to calculate collisions too.

Distance:
- Distance is used to calculate whether or not an enemy is within range of the player.
- Distance is used to calculate collisions too.

Normalization:
- Normalization is used to find the direction where objects would bounce after colliding.
- These normalized vectors are multiplied by a customized factor to create a knockback velocity vector.
- The knockback velocity vector is then added to the velocity of the object bouncing away.

Angles / sine / cosine:
- Angles are used to make enemies move towards the player when detected.
- The angle is calculated first for its components to be used.
- Sine affects the X velocity, while cosine affects the Y velocity.

Velocity and acceleration:
- Acceleration is stored as a scalar.
- Acceleration is added to the player and enemies velocities.
- Finally, velocity is added to the object's position.
- This makes movement smooth.

Dot product:
- Dot product is used to calculate if the enemy can see the player within it's FOV.
- The dot product is compared to the FOV value.
- If the dot product is greater than the FOV value, the player is within the enemy's FOV.

AI decision making:
- AI decision making is used to determine what behavior the enemy should be doing.
- The state is determined first, by whether or not a player is detected.
- In the enemy update function, the code is divided by states.
- If the enemy detects a player, change the angle to follow the player.
- If not, set the angle back to standard.

Thank you for playing.
- Jayden
