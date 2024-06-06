from random import uniform


class Camera:
    def __init__(self, game) -> None:
        # Reference to the parent game
        self.game = game
        # Number of tiles shown in the y direction
        self.zoom = 10
        # Speed that the camera move toward target
        self.speed = 10

        # Target that the camera will follow
        self.target = self.game.player
        # Initial position of the camera
        self.position = self.target.position.copy()

        # Timer for screen shake
        self.shake = 0
        # Strength of screen shake
        self.magnitude = .5

    def update(self):
        # Move the camera toward target
        self.position += (self.target.position - self.position) * self.speed * self.game.dt
        # Update shake timer
        self.shake = max(self.shake - self.game.dt, 0)
        # Shake screen
        if self.shake:
            self.position.x += uniform(-self.magnitude, self.magnitude) * self.shake
            self.position.y += uniform(-self.magnitude, self.magnitude) * self.shake
