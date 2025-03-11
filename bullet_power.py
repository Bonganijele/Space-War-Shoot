# Copyright (c) 2025, Bongani. All rights reserved.
# This file is part of the Space War Shoot project.
# Author: Bongani Jele <jelebongani43@gmail.com>

########################################################################################
# Pygame doc: https://www.pygame.org/docs/ref/rect.html                                #
#                                                                                      #
# For just in case if you experience issues Email me or                                #
# contribute to github I'll appreciate support                                         #
#                                                                                      #
########################################################################################


import random
import time
import sys
import pygame

class BulletPower:
    __slots__ = ['x', 'y', 'width', 'height', 'speed', 'image', 'bullet_up_sound']
    def __init__(self, screen_width, screen_height ):
        self.width = 50
        self.height = 50
        self.x = random.randint(0, screen_width - self.width)
        self.y = random.randint(-100, -40)
        self.speed = random.randint(2,2)
        self.image = pygame.image.load('assets/bullet/bullet.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # Load the power-up sound when the object is initialized
        try:
            self.bullet_up_sound = pygame.mixer.Sound("music/bonus-earned.mp3")  # Replace with your sound file path
        except Exception as e:
            self.bullet_up_sound = None
            print("Error loading power-up sound:", e)

    def activate_bullet_power_up(self):
        if self.bullet_up_sound:
            self.bullet_up_sound.play()
      
    def move(self):
        self.y += self.speed  # Move the power charge downward

    def draw(self, canvas):
        canvas.blit(self.image, (self.x, self.y))  # Draw the power charge on the screen

    def is_off_screen(self, screen_height):
        return self.y > screen_height  # Return True if it goes below the screen

    def check_collision(self, ship_x, ship_y, ship_width, ship_height):
        # Check for collision with the ship
        return (
            self.x < ship_x + ship_width
            and self.x + self.width > ship_x
            and self.y < ship_y + ship_height
            and self.y + self.height > ship_y
        )
        