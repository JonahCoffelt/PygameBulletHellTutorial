import pygame as pg
from math import sin, cos
from random import uniform
from particle_shapes import shapes

class Particle:
    def __init__(self, game, x:float=0, y:float=0, velocity:float=5, direction:float=0, curve:float=90, shape:str='square', color:tuple=(255, 255, 255), size:float=.1, life:float=.5) -> None:
        # Reference to the parent game
        self.game = game
        # Initial position of the particle
        self.position = pg.Vector2(x, y)
        # Velocity based on the given direction
        self.velocity = pg.Vector2(velocity * cos(direction), velocity * sin(direction))
        # Curve is the change in direction in degrees per second
        self.curve = curve
        # The shape that the particle will be drawn as
        self.shape = shape
        # The color that the particle will be drawn as 
        self.color = color
        # Scale of the particle for drawing
        self.size = size
        # Time variables
        self.life = life
        self.max_life = life
    
    def update(self):
        """
        Updates the particle direction, position, and life
        """
        
        # Update direction
        self.velocity = self.velocity.rotate(self.curve * self.game.dt)
        # Basic kinematics
        self.position += self.velocity * self.game.dt
        # Update lifetime
        self.life -= self.game.dt

    def draw(self):
        """
        Calls the draw function assigned to the particle
        """
        
        shapes[self.shape](self)

class ParticleHandler:
    def __init__(self, game) -> None:
        # Reference to the parent game
        self.game = game
        # The list of all particles
        self.particles = []

        # A dictionary of args (for the add function) for standard particle effects
        self.effects = {
            'smoke' : [(2, 270, .3, 1, 'circle', (155, 155, 155), .1, .75, 5)]
        }
    
    def add(self, x:float=0, y:float=0, direction:float=0, velocity:float=5, curve:float=180, direction_spread:float=.1, velocity_spread:float=2, shape:str='square', color:tuple=(255, 255, 255), size:float=.1, life:float=.5, num:int=1):
        """
        Adds particles to the particle list. Supports shapes, colors, and multiple particles at once
        """
        
        # The base color for the particle
        color = pg.Vector3(color)
        for i in range(num):
            # Gets random values based on particle ranges
            direction += uniform(-direction_spread, direction_spread)
            velocity += uniform(-velocity_spread, velocity_spread)
            curve = uniform(-curve, curve)
            # Adds a new particle
            self.particles.append(Particle(self.game, x, y, velocity, direction, curve, shape, color + pg.Vector3(uniform(-30, 30)), size, life))

    def add_effect(self, name:str, x:float=0, y:float=0, direction:float=0):
        """
        Adds a prebuilt particle effect
        """
        
        for particle_args in self.effects[name]:
            self.add(x, y, direction, *particle_args)

    def update(self):
        """
        Updates all particles
        """

        i = 0
        while i < len(self.particles):
            self.particles[i].update()
            if self.particles[i].life <= 0:
                self.particles.pop(i)
            else:
                i += 1

    def draw(self):
        """
        Draws all particles to the screen
        """

        for particle in self.particles:
            particle.draw()