import pygame as pg
from math import sin, cos, atan2
from random import uniform


class Bullet:
    def __init__(self, game, x:float=0, y:float=0, direction:float=0, velocity:float=5, acceleration:float=0, size:int=.05, life:float=5) -> None:
        # Reference to the parent game
        self.game = game
        # Initial position of the bullet
        self.position = pg.Vector2(x, y)
        # Inital velocity based on the given direction
        self.velocity = pg.Vector2(velocity * cos(direction), velocity * sin(direction))
        # Rate of change of the velocity
        self.acceleration = pg.Vector2(acceleration * cos(direction), acceleration * sin(direction))
        # Radius of the circle of the bullet
        self.size = size
        # Time until the bullet is removed from the game
        self.life = life
    
    def update(self):
        """
        Moves the bullet based on kinematic variables, updates life, and checks for collision
        """
        
        # Basic kinematics
        self.velocity += self.acceleration * self.game.dt
        self.position += self.velocity * self.game.dt
        # Update lifetime
        self.life -= self.game.dt
        # Check for collision with map
        if self.game.map.check_collide(self.position.x, self.position.y):
            self.life = 0
    
    def draw(self):
        """
        Draws the bullet to the parent games window
        """
        
        # Get display vaiables
        tile_size, win_size = self.game.map.tile_size, self.game.win_size
        # Get the position of the bullet in tiles
        pos = (self.position.x - self.game.player.position.x, self.position.y - self.game.player.position.y)
        # Draw the bullet, centered to the screen
        pg.draw.circle(self.game.win, (200, 200, 200), (pos[0] * tile_size + win_size[0]/2, pos[1] * tile_size + win_size[1]/2), self.size * tile_size)


class BulletHandler:
    def __init__(self, game) -> None:
        # Reference to the parent game
        self.game = game
        # The list of all bullets
        self.bullets = []
    
    def add(self, x:int=0, y:int=0, direction:int=0, velocity:int=5, acceleration:int=0, size:int=.05, life:float=5):
        """
        Add a new bullet to the list of bullets
        """
        
        self.bullets.append(Bullet(self.game, x, y, direction, velocity, acceleration, size, life))

    def update(self):
        """
        Updates each bullet and checks if the player is firing new bullets
        """
        
        # Add a new bullet if the mouse is pressed
        if self.game.mouse_buttons[0] and self.game.weapons.current_weapon and not self.game.weapons.current_weapon.cooldown:
            # Get the players position, this is where the bullet will start
            player_pos = self.game.player.position
            # Get the selected weapon
            weapon = self.game.weapons.current_weapon
            # Get the center of the screen
            center = self.game.win_size[0]/2, self.game.win_size[1]/2

            # Calculate the direction of the bullet based on the mouse position
            direction = atan2(self.game.mouse_pos[1] - center[1], self.game.mouse_pos[0] - center[0])

            # Add the bullets
            for bullet in range(weapon.burst):
                self.add(player_pos.x, player_pos.y, direction + uniform(-weapon.direction_spread, weapon.direction_spread), 
                        weapon.velocity + uniform(-weapon.velocity_spread, weapon.velocity_spread), weapon.acceleration, weapon.size, weapon.life)
            
            # Set the weapon cooldown
            weapon.cooldown = weapon.reload_time

        # Moves all bullets based on velocity and acceleration. Checks for colision
        i = 0
        while i < len(self.bullets):
            self.bullets[i].update()
            if self.bullets[i].life <= 0:
                self.bullets.pop(i)
            else:
                i += 1
    
    def draw(self):
        """
        Draws all bullets to the screen
        """

        for bullet in self.bullets:
            bullet.draw()