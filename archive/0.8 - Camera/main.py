"""
All code in this project is free to use. 
Full rights to use and sell products made with this code are given.
Credit is appreciated but not necessary.
"""


import pygame as pg
from player import Player
from map_handler import MapHandler
from bullet_handler import BulletHandler
from weapon_handler import WeaponHandler
from particle_handler import ParticleHandler
from camera import Camera


class Game:
    """
    The game class contains most pygame functionality and handlers
    """
    def __init__(self) -> None:
        # Initial size of the window, could be used to standardize drawing on any screen size
        self.win_size = (800, 800)
        
        pg.init()
        # Creates the window. This will be the destination of most drawing
        self.win = pg.display.set_mode(self.win_size, pg.RESIZABLE, vsync=True)
        # Creates a clock. Used for locking framerate and getting change in time between frames (delta time)
        self.clock = pg.Clock()
    
    def update(self) -> None:
        """
        Updates all hanlders
        """
        
        self.player.update()
        self.camera.update()
        self.weapons.update()
        self.bullets.update()
        self.particles.update()

        # Calls draw now that the game has been updated
        self.draw()

    def draw(self) -> None:
        """
        Calls all necessary draw functions and displays the screen
        """
        
        # Clears the window with the given color
        self.win.fill((0, 0, 0))

        # Draw all handlers
        self.map.draw()
        self.bullets.draw()
        self.player.draw()
        self.particles.draw()

        # Displays all that has been drawn to the screen. If this is not called, nothing will be shown
        pg.display.flip()
    
    def start(self) -> None:
        """
        Creats all handlers and starts the game
        """
        
        # Initialize all handlers
        self.player = Player(self)
        self.camera = Camera(self)
        self.map = MapHandler(self)
        self.bullets = BulletHandler(self)
        self.weapons = WeaponHandler(self)
        self.particles = ParticleHandler(self)

        # Determines if the game is running.
        # I like using a bool because it allows us to end the game from anywhere
        self.run = True
        
        # Starts the game loop
        while self.run:
            # Lock the fps and get frame time
            self.dt = self.clock.tick() / 1000
            pg.display.set_caption(str(int(self.clock.get_fps())))
            # Get pygame state variables. These allow us to know what the player is inputting
            self.events = pg.event.get()  # Events include button presses and window events
            self.keys = pg.key.get_pressed()  # A list containing the state of each keyboard button
            self.mouse_pos = pg.mouse.get_pos()  # Tuple of mouse position on the screen (x, y)
            self.mouse_buttons = pg.mouse.get_pressed()  # A tuple with the state of each button on the mouse (left, middle, right)

            # Loop through each event
            for event in self.events:
                if event.type == pg.QUIT:  # Checks if the window close button has been pressed
                    # Stops pygame
                    pg.quit()
                    # Exits the main loop
                    self.run = False
                if event.type == pg.VIDEORESIZE:
                    self.win_size = (event.w, event.h)
                    self.map.tile_size = self.win_size[1] / self.camera.zoom

            # Update the game
            self.update()


# Creates an instance of the game class
game = Game()
# Starts the game
game.start()