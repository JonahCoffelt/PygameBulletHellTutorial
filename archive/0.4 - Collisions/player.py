import pygame as pg

class Player:
    def __init__(self, game, x:int=0, y:int=0) -> None:
        # Reference to the parent game
        self.game = game
        # The initial position of the player. This is a list because it needs to be mutable
        self.position = pg.Vector2(x, y)
        # Player movement variables
        self.velocity = pg.Vector2(0, 0)  # Tiles per second
        self.speed = 10  # Tiles per second
        self.acceleration = 10  # Tiles per second^2
        # Player size
        self.size = pg.Vector2(.75, 1) # Tiles

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

        # Linearly interpolates velocity toward the target velocity
        self.velocity += (target_velocity - self.velocity) * self.acceleration * self.game.dt

        # Gets projected player position based on current velocity
        projected_position = self.position + self.velocity * self.game.dt
        collide_x, collide_y = False, False

        # We check each corner of the player for collision
        hit_points = (pg.Vector2(self.size.x / 2, self.size.y / 2), pg.Vector2(-self.size.x / 2, -self.size.y / 2), 
                      pg.Vector2(-self.size.x / 2, self.size.y / 2), pg.Vector2(self.size.x / 2, -self.size.y / 2))

        # Loop through each corner
        for hit_point in hit_points:
            # Gets the positions of the projected corner position in each axis
            x_position_check = pg.Vector2(projected_position.x, self.position.y) + hit_point
            y_position_check = pg.Vector2(self.position.x, projected_position.y) + hit_point
            # Checks for collisions
            if self.game.map.check_collide(x_position_check.x, x_position_check.y): collide_x = True
            if self.game.map.check_collide(y_position_check.x, y_position_check.y): collide_y = True

        # Updates position and velocity based on collisions. Snaps to grid if there is a collision
        if collide_x: 
            # Snap tp grid on x axis
            if self.velocity.x > 0:
                self.position.x = round(projected_position.x + self.size.x / 2) - (1 + self.size.x) / 2  - .001
            if self.velocity.x < 0:
                self.position.x = round(projected_position.x - self.size.x / 2) + (1 + self.size.x) / 2  + .001
            self.velocity.x = 0
        else: 
            # No collision, so set x to projected x
            self.position.x = projected_position.x
        if collide_y:
            # Snap tp grid on y axis
            if self.velocity.y > 0:
                self.position.y = round(projected_position.y + self.size.y / 2) - (1 + self.size.y) / 2  - .001
            if self.velocity.y < 0:
                self.position.y = round(projected_position.y - self.size.y / 2) + (1 + self.size.y) / 2  + .001
            self.velocity.y = 0
        else: 
            # No collision, so set y to projected y
            self.position.y = projected_position.y
    
    def draw(self) -> None:

        tile_size = self.game.map.tile_size
        w, h = tile_size * self.size.x, tile_size * self.size.y
        pg.draw.rect(self.game.win, (255, 0, 0), (self.game.win_size[0]/2 - w/2, self.game.win_size[1]/2 - h/2, w, h))