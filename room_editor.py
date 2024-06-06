import pygame as pg
from camera import FreeCamera
from map_handler import MapHandler
from editor_interface import Interface


class Editor:
    def __init__(self) -> None:
        # Initial size of the window, could be used to standardize drawing on any screen size
        self.win_size = (800, 800)
        
        pg.init()
        # Creates the window. This will be the destination of most drawing
        self.win = pg.display.set_mode(self.win_size, pg.RESIZABLE, vsync=True)
        # Creates a clock. Used for locking framerate and getting change in time between frames (delta time)
        self.clock = pg.Clock()

        # Number of chunks in a room
        self.room_size = 5
    
    def update(self) -> None:

        # Update handlers
        self.camera.update()
        self.interface.update()

        # Main draw call
        self.draw()
    
    def draw(self) -> None:

        # Clear the Screen with black
        self.win.fill((0, 0, 0))

        # Data used for drawing bounding box and grid
        tile_size = self.map.tile_size
        pos = pg.Vector2(-self.camera.position.x * tile_size, -self.camera.position.y * tile_size) + pg.Vector2(self.win_size[0]/2 - tile_size/2, self.win_size[1]/2 - tile_size/2)
        chunk_pixels = self.room_size * tile_size

        # Draw the bounding box for the room
        pg.draw.rect(self.win, (25, 25, 25), pg.Rect(pos.x, pos.y, self.map.chunk_size * chunk_pixels, self.map.chunk_size * chunk_pixels))

        # Draw map tiles
        self.map.draw()

        # Draw chunk gridlines
        for x in range(self.room_size + 1):
            pg.draw.line(self.win, (255, 255, 255), (pos.x + x * chunk_pixels, pos.y), (pos.x + x * self.room_size * tile_size, pos.y + self.map.chunk_size * self.room_size * tile_size))
        
        for y in range(self.room_size + 1):
            pg.draw.line(self.win, (255, 255, 255), (pos.x, pos.y + y * chunk_pixels), (pos.x + self.map.chunk_size * self.room_size * tile_size, pos.y + y * self.room_size * tile_size))

        # Draw the UI elements
        self.interface.draw()

        # Display Changes tot he screen
        pg.display.flip()

    def start(self) -> None:
        # Initialize all handlers
        self.camera = FreeCamera(self)
        self.map = MapHandler(self)
        self.interface = Interface(self)

        self.prev_keys = pg.key.get_pressed()

        self.run = True

        while self.run:
            # Lock the fps and get frame time
            self.dt = self.clock.tick() / 1000
            pg.display.set_caption(str(int(self.clock.get_fps())) + ' : ' + str(self.interface.mouse_grid_pos))
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
                    self.map.tile_handler.adjust_size(self.map.tile_size)
                if event.type == pg.MOUSEWHEEL:
                    self.camera.zoom = max(self.camera.zoom + event.y, 2)
                    self.map.tile_size = self.win_size[1] / self.camera.zoom
                    self.map.tile_handler.adjust_size(self.map.tile_size)
            
            self.update()

            self.prev_keys = self.keys  # A list containing the state of each keyboard button


room_editor = Editor()
room_editor.start()