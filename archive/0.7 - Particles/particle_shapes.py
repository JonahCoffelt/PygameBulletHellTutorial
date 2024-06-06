import pygame as pg


def draw_square(particle):
    """
    Draws a square at a given particle
    """
    
    # Get display vaiables
    tile_size, win_size = particle.game.map.tile_size, particle.game.win_size
    # Get the position of the particle in tiles
    pos = (particle.position.x - particle.game.player.position.x, particle.position.y - particle.game.player.position.y)
    # Get the width/height of the particle
    length = particle.size * tile_size * particle.life/particle.max_life
    # Draw the circle to the screen
    pg.draw.rect(particle.game.win, particle.color, (pos[0] * tile_size + win_size[0]/2 - length/2, pos[1] * tile_size + win_size[1]/2 - length/2, length, length))


def draw_circle(particle):
    """
    Draws a circle at a given particle
    """

    # Get display vaiables
    tile_size, win_size = particle.game.map.tile_size, particle.game.win_size
    # Get the position of the particle in tiles
    pos = (particle.position.x - particle.game.player.position.x, particle.position.y - particle.game.player.position.y)
    # Get the radius of the particle
    radius = particle.size/2 * tile_size * particle.life/particle.max_life
    # Draw the circle to the screen
    pg.draw.circle(particle.game.win, particle.color, (pos[0] * tile_size + win_size[0]/2, pos[1] * tile_size + win_size[1]/2), radius)


# Dictionary to reference the shape functions. This would allow for more shapes to be added/referenced easily
shapes = {
    'square' : draw_square,
    'circle' : draw_circle
}