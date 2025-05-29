# Meteor Rush 🚀

A fast-paced space shooter game built with Pygame where you pilot a spaceship through an endless meteor field, surviving as long as possible while racking up points!

## Introduction

Meteor Rush is an arcade-style space survival game that puts you in control of a nimble spaceship navigating through a dangerous asteroid field. Your mission is simple: survive as long as possible while shooting down incoming meteors. The longer you survive, the higher your score climbs!

The game features smooth sprite-based graphics, particle effects, sound effects, and background music to create an immersive space combat experience.

## Game Mechanics

### Core Gameplay Loop
1. **Movement**: Control your spaceship using arrow keys to dodge incoming meteors
2. **Shooting**: Fire lasers with the spacebar to destroy meteors before they hit you
3. **Survival**: Avoid collisions with meteors to stay alive
4. **Scoring**: Your score increases based on survival time (every 0.1 seconds = 1 point)

### Controls
- **Arrow Keys**: Move your spaceship (Up, Down, Left, Right)
- **Spacebar**: Fire laser shots
- **Close Window**: End the game

### Visual Effects
- **Rotating Meteors**: Meteors spin as they fall, adding visual appeal
- **Explosion Animations**: Destroyed meteors create animated explosion effects
- **Starfield Background**: Static stars create a space atmosphere
- **Laser Cooldown**: Visual feedback prevents laser spam

### Audio
- **Laser Sound**: Plays when firing lasers
- **Explosion Sound**: Plays when meteors are destroyed
- **Damage Sound**: Plays when hit by meteors
- **Background Music**: Continuous ambient space music

## Game Rules & Mechanics

### Lives System
- **One Life Only**: The game currently uses a single-life system
- **Instant Game Over**: Any collision with a meteor ends the game immediately
- **No Respawning**: Once hit, the game terminates

### Scoring System
- **Time-Based Scoring**: Score = survival time in deciseconds (0.1 second intervals)
- **Formula**: `current_time = pygame.time.get_ticks() // 100`
- **Display**: Score appears at the bottom center of the screen in a white bordered box
- **No Bonus Points**: Currently no additional points for destroying meteors

### Meteor Behavior
- **Spawn Rate**: New meteors appear every 150 milliseconds
- **Spawn Location**: Random X position at the top, Y position between -200 and -100 pixels
- **Movement**: Meteors move downward with slight horizontal drift
- **Speed**: Random speed between 400-500 pixels per second
- **Lifetime**: Meteors auto-destroy after 3 seconds if not hit
- **Rotation**: Each meteor rotates at 40-60 degrees per second

### Laser Mechanics
- **Cooldown**: 300 milliseconds between shots
- **Speed**: Lasers travel at 400 pixels per second upward
- **Auto-Cleanup**: Lasers disappear when leaving the screen
- **Collision**: Lasers are destroyed when hitting meteors

## Code Modifications Guide

### Changing Number of Lives

The game currently has a single-life system, but you can easily implement multiple lives:

```python
# At the top of your code, add a lives system
num_collisions = 3  # Start with 3 lives

# In the collision detection section, replace:
collision_Sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)  
if collision_Sprites: 
    damage_sound.play() 
    running = False

# With this multi-life system:
collision_Sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)  
if collision_Sprites: 
    num_collisions -= 1  
    damage_sound.play() 
    if num_collisions <= 0: 
        running = False
```

You can also display the remaining lives on screen:

```python
def display_lives():
    lives_text = font.render(f"Lives: {num_collisions}", True, 'white')
    lives_rect = lives_text.get_frect(topleft=(20, 20))
    display_surface.blit(lives_text, lives_rect)

# Add this to your main game loop
display_lives()
```

### Adjusting Meteor Spawn Rate

Change the meteor spawn frequency by modifying the timer value:

```python
# Current setting (fast-paced)
pygame.time.set_timer(meteor_event, 150)  # New meteor every 150ms

# Easier difficulty (slower spawn rate)
pygame.time.set_timer(meteor_event, 300)  # New meteor every 300ms

# Harder difficulty (faster spawn rate)
pygame.time.set_timer(meteor_event, 100)  # New meteor every 100ms

# Extreme difficulty
pygame.time.set_timer(meteor_event, 50)   # New meteor every 50ms
```

## Further upcoming add-ons to the game

1. **Power-ups**: Add temporary invincibility, rapid-fire, or shield power-ups
2. **Different Meteor Types**: Create meteors with different sizes, speeds, and point values
3. **High Score System**: Save and display the best survival times
4. **Particle Effects**: Add thruster particles behind the player ship
5. **Screen Boundaries**: Keep the player within screen bounds
6. **Progressive Difficulty**: Gradually increase meteor spawn rate over time

Happy coding and enjoy your Meteor Rush adventure! 🌟