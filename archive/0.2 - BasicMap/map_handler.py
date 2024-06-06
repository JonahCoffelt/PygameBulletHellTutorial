import pygame as pg

class MapHandler:
    def __init__(self, game) -> None:
        # Reference to the parent game
        self.game = game
        # Display variables
        self.tile_size = self.game.win_size[1] / 10
        # Map data
        self.map = {}
        self.map[(1, 1)] = None
        self.map[(1, 2)] = None

    def draw(self) -> None:
        # Gets the player position to scroll the tiles to the right position
        player_pos = self.game.player.position
        for tile in self.map:
            # Get the tile pos. Subtract .5 to center tiles
            pos = (tile[0] - player_pos.x - .5, tile[1] - player_pos.y - .5)
            # Does not draw a tile if it is too far
            if abs(pos[0]) > 15 or abs(pos[1]) > 15: continue
            # Draw the tile. win_size/2 is to center the map on the screen
            pg.draw.rect(self.game.win, (0, 0, 255), (pos[0] * self.tile_size + self.game.win_size[0]/2, pos[1] * self.tile_size + self.game.win_size[1]/2, self.tile_size + 1, self.tile_size + 1))