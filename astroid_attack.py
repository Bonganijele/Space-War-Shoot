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
import pygame


pygame.init()
class AstroidAttack(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.width = 35
        self.height = 35
        self.image = pygame.image.load('assets/PNG/10.png')  # Load the asteroid image
        self.image = pygame.transform.scale(self.image, (self.width, self.height))  # Scale it
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 800)
        self.rect.y = random.randint(-self.height, 0)
        self.speed = random.randint(1, 5)
        self.speed = random.uniform(1, 2)
        self.hit = False
        self.drift_x = 0
        self.drift_y = 0
        self.velocity_x = random.randint(-5, 5)  # Initial horizontal velocity
        self.velocity_y = random.randint( 1, 9)  # Initial vertical velocity

        self.deceleration = 0.98  # Deceleration factor for gradual slowdown

    def update_astroid(self):
        if self.hit:
            # Apply velocity and drift (simulating impact)
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y


            self.rect.x += self.drift_x
            self.rect.y += self.drift_y
            self.hit = False  # Reset hit after drifting
           # If the velocity becomes small enough, stop the drifting (simulate frictionless space)

        else:
            self.rect.y += self.speed

        # If asteroid goes off-screen, reset position
        if self.rect.y > 600:
            self.rect.y = -self.height
            self.rect.x = random.randint(0, 800)

    def bounce(self):
        # Reverse the direction of the asteroid to simulate bounce
        self.velocity_x = -self.velocity_x  # Reverse horizontal velocity
        self.velocity_y = -self.velocity_y  # Reverse vertical velocity

        self.drift_x = -self.drift_x
        self.drift_y = -self.drift_y

    def hit_by_missile(self, hit_side):
        self.hit = True

        # Based on the side the spaceship hit the asteroid, apply drift
        if hit_side == 'left':
            self.drift_x = random.randint(3, 6)  # Drift right
            self.drift_y = random.randint(-3, 3)  # Some vertical drift
        elif hit_side == 'right':
            self.drift_x = random.randint(-6, -3)  # Drift left
            self.drift_y = random.randint(-3, 3)
        elif hit_side == 'top':
            self.drift_x = random.randint(-3, 3)  # Some horizontal drift
            self.drift_y = random.randint(3, 6)  # Drift down
        elif hit_side == 'bottom':
            self.drift_x = random.randint(-3, 3)
            self.drift_y = random.randint(-6, -3)  # Drift up
