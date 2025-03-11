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


import pygame
import random
import  math

# Placeholder enemy class for regular enemies
class Enemy:
    __slots__ = ['x', 'y', 'width', 'height', 'color']
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.color = (0, 255, 0)

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, (self.x, self.y, self.width, self.height))


class BossEnemy2:
    __slots__ = [ 'x', 'y', 'width', 'height', 'health', 'max_health', 'speed', 'movement_direction',
                  'shield_active', 'shield_timer', 'max_shield_time', 'shield_value', 'shield_image',
                  'bullets', 'missiles', 'bullet_cooldown', 'exploded', 'explosion_timer',
                  'alive', 'change_direction_cooldown', 'missile_image', 'shoot_interval',
                  'last_shot_time', 'start_time', 'missile_chance', 'reloading', 'reload_start_time',
                  'reload_duration', 'image', 'explosion_image', 'explosion_sound'
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

        # Shield starts with 100% "health"
        self.shield_image = pygame.image.load('assets/spr_shield.png')
        self.shield_image = pygame.transform.scale(self.shield_image, (130, 160))
        self.bullets = []
        self.missiles = []
        self.bullet_cooldown = 0
        self.exploded = False
        self.explosion_timer = 0
        self.alive = True

        # self.movement_direction = random.choice([-1, 1])
        self.change_direction_cooldown = 60


        self.max_shield_time = 9000  # 9 seconds in milliseconds
        self.shield_value = 100
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

        # Explosion assets
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

    def shoot(self):
        current_time = pygame.time.get_ticks()

        # Check if we're in reloading state
        if self.reloading:
            if current_time >= self.reload_start_time + self.reload_duration:
                self.reloading = False
                self.start_time = current_time  # Reset the start time after reloading
                print("Reloading complete, ready to shoot again")

            return  # Don't shoot while reloading

        # Check if 7 seconds have passed to trigger reloading
        if current_time >= self.start_time + 9000:
            print("Initiating reload...")
            self.reloading = True
            self.reload_start_time = current_time

            return  # Pause shooting during reload

        # Shoot double bullets if not reloading
        if current_time - self.last_shot_time >= self.shoot_interval:
            self.last_shot_time = current_time

            bullet1 = {'x': self.x + 20, 'y': self.y + self.height, 'speed': 5}
            bullet2 = {'x': self.x + self.width - 20, 'y': self.y + self.height, 'speed': 5}
            self.bullets.extend([bullet1, bullet2])

            # Occasionally fire a missile
            if random.random() < self.missile_chance:
                missile = {'x': self.x + self.width // 2, 'y': self.y + self.height, 'speed': 8}
                self.missiles.append(missile)

            print("Shooting bullets")

    def respawn(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.exploded = False
        self.explosion_timer = 100
        self.alive = True

        self.shield_timer = 0
        self.movement_direction = random.choice([-1, 1])
        self.bullets.clear()
        self.missiles.clear()
        print("Boss has been respawned.")

    # def check_respawn(self, score):
    #     if self.exploded and score >= 600 and not self.alive:
    #         print("Score reached 600! Respawning boss...")
    #         self.respawn(x=350, y=100, health=300)  # Respawn the boss only once

    def check_respawn(self, score):
        if self.exploded and score >= 600:
            print("Score reached 4000! Respawning boss...")
            self.respawn(x=350, y=100, health=300)  # Respawn the boss

    def update_bullets_and_missiles(self, canvas, player_x, player_y, player_width, player_height):
        bullet_width = 4
        bullet_height = 20
        missile_width = 50  # Adjust based on missile image size
        missile_height = 100  # Adjust based on missile image size

        # Update and draw bullets
        for bullet in self.bullets[:]:  # Use a copy of the list to safely iterate
            bullet['y'] += bullet['speed']  # Move the bullet
            pygame.draw.rect(canvas, (255, 0, 0),
                             (bullet['x'] - bullet_width // 2, bullet['y'], bullet_width, bullet_height),
                             border_radius=5)

            # Check collision with the player's ship
            if (
                    player_x < bullet['x'] + bullet_width and
                    player_x + player_width > bullet['x'] and
                    player_y < bullet['y'] + bullet_height and
                    player_y + player_height > bullet['y']
            ):
                print("Player hit by boss bullet!")
                self.bullets.remove(bullet)  # Remove bullet on collision
                return True  # Indicate collision to reduce player health

            # Remove bullets that are off-screen
            if bullet['y'] > canvas.get_height():
                self.bullets.remove(bullet)

        # Update and draw missiles
        for missile in self.missiles[:]:  # Use a copy of the list to safely iterate
            missile['y'] += missile['speed']  # Move the missile
            canvas.blit(self.missile_image, (missile['x'], missile['y']))

            # Check collision with the player's ship
            if (
                    player_x < missile['x'] + missile_width and
                    player_x + player_width > missile['x'] and
                    player_y < missile['y'] + missile_height and
                    player_y + player_height > missile['y']
            ):
                print("Player hit by boss missile!")
                self.missiles.remove(missile)  # Remove missile on collision
                return True  # Indicate collision to reduce player health

            # Remove missiles that are off-screen
            if missile['y'] > canvas.get_height():
                self.missiles.remove(missile)

        return False  # No collision detected

    def move_randomly_boss2(self, screen_width):
        self.x += self.movement_direction * self.speed
        if self.x <= 0 or self.x + self.width >= screen_width:
            self.movement_direction *= -1  # Reverse direction



    def activate_shield(self):
        if not self.shield_active and pygame.time.get_ticks() - self.shield_timer >= 10000:
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

    def update(self, canvas, screen_width, bullets):
        if self.alive:
            self.move_randomly_boss2(screen_width)
            self.shoot()

            # Check bullet collisions
            if self.check_bullet_collision(bullets):
                print("Bullet hit boss")

            self.activate_shield()
            self.deactivate_shield()

            try:
                self.draw(canvas)
            except Exception as e:
                print(f"Error drawing boss: {e}")



    def handle_explosion(self):
        if self.health <= 0 and not self.exploded:
            self.exploded = True
            if self.explosion_sound:
                self.explosion_sound.play()
            print("Explosion triggered!")
            self.alive = False  # Mark the boss as dead

    def check_bullet_collision(self, bullets):
        for bullet in bullets:
            if bullet.x + bullet.width > self.x and bullet.x < self.x + self.width and \
                    bullet.y + bullet.height > self.y and bullet.y < self.y + self.height:
                self.health -= 100
                bullets.remove(bullet)
                if self.health <= 0:
                    self.handle_explosion()
                break





