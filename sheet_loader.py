import pygame as pg


def load_sheet(path: str, tile_size: int) -> list:
    '''
    Splits a tilesheet into a list of pygame surfaces
    Args:
        path: str
            The relative path of the sheet's image (.png)
        tile_size: int
            Number of pixels for each tile's width and height
    '''

    tiles = []
    sheet_img = pg.image.load(path).convert_alpha()

    size = sheet_img.get_size()
    dimensions = (size[0]//tile_size, size[1]//tile_size)

    # Loop through tiles
    for y in range(0, dimensions[1]):
        for x in range(0, dimensions[0]):
            # Create empty surface of tile size
            tile = pg.Surface((tile_size, tile_size)).convert_alpha()
            tile.fill((0, 0, 0, 0))
            # Blit desired cutout of the sheet image to the surface
            tile.blit(sheet_img, (-x * tile_size, -y * tile_size))

            tiles.append(tile)
    
    return tiles