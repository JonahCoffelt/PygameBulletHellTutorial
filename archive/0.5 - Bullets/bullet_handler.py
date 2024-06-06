import pygame as pg
from math import sin, cos, atan2

class Bullet:
    def __init__(self, game, x:int=0, y:int=0, direction:int=0, velocity:int=5, acceleration:int=0) -> None:

        # Reference to the parent game
        self.game = game
        # Initial position of the bullet
        self.position = pg.Vector2(x, y)
        # Inital velocity based on the given direction
        self.velocity = pg.Vector2(velocity * cos(direction), velocity * sin(direction))
        # Rate of change of the velocity
        self.acceleration = acceleration
        # Time until the bullet is removed from the game
        self.life = 5
    
    def update(self):
        # Basic kinematics
        self.velocity += pg.Vector2(self.acceleration * self.game.dt)
        self.position += self.velocity * self.game.dt
        # Update lifetime
        self.life -= self.game.dt
        # Check for collision with map
        if self.game.map.check_collide(self.position.x, self.position.y):
            self.life = 0
    
    def draw(self):
        pos = (self.position.x - self.game.player.position.x, self.position.y - self.game.player.position.y)
        tile_size, win_size = self.game.map.tile_size, self.game.win_size
        pg.draw.circle(self.game.win, (200, 200, 200), (pos[0] * tile_size + win_size[0]/2, pos[1] * tile_size + win_size[1]/2), 5)


class BulletHandler:
    def __init__(self, game) -> None:

        ## Reference to the parent game
        self.game = game
        # The list of all bullets
        self.bullets = []
    
    def add(self, x:int=0, y:int=0, direction:int=0, velocity:int=5, acceleration:int=0):
        # Add a new bullet to the list of bullets
        self.bullets.append(Bullet(self.game, x, y, direction, velocity, acceleration))

    def update(self):
        # Add a new bullet if the mouse is pressed
        if self.game.mouse_buttons[0]:
            # Get the players position, this is where the bullet will start
            player_pos = self.game.player.position
            # Get the center of the screen
            center = self.game.win_size[0]/2, self.game.win_size[1]/2
            # Calculate the direction of the bullet based on the mouse position
            direction = atan2(self.game.mouse_pos[1] - center[1], self.game.mouse_pos[0] - center[0])
            # Add the bullet
            self.add(player_pos.x, player_pos.y, direction, 10)

        # Moves all bullets based on velocity and acceleration. Checks for colision
        i = 0
        while i < len(self.bullets):
            self.bullets[i].update()
            if self.bullets[i].life <= 0:
                self.bullets.pop(i)
            else:
                i += 1
    
    def draw(self):
         # Draws all bullets to the screen
         for bullet in self.bullets:
            bullet.draw()