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


class BossEnemy2:
    __slots__ = ['x', 'y', 'width', 'height', 'health', 'max_health', 'speed', 'movement_direction', 'shield_active', 'shield_timer',
                 'max_shield_time', 'shield_value', 'shield_image', 'bullets',
                 'angle', 'missiles', 'bullet_cooldown', 'exploded', 'missile_image',
                 'explosion_timer', 'alive', 'change_direction_cooldown', 'shoot_interval', 'last_shot_time',
                 'start_time', 'missile_chance', 'reloading', 'reload_start_time',
                 'reload_duration', 'image', 'original_image', 'explosion_image', 'explosion_sound'
    ]

    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 150
        self.health = health
        self.max_health = health
        self.speed = 3
        self.movement_direction = random.choice([-1, 1])
        self.shield_active = False
        self.shield_timer = 0
        self.max_shield_time = 90000  # 5 seconds in milliseconds
        self.shield_value = 100  # Shield starts with 100% "health"
        self.shield_image = pygame.image.load('assets/spr_shield.png')
        self.shield_image = pygame.transform.scale(self.shield_image, (130, 160))
        self.bullets = []
        self.angle = 0
        self.missiles = []
        self.bullet_cooldown = 0
        self.exploded = False

        self.explosion_timer = 0
        self.alive = True

        self.movement_direction = random.choice([-1, 1])
        self.change_direction_cooldown = 60
        self.shield_active = False
        self.shield_timer = 0

        # Load missile image
        self.missile_image = pygame.image.load('assets/weapons/missile.png')
        self.missile_image = pygame.transform.scale(self.missile_image, (50, 50))

        # Cooldowns to control shooting rates
        self.shoot_interval = 500  # Boss fires every 500 milliseconds
        self.last_shot_time = pygame.time.get_ticks()
        self.start_time = pygame.time.get_ticks()  # Time when game starts
        self.last_shot_time = 0
        self.shoot_interval = 500  # Time between consecutive shots (milliseconds)
        self.missile_chance = 0.1  # Chance to shoot a missile
        self.reloading = False  # Indicates whether the gun is currently reloading
        self.reload_start_time = 0
        self.reload_duration = 5000  # Reload time in milliseconds (3 seconds)

        self.missile_chance = 0.1  # 10% probability to fire a missile

        self.image = pygame.image.load('assets/enemies/gegno augen.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.original_image = self.image

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

    def update_bullets_and_missiles(self, canvas, player_x, player_y, player_width, player_height):
        bullet_width = 4
        bullet_height = 20
        missile_width = 50  # Adjust based on missile image size
        missile_height = 100  # Adjust based on missile image size

        # Skip checking for collisions if the shield is active
        if self.shield_active:
            return False  # Return early if shield is active to prevent bullet damage

        # Draw and move bullets
        for bullet in self.bullets[:]:  # Use a copy of the list to safely remove items
            bullet['y'] += bullet['speed']
            # Draw the bullet as a rectangle with height 5 pixels
            pygame.draw.rect(canvas, (255, 0, 0),
                             (bullet['x'] - bullet_width // 2, bullet['y'], bullet_width, bullet_height),
                             border_radius=5)

            # Check collision with the player's ship
            if (
                    player_x < bullet['x'] < player_x + player_width and
                    player_y < bullet['y'] + bullet_height and
                    player_y + player_height > bullet['y']
            ):
                print("Player hit by boss bullets!")
                self.bullets.remove(bullet)  # Remove bullet on collision
                return True  # Indicate collision to reduce player health

        # Draw and move missiles
        for missile in self.missiles[:]:  # Use a copy of the list to safely remove items
            missile['y'] += missile['speed']
            canvas.blit(self.missile_image, (missile['x'], missile['y']))

            # Check collision with the player's ship
            if (
                    player_x < missile['x'] + missile_width and
                    player_x + player_width > missile['x'] and
                    player_y < missile['y'] + missile_height and
                    player_y + player_height > missile['y']
            ):
                print("Player hit by boss missiles!")
                self.missiles.remove(missile)  # Remove missile on collision
                return True  # Indicate collision to reduce player health

        return False  # No collision

    def move_randomly_boss2(self, player_x, player_y, screen_width, screen_height):
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

    def activate_shield(self):
        if not self.shield_active and pygame.time.get_ticks() - self.shield_timer >= self.max_shield_time:
            self.shield_active = True
            self.shield_timer = pygame.time.get_ticks()
            self.shield_value = 100  # Reset shield value to full when reactivated

    def deactivate_shield(self):
        if self.shield_active:
            elapsed_time = pygame.time.get_ticks() - self.shield_timer
            if elapsed_time >= self.max_shield_time:
                self.shield_active = False
            else:
                # Decrease shield health over time
                self.shield_value = max(0, 100 - int(elapsed_time / self.max_shield_time) * 100)

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
        # Skip checking for collisions if the shield is active
        if self.shield_active:
            return  # If shield is active, do not process any bullet collisions

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
                # Draw the explosion image at the boss's position
                canvas.blit(self.explosion_image, (self.x, self.y))
                self.explosion_timer -= 1
            else:
                # Stop showing the explosion after the timer ends
                self.exploded = False
                self.alive = False  # Mark the boss as no longer alive
            return

        if not self.alive:
            return

        canvas.blit(self.image, (self.x, self.y))

        # Draw shield if active
        if self.shield_active:
            shield_x = self.x - 10
            shield_y = self.y - 10
            canvas.blit(self.shield_image, (shield_x, shield_y))



        # Draw health bar
        health_bar_width = 100
        health_bar_height = 10
        health_bar_x = self.x + (self.width - health_bar_width) // 2
        health_bar_y = self.y - 15
        pygame.draw.rect(canvas, (169, 169, 169), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), border_radius=3)
        current_health_width = (self.health / self.max_health) * health_bar_width
        pygame.draw.rect(canvas, (255, 0, 0), (health_bar_x, health_bar_y, current_health_width, health_bar_height), border_radius=3)

        # Draw shield bar above health bar
        if self.shield_active:
            shield_bar_y = health_bar_y - 15
            pygame.draw.rect(canvas, (169, 169, 169), (health_bar_x, shield_bar_y, health_bar_width, health_bar_height), border_radius=3)
            current_shield_width = (self.shield_value / 100) * health_bar_width
            pygame.draw.rect(canvas, (148, 0, 211), (health_bar_x, shield_bar_y, current_shield_width, health_bar_height), border_radius=3)

    def handle_explosion(self):
        # Only trigger explosion if shield is not active and health <= 0
        if self.health <= 0 and not self.shield_active and not self.exploded:
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
        if self.exploded and score >= 600:
            print("Score reached 4000! Respawning boss...")
            self.respawn(x=350, y=100, health=300)  # Respawn the boss

    def check_bullet_collision(self, bullets):
        # If shield is active, do not check for bullet collisions
        if self.shield_active:
            return  # Skip damage when shield is active

        for bullet in bullets:
            if bullet.x + bullet.width > self.x and bullet.x < self.x + self.width and \
                    bullet.y + bullet.height > self.y and bullet.y < self.y + self.height:
                self.health -= 5
                bullets.remove(bullet)
                if self.health <= 0:
                    self.handle_explosion()
                break
