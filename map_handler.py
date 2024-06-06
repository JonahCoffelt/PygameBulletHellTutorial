import pygame as pg
from tile_handler import Tile, TileHandler


class MapHandler:
    def __init__(self, game) -> None:
        # Reference to the parent game
        self.game = game
        # Display variables
        self.tile_size = self.game.win_size[1] / self.game.camera.zoom
        self.chunk_size = 5
        # Creat tile hanlder
        self.tile_handler = TileHandler()
        self.tile_handler.adjust_size(self.tile_size)
        # Map data
        self.map = {}
        self.collisions = {}
        # Layers map data
        self.layers = {'collisions' : {}, 'layer1': {}}

        # Add a million tiles
        for x in range(2, 5):
            for y in range(2, 5):
                self.add_collider(x, y)
        
        self.add(2, 4, 'wall_front', 1)
        self.add(3, 4, 'wall_front', 1)
        self.add(4, 4, 'wall_front', 1)
        self.add(2, 3, 'wall_front', 0)
        self.add(3, 3, 'wall_front', 0)
        self.add(4, 3, 'wall_front', 0)
        self.add(2, 2, 'wall_top', 11)
        self.add(3, 2, 'wall_top', 11)
        self.add(4, 2, 'wall_top', 11)

    def add(self, x: float, y: float, tile: str='wall_top', variant: int=0) -> None:
        """
        Add a tile to the map
        """
        
        chunk, relative_position = self.get_chunk_and_pos(x, y)

        # If the chunk does not aready exist, we make a new blank one
        if chunk not in self.map: self.map[chunk] = {}
        # Add the tile
        self.map[chunk][relative_position] = Tile(tile, variant)
    
    def remove(self, x: float, y: float) -> None:
        """
        Remove a tile from the map
        """
        
        chunk, relative_position = self.get_chunk_and_pos(x, y)

        if chunk not in self.map: return None
        if relative_position not in self.map[chunk]: return None

        del self.map[chunk][relative_position]

        if not len(self.map[chunk]): del self.map[chunk]

    def add_collider(self, x: float, y: float) -> None:
        """
        Add a collidable tile to the map
        This tile will not be visible
        """
        
        chunk, relative_position = self.get_chunk_and_pos(x, y)

        # If the chunk does not aready exist, we make a new blank one
        if chunk not in self.collisions: self.collisions[chunk] = {}
        # Add the tile
        self.collisions[chunk][relative_position] = None

    def check_collide(self, x: float, y: float) -> bool:
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

    def get_chunk_and_pos(self, x: float, y: float) -> tuple:
        """
        Gets the chunk key and relative position of a given point
        returns a tuple: (chunk, relative_position)
        """
        
        # Chunk is used as a key for the map dictionary
        chunk = (round(x // self.chunk_size), round(y // self.chunk_size))
        # Tile positions are relative to a chunk, so this is what we will use
        relative_position = (round(x % self.chunk_size), round(y % self.chunk_size))

        return chunk, relative_position

    def get_tile(self, x: float, y: float) -> tuple:
        """
        Get the tile id and variant at a position
        """
        
        chunk, relative_position = self.get_chunk_and_pos(x, y)

        if chunk not in self.map: return (None, None)
        if relative_position not in self.map[chunk]: return (None, None)

        tile = self.map[chunk][relative_position]

        return (tile.id, tile.variant)


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

        # Get the number of chunks on the screen in each axis
        x_range = int((self.game.win_size[0] / self.tile_size / self.chunk_size) // 2) + 1
        y_range = int((self.game.win_size[1] / self.tile_size / self.chunk_size) // 2) + 1

        # Loop through chunks in range
        for chunk_x in range(-x_range, x_range + 1):
            for chunk_y in range(-y_range, y_range + 1):
                # Get the chunk key
                chunk = (chunk_x + player_chunk.x, chunk_y + player_chunk.y)
                # Skip the chunk if it doesnt exist
                if chunk not in self.map: continue
                # Loop through the tiles in the chunk
                for tile in self.map[chunk]:
                    # Get the tile pos. Subtract .5 to center tiles
                    pos = (tile[0] + chunk[0] * self.chunk_size - cam_pos.x - .5, tile[1] + chunk[1] * self.chunk_size - cam_pos.y - .5)
                    # Draw the tile. win_size/2 is to center the map on the screen

                    tile = self.map[chunk][tile]
                    image = self.tile_handler.tiles[tile.id][tile.variant]

                    self.game.win.blit(image, (pos[0] * self.tile_size + self.game.win_size[0]/2, pos[1] * self.tile_size + self.game.win_size[1]/2))