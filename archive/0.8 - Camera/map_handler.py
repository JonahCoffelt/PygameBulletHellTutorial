import pygame as pg

class MapHandler:
    def __init__(self, game) -> None:
        # Reference to the parent game
        self.game = game
        # Display variables
        self.tile_size = self.game.win_size[1] / self.game.camera.zoom
        self.chunk_size = 5
        # Map data
        self.map = {}
        self.collisions = {}

        # Add a million tiles
        for x in range(2, 5):
            for y in range(2, 5):
                self.add(x, y)
                self.add_collider(x, y)

    def add(self, x:int, y:int) -> None:
        """
        Add a tile to the map
        """
        
        chunk, relative_position = self.get_chunk_and_pos(x, y)

        # If the chunk does not aready exist, we make a new blank one
        if chunk not in self.map: self.map[chunk] = {}
        # Add the tile
        self.map[chunk][relative_position] = None
    
    def add_collider(self, x, y) -> None:
        """
        Add a collidable tile to the map
        This tile will not be visible
        """
        
        chunk, relative_position = self.get_chunk_and_pos(x, y)

        # If the chunk does not aready exist, we make a new blank one
        if chunk not in self.collisions: self.collisions[chunk] = {}
        # Add the tile
        self.collisions[chunk][relative_position] = None

    def check_collide(self, x, y) -> bool:
        """
        Checks if there is a collision point at a given point
        Returns True if there is a collions, otherwise returns false
        """
        
        chunk, relative_position = self.get_chunk_and_pos(x, y)

        # Checks if the chunk exists
        if chunk not in self.collisions: return False
        # If the tile is in the chunk, then there is a collision
        if relative_position in self.collisions[chunk]: return True
        return False

    def get_chunk_and_pos(self, x, y) -> tuple:
        """
        Gets the chunk key and relative position of a given point
        returns a tuple: (chunk, relative_position)
        """
        
        # Chunk is used as a key for the map dictionary
        chunk = (round(x // self.chunk_size), round(y // self.chunk_size))
        # Tile positions are relative to a chunk, so this is what we will use
        relative_position = (round(x % self.chunk_size), round(y % self.chunk_size))

        return chunk, relative_position

    def draw(self) -> None:
        """
        Draws all the in range tiles to the parent game's window
        """
        
        # Gets the player position to scroll the tiles to the right position
        cam_pos = self.game.camera.position
        player_chunk = cam_pos // self.chunk_size

        # Create a dummy tile
        tile_image = pg.Surface((self.tile_size - 1, self.tile_size - 1)).convert()
        tile_image.fill((0, 0, 255))

        # Loop through chunks in range
        for chunk_x in range(-2, 3):
            for chunk_y in range(-2, 3):
                # Get the chunk key
                chunk = (chunk_x + player_chunk.x, chunk_y + player_chunk.y)
                # Skip the chunk if it doesnt exist
                if chunk not in self.map: continue
                # Loop through the tiles in the chunk
                for tile in self.map[chunk]:
                    # Get the tile pos. Subtract .5 to center tiles
                    pos = (tile[0] + chunk[0] * self.chunk_size - cam_pos.x - .5, tile[1] + chunk[1] * self.chunk_size - cam_pos.y - .5)
                    # Draw the tile. win_size/2 is to center the map on the screen
                    self.game.win.blit(tile_image, (pos[0] * self.tile_size + self.game.win_size[0]/2, pos[1] * self.tile_size + self.game.win_size[1]/2))