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
import  math

pygame.mixer.init()

class Bullet:
    __slots__ = ['x', 'y', 'width', 'height', 'speed', 'angle', 'dx', 'dy']
    def __init__(self, x, y, angle, speed=10):
        self.x = x
        self.y = y
        self.width = 5  # Bullet width
        self.height = 10  # Bullet height
        self.speed = speed  # Bullet speed
        self.angle = angle  # Angle at which the bullet is fired

        # # If facing down or up, move vertically (Y-axis movement)
        if self.angle == 0:  # Facing down
            self.dx = 0
            self.dy = self.speed
        elif self.angle == 180:  # Facing up
            self.dx = 0
            self.dy = -self.speed
        elif self.angle == 90:  # Facing right
            self.dx = self.speed
            self.dy = 0
        elif self.angle == 270:  # Facing left
            self.dx = -self.speed
            self.dy = 0
        else:
            self.dx = 0
            self.dy = 0

    def move(self):
        # Move the bullet based on the calculated direction
        self.x += self.dx
        self.y += self.dy

    def draw(self, canvas):
        # Draw a solid red bullet
        pygame.draw.rect(canvas, (255, 0, 10), (self.x, self.y, self.width, self.height), border_radius=5)


class BossEnemy:
    __slots__ = [
        'width', 'x', 'y', 'height', 'health', 'max_health', 'speed',
        'angle', 'image', 'original_image', 'bullets', 'bullet_cooldown', 'exploded',
        'alive', 'explosion_timer', 'movement_direction', 'change_direction_cooldown',
        'explosion_image', 'explosion_sound'
    ]
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.width = 120
        self.height = 80
        self.health = health
        self.max_health = health
        self.speed = 3
        self.angle = 0
        self.image = pygame.image.load('assets/enemies/cargo_ship.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.original_image = self.image
        self.bullets = []
        self.bullet_cooldown = 0
        self.exploded = False  # Track if the boss has exploded
        self.alive = True  # Track if the boss is alive
        self.explosion_timer = 220
        self.movement_direction = random.choice([-1, 1])
        self.change_direction_cooldown = 60

        # Load explosion assets
        try:
            self.explosion_image = pygame.image.load('assets/explosions/expl.png')
            self.explosion_image = pygame.transform.scale(self.explosion_image, (self.width, self.height))
        except Exception as e:
            self.explosion_image = None
            print("Error loading explosion image:", e)

        try:
            self.explosion_sound = pygame.mixer.Sound('music/expl.mp3')
        except Exception as e:
            self.explosion_sound = None
            print("Error loading explosion sound:", e)


    def move_randomly(self, player_x, player_y, screen_width, screen_height):
        # Calculate dx and dy
        dx = player_x - (self.x + self.width // 2)  # Center of the boss sprite
        dy = player_y - (self.y + self.height // 2)  # Center of the boss sprite

        # Calculate angle in degrees (math.atan2 returns radians)
        angle = math.degrees(math.atan2(-dy, dx))  # Negative dy because y-axis is inverted in pygame

        # Rotate the boss sprite
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.width, self.height = self.image.get_size()  # Update size after rotation

        # Normalize dx and dy to ensure smooth movement towards the player
        distance = math.hypot(dx, dy)  # Euclidean distance
        if distance != 0:  # Prevent division by zero
            normalized_dx = (dx / distance) * self.speed
            normalized_dy = (dy / distance) * self.speed
        else:
            normalized_dx, normalized_dy = 0, 0

        # Move the boss
        self.x += normalized_dx
        self.y += normalized_dy

        # Constrain movement within screen boundaries
        top_margin = 50  # Prevent boss from going too high
        bottom_margin = screen_height - 460  # Prevent boss from getting too low
        self.x = max(0, min(self.x, screen_width - self.width))
        self.y = max(top_margin, min(self.y, bottom_margin))

    def shoot(self):
        if not self.alive:
            return

        if self.bullet_cooldown == 0:
            bullet_offsets = [-10, 0, 10]  # Offsets for bullet spread
            bullets_to_add = []

            for offset in bullet_offsets:
                if self.angle == 0:  # Facing down
                    bullet_x = self.x + self.width // 2 - 2.5 + offset
                    bullet_y = self.y + self.height
                elif self.angle == 180:  # Facing up
                    bullet_x = self.x + self.width // 2 - 2.5 + offset
                    bullet_y = self.y - self.height
                elif self.angle == 90:  # Facing right
                    bullet_x = self.x + self.width
                    bullet_y = self.y + self.height // 2 + offset
                elif self.angle == 270:  # Facing left
                    bullet_x = self.x - self.width
                    bullet_y = self.y + self.height // 2 + offset
                else:
                    continue  # Skip invalid angles

                bullets_to_add.append(Bullet(bullet_x, bullet_y, self.angle))

            # Add bullets to the boss's bullet list
            self.bullets.extend(bullets_to_add)

            # Set cooldown
            self.bullet_cooldown = 30  # Cooldown period before the next shot

    def update_bullet_cooldown(self):
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1

    def update_bullets(self, canvas, player_x, player_y, player_width, player_height):
        for bullet in self.bullets[:]:
            bullet.move()
            bullet.draw(canvas)

            # Check collision with the player's ship
            if (
                    player_x < bullet.x + bullet.width and
                    player_x + player_width > bullet.x and
                    player_y < bullet.y + bullet.height and
                    player_y + player_height > bullet.y
            ):
                print("Player hit by boss bullet!")
                self.bullets.remove(bullet)  # Remove bullet on collision
                return True  # Indicate collision to reduce player health

    def remove_bullets(self):
        self.bullets = [bullet for bullet in self.bullets if bullet.y <= 600]

    def draw(self, canvas):
        if self.exploded:
            if self.explosion_image and self.explosion_timer > 0:
                canvas.blit(self.explosion_image, (self.x, self.y))
                self.explosion_timer -= 1
            return

        if not self.alive:
            return


        canvas.blit(self.image, (self.x, self.y))

        health_bar_width = 100
        health_bar_height = 10
        health_bar_x = self.x + (self.width - health_bar_width) // 2
        health_bar_y = self.y - 15
        pygame.draw.rect(canvas, (169, 169, 169), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), border_radius=3)
        current_health_width = (self.health / self.max_health) * health_bar_width
        pygame.draw.rect(canvas, (255, 0, 0), (health_bar_x, health_bar_y, current_health_width, health_bar_height), border_radius=3)

        self.update_bullet_cooldown()
        for bullet in self.bullets:
            bullet.move()
            bullet.draw(canvas)
        self.remove_bullets()

    def handle_explosion(self):
        if self.health <= 0 and not self.exploded:
            self.exploded = True
            if self.explosion_sound:
                self.explosion_sound.play()
            print("Explosion triggered!")
            self.alive = False  # Mark the boss as dead

    def respawn(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.alive = True
        self.exploded = False
        self.explosion_timer = 100  # Reset the explosion timer

    def check_respawn(self, score):
        if self.exploded and score >= 4000:
            print("Score reached 4000! Respawning boss...")
            self.respawn(x=350, y=100, health=300)  # Respawn the boss

    def check_bullet_collision(self, bullets):
        for bullet in bullets:
            if bullet.x + bullet.width > self.x and bullet.x < self.x + self.width and \
            bullet.y + bullet.height > self.y and bullet.y < self.y + self.height:
                self.health -= 5
                bullets.remove(bullet)
                if self.health <= 0:
                    self.handle_explosion()
                break

