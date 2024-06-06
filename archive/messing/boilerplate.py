import pygame as pg


class Game:
    """
    The game class contains most pygame functionality
    """
    def __init__(self) -> None:
        # Initial size of the window, could be used to standardize drawing on any screnn size
        self.win_size = (800, 800)
        
        pg.init()
        # Creates the window. This will be the destination of most drawing
        self.win = pg.display.set_mode(self.win_size, pg.RESIZABLE)
        # Creates a clock. Used for locking framerate and getting change in time between frames (delta time)
        self.clock = pg.Clock()
    
    def update(self) -> None:
        """
        Updates all game logic
        """
        
        self.draw()

    def draw(self) -> None:
        """
        
        """
        
        # Clears the window with the given color
        self.win.fill((0, 0, 255))

        # Displays all that has been drawn to the screen. If this is not called, nothing will be shown
        pg.display.flip()
    
    def start(self) -> None:
        """
        Starts the game
        """
        
        # Determines if the game is running.
        # I like using a bool because it allows us to end the game from anywhere
        self.run = True
        
        # Starts the game loop
        while self.run:
            # Get pygame state variables. These allow us to know what the player is inputting
            self.events = pg.event.get()  # Events include button presses and window events

            for event in self.events:
                if event.type == pg.QUIT:  # Checks if the window close button has been pressed
                    # Stops pygame
                    pg.quit()
                    # Exits the main loop
                    self.run = False
            
            self.update()


# Creates an instance of the game class
game = Game()
# Starts the game
game.start()