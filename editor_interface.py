import pygame as pg
from math import floor
from random import randrange


class Interface:
    def __init__(self, editor) -> None:
        # Reference to the parent game
        self.editor = editor
        # The grid position of the mouse. Used for drawing and UI
        self.mouse_grid_pos = (0, 0)
        # Tool for tiling
        self.tool = 'draw'
        # Drawing tile
        self.tile_index = 0
        self.tile = 'wall_top'
        self.variant = 0
    
    def draw(self):

        if not (0 <= self.mouse_grid_pos[0] < self.editor.room_size * self.editor.map.chunk_size and 
                0 <= self.mouse_grid_pos[1] < self.editor.room_size * self.editor.map.chunk_size): return

        selected_tile_image = self.editor.map.tile_handler.tiles[self.tile][self.variant]

        pos = (pg.Vector2(self.mouse_grid_pos) - self.editor.camera.position) * self.editor.map.tile_size
        pos.x += self.editor.win_size[0] / 2 - self.editor.map.tile_size / 2
        pos.y += self.editor.win_size[1] / 2 - self.editor.map.tile_size / 2

        self.editor.win.blit(selected_tile_image, pos)

    def check_key_inputs(self):
        # Up and Down control the variant of the draw tile
        if self.editor.keys[pg.K_UP] and not self.editor.prev_keys[pg.K_UP]:
            self.variant += 1
            if self.variant == len(self.editor.map.tile_handler.tiles[self.tile]):
                self.variant = 0
        if self.editor.keys[pg.K_DOWN] and not self.editor.prev_keys[pg.K_DOWN]:
            self.variant -= 1
            if self.variant < 0:
                self.variant = len(self.editor.map.tile_handler.tiles[self.tile]) - 1


        # Get the tile types from the tile_handler
        tiles = list(self.editor.map.tile_handler.tiles.keys())

        # Left and right control the tile type
        if self.editor.keys[pg.K_RIGHT] and not self.editor.prev_keys[pg.K_RIGHT]:
            # Incrament the tile index and loop to 0 if needed
            self.tile_index += 1
            if self.tile_index == len(tiles):
                self.tile_index = 0
            # Reset variant 
            self.variant = 0
        if self.editor.keys[pg.K_LEFT] and not self.editor.prev_keys[pg.K_LEFT]:
            # Decrement the tile index and loop to top if needed
            self.tile_index -= 1
            if self.tile_index < 0:
                self.tile_index = len(tiles) - 1
            # Reset variant 
            self.variant = 0
            
        # Set the tile based on the index
        self.tile = tiles[self.tile_index]

        # Check for tool keys
        if self.editor.keys[pg.K_b]:
            self.tool = 'draw'
        if self.editor.keys[pg.K_t]:
            self.tool = 'auto'
        if self.editor.keys[pg.K_r]:
            self.tool = 'random'

    def update(self) -> None:
        self.mouse_grid_pos  = (floor((self.editor.mouse_pos[0] - self.editor.win_size[0]/2 + self.editor.map.tile_size/2) / self.editor.map.tile_size + self.editor.camera.position.x), 
                                floor((self.editor.mouse_pos[1] - self.editor.win_size[1]/2 + self.editor.map.tile_size/2) / self.editor.map.tile_size + self.editor.camera.position.y))

        self.check_key_inputs()

        if self.editor.mouse_buttons[0] and (0 <= self.mouse_grid_pos[0] < self.editor.room_size * self.editor.map.chunk_size and 0 <= self.mouse_grid_pos[1] < self.editor.room_size * self.editor.map.chunk_size):
            if self.tool == 'draw':
                self.editor.map.add(*self.mouse_grid_pos, self.tile, self.variant)
            if self.tool == 'auto':
                self.editor.map.add(*self.mouse_grid_pos, self.tile, self.variant)
                self.editor.map.tile_handler.update_tiles_in_range(self.editor.map, self.tile, self.mouse_grid_pos[0], self.mouse_grid_pos[1])
            if self.tool == 'random':
                self.editor.map.add(*self.mouse_grid_pos, self.tile, randrange(0, len(self.editor.map.tile_handler.tiles.keys())))

        if self.editor.mouse_buttons[2]:
            self.editor.map.remove(*self.mouse_grid_pos)

            if self.tool == 'auto':
                self.editor.map.tile_handler.update_tiles_in_range(self.editor.map, self.tile, self.mouse_grid_pos[0], self.mouse_grid_pos[1])