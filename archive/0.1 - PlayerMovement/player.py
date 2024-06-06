import pygame as pg

class Player:
    def __init__(self, game, x=0, y=0) -> None:
        # Reference to the parent game
        self.game = game
        # The initial position of the player. This is a list because it needs to be mutable
        self.position = pg.Vector2(x, y)
        # Player movement variables
        self.velocity = pg.Vector2(0, 0)  # Tiles per second
        self.speed = 10  # Tiles per second
        self.acceleration = 10  # Tiles per second^2

    def update(self) -> None:
        """
        Handles player inputs/movement
        """

        # Get inputs from parent game
        keys = self.game.keys
        # Velocity to accelerate towards
        target_velocity = pg.Vector2(0, 0)

        # Updates the velocity if a movement key is pressed
        target_velocity.x = self.speed * (keys[pg.K_d] - keys[pg.K_a])
        target_velocity.y = self.speed * (keys[pg.K_s] - keys[pg.K_w])

        # This corrects diagonal movement speed
        if target_velocity.x and target_velocity.y:
            target_velocity *= .7

        # Linear interpolates velocity toward the target velocity
        self.velocity += (target_velocity - self.velocity) * self.acceleration * self.game.dt

        # Moves the player based on current velocity
        self.position += self.velocity * 50 * self.game.dt
    
    def draw(self) -> None:
        pg.draw.rect(self.game.win, (255, 0, 0), (self.position.x, self.position.y, 50, 50))