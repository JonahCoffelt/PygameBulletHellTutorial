import pygame as pg
from random import uniform


class Camera:
    """
    Camera that is tied to an object. Ideal for gameplay and cutscenes
    """
    
    def __init__(self, game) -> None:
        # Reference to the parent game
        self.game = game
        # Number of tiles shown in the y direction
        self.zoom = 10
        # Speed that the camera moves toward target
        self.speed = 9
        # Timer for screen shake
        self.shake = 0
        # Strength of screen shake
        self.magnitude = .75
        # Inital postion and target
        self.position = pg.Vector2(0, 0)
        self.target = None

    def set_target(self, target):
        # Target that the camera will follow
        self.target = self.game.player
        # Initial position of the camera
        self.position = self.target.position.copy()

    def update(self):
        # Move the camera toward target
        if self.target:
            self.position += (self.target.position - self.position) * self.speed * self.game.dt
        # Update shake timer
        self.shake = max(self.shake - self.game.dt, 0)
        # Shake screen
        if self.shake:
            self.position.x += uniform(-self.magnitude, self.magnitude) * self.shake
            self.position.y += uniform(-self.magnitude, self.magnitude) * self.shake



class FreeCamera:
    """
    Camera that is not tied to an object. Ideal for debugging and tools
    """
    
    def __init__(self, game) -> None:
        # Reference to the parent game
        self.game = game
        # Number of tiles shown in the y direction
        self.zoom = 20
        # Inital position
        self.position = pg.Vector2(0, 0)
        # Speed that the camera moves
        self.speed = 20
    
    def update(self):
        """
        Move the camera directly based on user input
        """
        
        # Get keys pressed from the parent game
        keys = self.game.keys
        # Update position
        self.position.x += (keys[pg.K_d] - keys[pg.K_a]) * self.speed * self.game.dt
        self.position.y += (keys[pg.K_s] - keys[pg.K_w]) * self.speed * self.game.dt