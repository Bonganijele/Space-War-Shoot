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

pygame.init()

class FlashBullet:
    __slots__ = ['x', 'y', 'width', 'height', 'speed', 'color']
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 8
        self.height = 15
        self.speed = 5
        self.color = (255, 255, 0)

    def move(self):
        self.y += self.speed

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, (self.x, self.y, self.width, self.height), border_radius=5)

    def is_off_screen(self, screen_height):
        return self.y > screen_height


class TheFinalBoss:
    __slots__ = ['x', 'y', 'width', 'height', 'speed', 'angle',
        'health', 'max_health' , 'laser', 'movement_direction' , 'explosion_timer', 'exploded',
        'alive', 'bullets' , 'shoot_interval', 'last_shot_time',
        'invisible', 'invisibility_timer', 'invisibility_duration', 'laser_triggered',
        'final_boss_img', 'explosion_image',  'explosion_image_size', 'explosion_sound'
    ]
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 150
        self.health = health
        self.max_health = health
        self.laser = None
        self.speed = 3
        self.movement_direction = random.choice([-1, 1])

        # Invisibility Mechanism
        self.invisible = False
        self.invisibility_timer = 0
        self.invisibility_duration = 5000  # 5 seconds

        self.laser_triggered = False

        self.explosion_timer = 0
        self.exploded = False
        self.alive = True

        # Invisibility Mechanism
        self.invisible = False
        self.invisibility_timer = 0
        self.invisibility_duration = 5000

        self.bullets = []
        self.shoot_interval = 500
        self.last_shot_time = pygame.time.get_ticks()

        # Load Boss Image
        self.final_boss_img = pygame.image.load('assets/enemies/arch-carrack.png')
        self.final_boss_img = pygame.transform.scale(self.final_boss_img, (self.width, self.height))

        # Explosion Effect
        try:
            self.explosion_image = pygame.image.load('assets/explosions/expl.png')
            self.explosion_image_size = (210, 210)
            self.explosion_image = pygame.transform.scale(self.explosion_image, self.explosion_image_size)
        except Exception as e:
            self.explosion_image = None
            print("Error loading explosion image:", e)

        try:
            self.explosion_sound = pygame.mixer.Sound('music/expl.mp3')
        except Exception as e:
            self.explosion_sound = None
            print("Error loading explosion sound:", e)

    def shoot(self):
        # Stop firing if boss is invisible
        if self.invisible:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_interval:
            self.last_shot_time = current_time
            bullet_x = self.x + (self.width // 2) - 10
            bullet_y = self.y + self.height
            flash_bullet = FlashBullet(bullet_x, bullet_y)
            self.bullets.append(flash_bullet)

    def update_bullets(self, canvas, player_x, player_y, player_width, player_height):
        for bullet in self.bullets[:]:
            bullet.move()
            bullet.draw(canvas)

            if (player_x < bullet.x + bullet.width and
                    player_x + player_width > bullet.x and
                    player_y < bullet.y + bullet.height and
                    player_y + player_height > bullet.y):
                print("Player hit by the final boss!")
                self.bullets.remove(bullet)
                return True

    def draw(self, canvas):
        if self.exploded:
            if self.explosion_image and self.explosion_timer > 0:
                canvas.blit(self.explosion_image, self.explosion_image_size)
                self.explosion_timer -= 1
            else:
                self.exploded = False
                self.alive = False
            return

        if not self.alive or self.invisible:
            return

        canvas.blit(self.final_boss_img, (self.x, self.y))

        # Health Bar
        health_bar_width = 130
        health_bar_height = 10
        health_bar_x = self.x + (self.width - health_bar_width) // 2
        health_bar_y = self.y - 15
        pygame.draw.rect(canvas, (169, 169, 169), (health_bar_x, health_bar_y, health_bar_width, health_bar_height),
                         border_radius=3)
        current_health_width = (self.health / self.max_health) * health_bar_width
        pygame.draw.rect(canvas, (255, 0, 0), (health_bar_x, health_bar_y, current_health_width, health_bar_height),
                         border_radius=3)

        # Invisibility Timer Bar
        if self.invisible:
            invisibility_bar_width = 130
            invisibility_bar_height = 10
            invisibility_bar_x = self.x + (self.width - invisibility_bar_width) // 2
            invisibility_bar_y = self.y - 30  # Adjusted position below health bar
            pygame.draw.rect(canvas, (169, 169, 169),
                             (invisibility_bar_x, invisibility_bar_y, invisibility_bar_width, invisibility_bar_height),
                             border_radius=3)

            remaining_time = max(0, self.invisibility_duration - (pygame.time.get_ticks() - self.invisibility_timer))
            current_invisibility_width = (remaining_time / self.invisibility_duration) * invisibility_bar_width
            pygame.draw.rect(canvas, (0, 0, 255), (
            invisibility_bar_x, invisibility_bar_y, current_invisibility_width, invisibility_bar_height),
                             border_radius=3)

    def respawn(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.exploded = False
        self.explosion_timer = 100
        self.alive = True
        self.movement_direction = random.choice([-1, 1])
        self.bullets.clear()
        print("Boss has been respawned.")

    def check_respawn(self, score):
        if self.exploded and score >= 100:
            print("Score reached 100! Respawning the final boss...")
            self.respawn(x=350, y=100, health=400)

    def evade(self):
        # Boss evades by dashing to a new position
        self.x += random.choice([-1, 1]) * 50
        self.y += random.choice([-1, 1]) * 50

    def activate_invisibility(self):
        # Random chance to trigger invisibility
        if random.random() < 0.05:  # 5% chance to become invisible
            self.invisible = True
            self.invisibility_timer = pygame.time.get_ticks()



    def update(self, canvas, screen_width, screen_height, bullets):
        if self.alive:
            self.move_randomly_final_boss(screen_width, screen_height)
            self.draw(canvas)
            self.shoot()

            # Invisibility Timer
            if self.invisible and pygame.time.get_ticks() - self.invisibility_timer >= self.invisibility_duration:
                self.invisible = False

            if self.check_bullet_collision(bullets):
                print("Bullet hit final boss!")

            self.handle_phase_change()

            if random.random() < 0.02:  # 2% chance of evading each frame
                self.evade()
                self.activate_invisibility()


    def handle_explosion(self):
        if self.health <= 0 and not self.exploded:
            self.exploded = True
            if self.explosion_sound:
                self.explosion_sound.play()
            print("Explosion triggered!")
            self.alive = False

    def handle_phase_change(self):
        # Change boss behavior based on health
        if self.health <= self.max_health * 0.5:  # Phase 2
            self.speed = 5
            self.shoot_interval = 300
            print("Phase 2: Boss is faster and more aggressive!")

    def move_randomly_final_boss(self, screen_width, screen_height):
        self.x += self.movement_direction * self.speed

        # Ensure the boss stays within screen width
        if self.x <= 0:
            self.x = 0
            self.movement_direction *= -1
        elif self.x + self.width >= screen_width:
            self.x = screen_width - self.width
            self.movement_direction *= -1

        # Limit the boss's vertical position to prevent going off the bottom
        self.y = max(100, min(self.y, screen_height // 2 - self.height // 2))  # Keeps the boss within the top half

    def check_bullet_collision(self, bullets):
        for bullet in bullets[:]:
            if bullet.x + bullet.width > self.x and bullet.x < self.x + self.width and \
                    bullet.y + bullet.height > self.y and bullet.y < self.y + self.height:
                self.health -= 1
                bullets.remove(bullet)
                if self.health <= 0:
                    self.handle_explosion()
                break





