import pygame as pg
from random import uniform
from math import atan2


class Weapon:
    def __init__(self, velocity:float=5, acceleration:float=0, direction_spread:float=.1, velocity_spread:float=.1, reload_time:float=.1, burst:int=1, size:int=.05, life:float=5) -> None:
        # Various attribs which determin how a bullet will fire
        self.velocity = velocity
        self.acceleration = acceleration
        self.direction_spread = direction_spread
        self.velocity_spread = velocity_spread
        self.reload_time = reload_time
        self.burst = burst
        self.size = size
        self.life = life
        # Cooldown timer
        self.cooldown = 0


class WeaponHandler:
    def __init__(self, game) -> None:
        # Reference to the parent game
        self.game = game
        # List of all weapons the player has
        self.weapons = {}
        # self.current
        self.current_weapon = None
        # Add sample weapons (for testing)
        self.add('pistol', velocity=10, size=0.08)
        self.add('minigun', velocity=15, direction_spread=.2, velocity_spread=2, reload_time=.05)
        self.add('shotgun', velocity=15, acceleration=-3, direction_spread=.5, velocity_spread=1, reload_time=.5, burst=8, size=.1)
        self.add('sniper', velocity=25, direction_spread=.01, reload_time=.8, size=.07)
        self.add('rocket', velocity=0, acceleration=15, direction_spread=.01, reload_time=1.5, size=.25)
    
    def add(self, name, velocity:float=5, acceleration:float=0, direction_spread:float=.1, velocity_spread:float=.1, reload_time:float=.1, burst:int=1, size:int=.05, life:float=5) -> None:
        """
        Adds a new weapon and equips it
        """
        
        # Add new weapon object to the wepons list
        self.weapons[name] = Weapon(velocity, acceleration, direction_spread, velocity_spread, reload_time, burst, size, life)
        # Equip the new weapon
        self.equip(name)
    
    def equip(self, name:str):
        """
        Equips a weapon if it exists
        """

        if name in self.weapons: self.current_weapon = self.weapons[name]

    def update(self):
        """
        Updates weapon cooldown and checks for player weapon input
        """
        
        # Update the cooldown of each weapon
        for weapon in self.weapons.values():
            weapon.cooldown = max(weapon.cooldown - self.game.dt, 0)
        
        # Check inputs for a number press
        for num_key_code in range(pg.K_1, pg.K_9):
            if self.game.keys[num_key_code]:
                # Get the number of the key pressed
                number_pressed = num_key_code - pg.K_1
                # Check if there is a weapon associated with the key
                if number_pressed >= len(self.weapons): continue
                # Get the weapon from weapons list
                selection = list(self.weapons.keys())[number_pressed]
                # Equip the weapon
                self.equip(selection)
        
        # Add a new bullet if the mouse is pressed
        if self.game.mouse_buttons[0] and self.current_weapon and not self.current_weapon.cooldown:
            # Get the players position, this is where the bullet will start
            player_pos = self.game.player.position
            # Get the selected weapon
            weapon = self.current_weapon
            # Get the position of the player on the screen as the center
            offset = (player_pos - self.game.camera.position) * self.game.map.tile_size
            center = self.game.win_size[0]/2 + offset.x, self.game.win_size[1]/2 + offset.y

            # Calculate the direction of the bullet based on the mouse position
            direction = atan2(self.game.mouse_pos[1] - center[1], self.game.mouse_pos[0] - center[0])

            # Add the bullets
            for bullet in range(weapon.burst):
                self.game.bullets.add(player_pos.x, player_pos.y, direction + uniform(-weapon.direction_spread, weapon.direction_spread), 
                        weapon.velocity + uniform(-weapon.velocity_spread, weapon.velocity_spread), weapon.acceleration, weapon.size, weapon.life)
            
            # Set the weapon cooldown
            weapon.cooldown = weapon.reload_time