import pygame as pg
from sheet_loader import load_sheet


states = {14: 0, 62: 1, 56: 2, 248: 7, 224: 12, 227: 11, 131: 10, 143: 5, 255: 6, 254: 3, 191: 4, 251: 8, 239: 9, 7: 5, 28: 1, 138: 6, 193: 11, 30: 2, 31: 0, 15: 0, 120: 2, 124: 2, 60: 2, 240: 12, 241: 12, 225: 12, 195: 10, 199: 10, 135: 10, 207: 5, 159: 5, 126: 1, 63: 1, 249: 7, 252: 7, 231: 11, 243: 11, 223: 5, 127: 1, 253: 7, 247: 11}


class Tile:
    def __init__(self, id: str, variant: int=0) -> None:
        self.id = id
        self.variant = variant


class TileHandler:
    def __init__(self) -> None:
        # Blank dictionary which will hold tiles and variants
        self.original_tiles = {}
        self.tiles = {}
        # Add tile types
        self.add('wall_top', 'assets\wall_top.png')
        self.add('wall_front', 'assets\wall_front.png')
        self.add('ground', 'assets\ground.png')
    
    def add(self, name: str, path: str, tile_size: int=8):
        """
        Load a tile sheet into the tiles dictionary
        """
        
        self.original_tiles[name] = load_sheet(path, tile_size)
        self.tiles[name] = self.original_tiles[name].copy()
    
    def adjust_size(self, tile_size: int):
        for tile_type in self.original_tiles:
            for index, image in enumerate(self.original_tiles[tile_type]):
                self.tiles[tile_type][index] = pg.transform.scale(image, (tile_size + 1, tile_size + 1))

    def update_tiles_in_range(self, map, id, x, y):
        for rel_x in range(-1, 2):
            for rel_y in range(-1, 2):
                if map.get_tile(x + rel_x, y + rel_y)[0] != id: continue

                rule_variant = map.tile_handler.get_tile_variant(map, id, x + rel_x, y + rel_y)
                if rule_variant >= len(map.tile_handler.tiles[id]): continue

                map.add(x + rel_x, y + rel_y, id, rule_variant)

    def get_tile_variant(self, map, id, x, y):
        """
        Get the variant of a tile based on neighbors
        """
        
        state = 0

        state = state | int(map.get_tile(x + 1, y - 1)[0] == id) << 0
        state = state | int(map.get_tile(x + 1, y    )[0] == id) << 1
        state = state | int(map.get_tile(x + 1, y + 1)[0] == id) << 2
        state = state | int(map.get_tile(x    , y + 1)[0] == id) << 3
        state = state | int(map.get_tile(x - 1, y + 1)[0] == id) << 4
        state = state | int(map.get_tile(x - 1, y    )[0] == id) << 5
        state = state | int(map.get_tile(x - 1, y - 1)[0] == id) << 6
        state = state | int(map.get_tile(x    , y - 1)[0] == id) << 7

        if state not in states: return 6

        return states[state]
