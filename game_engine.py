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
import pygame.locals

from  sys import  exit
from ncp import Enemy, EnemyBullet
from power_charge import PowerCharge
from bullet_power import BulletPower
from  astroid_attack import  AstroidAttack
from boss_npc import BossEnemy
from boss_enemy2 import BossEnemy2
from  final_boss import TheFinalBoss
import random
import time
import  gc

collected = gc.collect()
print("Garbage collected: collected", "%d objects." % collected)


class CrashedUfoBackground:
    __slots__ = ['x', 'y', 'width', 'height', 'speed', 'image0', 'ufo']
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.width = 50  # Adjust the size of meteoroids
        self.height = 50
        self.speed = speed
        self.image0 = pygame.image.load("assets/enemies/crashed_ufo.png")
        self.image0 = pygame.transform.scale(self.image0, (self.width, self.height))
        
        
        self.image0 = pygame.transform.rotate(self.image0, -80)
        
        
        self.ufo = []
        
        
    def move(self):
        # Move meteoroid across the screen
        self.x -= self.speed  # Move left (you can adjust the direction and speed)
        if self.x < -self.width:  # If meteoroid goes off-screen, reset to the right
            self.x = 1020  # Reset position to the right edge of the screen

    def shoot(self):
        # Random chance for the meteoroid to shoot
        if random.randint(1, 100) < 2:  # 2% chance to shoot
            bullet = Bullet(self.x + self.width // 2 - 5, self.y + self.height)  # Create a bullet
            self.ufo.append(bullet)  # Add to the list of bullets

    def draw(self, canvas):
        canvas.blit(self.image0, (self.x, self.y))  # Draw meteoroid
        
        
        

class Meteoroid:
    __slots__ = ['x', 'y', 'width', 'height',  'speed', 'image' , 'meteoroid_bullets']
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.width = 50  # Adjust the size of meteoroids
        self.height = 50
        self.speed = speed
        self.image = pygame.image.load('assets/PNG/meteoroid.png')  # Use the meteoroid image
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        self.meteoroid_bullets = [] # List to store meteoroid bullets

    def move(self):
        # Move meteoroid across the screen
        self.x -= self.speed  # Move left (you can adjust the direction and speed)
        if self.x < -self.width:  # If meteoroid goes off-screen, reset to the right
            self.x = 1020  # Reset position to the right edge of the screen

    def shoot(self):
        # Random chance for the meteoroid to shoot
        if random.randint(1, 100) < 2:  # 2% chance to shoot
            bullet = Bullet(self.x + self.width // 2 - 5, self.y + self.height)  # Create a bullet
            self.meteoroid_bullets.append(bullet)  # Add to the list of bullets

    def draw(self, canvas):
        canvas.blit(self.image, (self.x, self.y))  # Draw meteoroid

# Spaceship Bullet Animation
class Bullet:
    __slots__ = ['x', 'y','width', 'height', 'speed']
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5  # Bullet width
        self.height = 10  # Bullet height
        self.speed = 9  # Speed at which the bullet moves upward

    def move(self):
        self.y -= self.speed  # Move the bullet upwards

    def draw(self, canvas):
        # Draw a solid dark blue bullet
        pygame.draw.rect(canvas, (98, 190, 193), (self.x, self.y, self.width, self.height), border_radius=5)  # Dark Blue Color



class ExhaustFlame:
    __slots__ = ['x', 'y',  'width', 'height', 'speed', 'horizontal_wiggle',
                 'fade_rate', 'max_opacity', 'opacity','color'
    ]
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = random.randint(12, 20)  # Random width for variability
        self.height = random.randint(20, 35)  # Random height for variability
        self.speed = random.uniform(4, 6)  # Flame movement speed
        self.horizontal_wiggle = random.uniform(-1, 1)  # Random horizontal drift
        self.fade_rate = random.uniform(0.5, 1.5)  # Fade effect to make the flame disappear
        self.max_opacity = 255  # Maximum opacity for the flame
        self.opacity = self.max_opacity  # Initial opacity of the flame

        # Color for flame, with a random orange gradient
        self.color = (255, random.randint(50, 150), 0)  # Orange gradient for flames

    def move(self):
        # Flame moves downward
        self.y += self.speed
        # Flame wiggles horizontally
        self.x += self.horizontal_wiggle
        # Reduce opacity to simulate the flame fading as it moves
        self.opacity = max(0, self.opacity - int(self.fade_rate))  # Ensure opacity is an integer

    def draw(self, canvas):
        # Adjust color opacity based on the current opacity
        flame_color = (self.color[0], self.color[1], self.color[2], int(self.opacity))

        # Draw the flame using an ellipse
        pygame.draw.ellipse(canvas, flame_color, (self.x, self.y, self.width, self.height))


class Spaceship:
    __slots__ = ['x', 'y', 'width', 'height', 'speed', 'image',
                 'rotated_image', 'angle', 'exhaust_flames', 'tilt_speed', 'protection_img',
                 'shield_active', 'shield_time', 'shield_active', 'max_shield_time',
                 'shield_value', 'health', 'max_health'

    ]

    def __init__(self, x, y, health):

        self.x = x
        self.y = y
        self.width = 60
        self.height = 60
        self.speed = 14
        self.angle = 0  # Angle for rotation
        self.tilt_speed = 5  # Smooth tilt speed for airplane-like movement
        self.image = pygame.image.load('assets/spaceship/blackbird.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.protection_img = pygame.image.load('assets/spr_shield.png')
        self.protection_img = pygame.transform.scale(self.protection_img, (130, 160))

        self.shield_active = False
        self.shield_time = 0

        self.max_shield_time = 4000
        self.shield_value  = 100

        self.max_health = health
        self.health  = health


        self.rotated_image = self.image  # Store rotated image
        self.exhaust_flames = []  # List to store active flames

    def move(self, keys, resolution):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
            if self.angle < 5:  # Smooth tilt left
                self.angle += self.tilt_speed
        elif keys[pygame.K_RIGHT] and self.x < resolution[0] - self.width:
            self.x += self.speed
            if self.angle > -5:  # Smooth tilt right
                self.angle -= self.tilt_speed
        else:
            # Gradually reset the angle to 0 when no horizontal movement
            if self.angle > 0:
                self.angle -= self.tilt_speed
            elif self.angle < 0:
                self.angle += self.tilt_speed

        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
            self.release_flames()  # Release flames when moving up
        if keys[pygame.K_DOWN] and self.y < resolution[1] - self.height:
            self.y += self.speed

    def move_away(self):
        # Move the spaceship to the side when a collision occurs
        self.x += self.speed  # Move the spaceship right, adjust as necessary
        if self.x > 800 - self.width:
            self.x = 800 - self.width  # Keep within the screen bounds

    def release_flames(self):
        # I've decided not to use self.width and height to calculate co-ordinates
        # because flames they
        # become aligned at left engine  of spaceship
        # the aim is to place the flame at the center

        flame = ExhaustFlame(self.x + 110 // 2 - 5, self.y + 100)
        self.exhaust_flames.append(flame)

    def activate_shield(self):
        if not self.shield_active and pygame.time.get_ticks() - self.shield_time >= 1000:
            self.shield_active = True
            self.shield_time = pygame.time.get_ticks()
            self.shield_value = 100  # Reset shield value to full when reactivated

    def deactivate_shield(self):
        if self.shield_active:
            elapsed_time = pygame.time.get_ticks() - self.shield_time  # Time since shield was activated

            # Debug: Print the elapsed time and shield value
            print(f"Elapsed Time: {elapsed_time}, Shield Value: {self.shield_value}")

            # Deactivate if either the time is up or the shield value reaches 0
            if elapsed_time >= self.max_shield_time:
                self.shield_active = False
                self.shield_value = 0  # Fully depleted shield value
                print(f"Shield Deactivated due to time: {elapsed_time}ms, Shield Value: {self.shield_value}")
            elif self.shield_value <= 0:
                self.shield_active = False
                self.shield_value = 0
                print(f"Shield Deactivated due to shield value: {elapsed_time}ms, Shield Value: {self.shield_value}")
            else:
                # Gradually decrease shield value over time
                self.shield_value = max(0, 100 - int(elapsed_time / self.max_shield_time) * 100)

            # Print shield status after deactivation check
            print(f"Shield Active: {self.shield_active}, Shield Value: {self.shield_value}")

    def draw(self, canvas):
        # Rotate the spaceship image based on angle
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = self.rotated_image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        canvas.blit(self.rotated_image, rotated_rect.center)


        if self.shield_active:
            shield_x = self.x - 10
            shield_y = self.y - 10
            canvas.blit(self.protection_img, (shield_x, shield_y))

            # Draw shield bar
            shield_bar_x = self.x + (self.width - 100) // 2 # Adjusted positioning
            shield_bar_y = self.y - 20  # Positioned above the character
            shield_bar_w = 100
            shield_bar_h = 10

            pygame.draw.rect(canvas, (169, 169, 169),
                             (shield_bar_x, shield_bar_y, shield_bar_w, shield_bar_h), border_radius=3)
            current_shield_width = int((self.shield_value / 100) * shield_bar_w)
            pygame.draw.rect(canvas, (148, 0, 211),
                             (shield_bar_x, shield_bar_y, current_shield_width, shield_bar_h), border_radius=3)

            print(f"Drawing Shield Bar: {current_shield_width}/{shield_bar_w}")

        for flame in self.exhaust_flames[:]:
            flame.move()
            flame.draw(canvas)
            if flame.y > 600:  # Remove flames when they go off-screen
                self.exhaust_flames.remove(flame)

    def update(self):
        print("Updating shield status...")
        # self.activate_shield()
        # self.deactivate_shield()
        pass


    def check_collision_with_asteroid(self, asteroid):
        # Simple rectangle collision check
        if self.x < asteroid.rect.x + asteroid.width and self.x + self.width > asteroid.rect.x and \
                self.y < asteroid.rect.y + asteroid.height and self.y + self.height > asteroid.rect.y:
            # Collision detected, figure out the side hit and trigger the asteroid's space movement
            hit_side = self.get_collision_side(asteroid)
            asteroid.hit_by_missile(hit_side)

    def get_collision_side(self, asteroid):
        # Detect which side of the asteroid was hit by the spaceship
        hit_side = None

        # Get the center of the spaceship and the asteroid
        spaceship_center = self.x + self.width / 2, self.y + self.height / 2
        asteroid_center = asteroid.rect.x + asteroid.width / 2, asteroid.rect.y + asteroid.height / 2

        # Check for hit from each side of the asteroid
        if spaceship_center[0] < asteroid_center[0]:  # Hit from the left
            hit_side = 'left'
        elif spaceship_center[0] > asteroid_center[0]:  # Hit from the right
            hit_side = 'right'
        elif spaceship_center[1] < asteroid_center[1]:  # Hit from above
            hit_side = 'top'
        elif spaceship_center[1] > asteroid_center[1]:  # Hit from below
            hit_side = 'bottom'

        return hit_side






def open_play_window():
    pygame.init()

    # Initialize the mixer for sound
    pygame.mixer.init()
    
    #  gunshot sound
    gunshot_sound = pygame.mixer.Sound('music/laser-gun.mp3')

    # explosion sound
    explosion_sound = pygame.mixer.Sound('music/expl.mp3')  # Replace with your file path


    # Screen resolution and window setup
    resolution = (1020, 600)
    all_sprites = pygame.sprite.Group()
    canvas = pygame.display.set_mode(resolution, pygame.RESIZABLE)
    pygame.display.set_caption('Space War Shooter')

    # Background images and planet images
    bg_image = pygame.image.load('assets/kurt/space_up.png')
    planet_image = pygame.image.load('assets/PNG/13.png')
    space_stars = pygame.image.load('assets/PNG/12.png')
    janitor_planet = pygame.image.load('assets/PNG/15.png')
    # ship = pygame.image.load('assets/spaceship/space-ship.png')
    slight  = pygame.image.load('assets/PNG/9.png')
    shooting_start = pygame.image.load('assets/PNG/6.png')
    


    # Game overloaded image
    game_over_img = pygame.image.load("assets/game_over/game-over.png")
    game_over_img_width, game_over_img_height = 200, 200  #image dimensions
    game_over_img = pygame.transform.scale(game_over_img, (game_over_img_width, game_over_img_height))

    # Game star image is loaded when the boss is destroyed
    star_image = pygame.image.load('assets/star/star.png')

    explosion_img = pygame.image.load('assets/explosions/expl.png')
    explosion_size = (100, 100)
    explosion_img = pygame.transform.scale(explosion_img, explosion_size)


    # Play/Pause button images
    play_img = pygame.image.load('assets/pause_play/play.png')
    pause_img = pygame.image.load('assets/pause_play/pause.png')

    # Scale play/pause images to desired size
    BUTTON_WIDTH, BUTTON_HEIGHT = 50, 50  # Adjust as needed
    play_img = pygame.transform.scale(play_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
    pause_img = pygame.transform.scale(pause_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

    default_image_size = (1020, 600)
    planet_size = (100, 100)
    stars_size = (22, 22)
    janitor_planet_size = (19, 19)
    shooting_start_size = (29, 29)
    
    # meteoroid = pygame.transform.scale(meteoroid,  shooting_start_size)

    planet_image = pygame.transform.scale(planet_image, planet_size)
    space_stars = pygame.transform.scale(space_stars, stars_size)
    bg_image = pygame.transform.scale(bg_image, default_image_size)
    janitor_planet = pygame.transform.scale(janitor_planet, janitor_planet_size)
    slight = pygame.transform.scale(slight, planet_size)
    
    shooting_start = pygame.transform.rotate(shooting_start, 180)
    shooting_start = pygame.transform.scale(shooting_start, shooting_start_size)
    
    slight = pygame.transform.rotate(slight, 180)





    # Ship variables
    ship_width = 50
    ship_height = 50
    ship_x = resolution[0] // 2 - ship_width // 2  # Start in the center of the screen
    ship_y = resolution[1] - ship_height - 10  # Position at the bottom of the screen
    ship_speed = 14




    # Health bar variables
    health_max = 100  
    health_width = 125  
    health_height = 10  
    health_x = 10  
    health_y = 10  



    fire_bomb_max= 109
    fire_bomb_width = 90
    fire_bomb_height = 10
    fire_bomb_x = 10
    fire_bomb_y = health_y + health_x + 10
    
    score_font_y = health_y + health_height + 5
    score_font = pygame.font.Font(None, 30)
    score = 0
    
    

    enemies_to_remove = []
    bullets_to_remove = []

    # List to store active bullets
    bullets = []
    spawn_rate = 60



    bullet_ready_to_fire = True



    # Pause functionality
    is_paused = False  # Initially, the game is not paused

    # Position for the play/pause button at the top center
    button_x = resolution[0] // 2 - BUTTON_WIDTH // 2 # Centered horizontally
    button_y = 10  # Placed 10 pixels from the top

    
    # UFO Enemies don't get confused asking yourself what is this...
    enemies = [Enemy(resolution[0], resolution[1]) for _ in range(5)]  #5 ncp enemies
    
    # Initialize boss enemy
    boss_enemy = None
    boss_defeated = False


    asteroids = None
    asteroid_spawned = False

    # Initialize boss enemy 2
    boss_enemy2 = None
    boss_spawned = False



    final_boss = None
    final_boss_spawned = False



    stars_start_time_1 = 0
    stars_start_time_2 = 0
    stars_start_time_3 = 0
    show_stars_1 = False
    show_stars_2 = False
    the_final_boss_star =  False
    initial_y_position = resolution[1] // 2  # Start at the center of the screen


    
    enemy_bullets = []
    ship_energy = 100
    powered_bullets = 0

    
    # Initialize variables
    power_charges = []
    frame_count = 0
    last_power_spawn_time = time.time()
    power_spawn_interval = 10
    bullet_powers = []

    ship = Spaceship(ship_x, ship_y, health=100)
    ship.draw(canvas)
    ship.update()

    meteoroids = [Meteoroid(1020, random.randint(50, 500), random.uniform(0.5, 1.5)) for _ in range(4)]
    crashed_ufos = [CrashedUfoBackground(1020, random.randint(50, 500), random.uniform(0.5, 1.5)) for _ in range(2)]




    clock = pygame.time.Clock()

    player_x = ship_x  # Assuming ship_x is the horizontal position of the player's ship
    player_y = ship_y  # Assuming ship_y is the vertical position of the player's ship
    player_width = ship_width  # Assuming ship_width represents the width of the player's ship
    player_height = ship_height  # Assuming ship_height represents the height of the player's ship


    # # Initial object positions
    planet_x, planet_y = resolution[0] // 2 - 50, resolution[1] - 150
    slight_tech_x1 = resolution[0] // 2 - 100


    bg_x = 0

    # Set a flag for resizing to prevent scaling on every frame
    background_scaled = False

    # Game loop flag
    running = True
    while running:

        keys = pygame.key.get_pressed()
        # start_time = time.time()
        # Fill the canvas with black or any background color to clear the screen
        canvas.fill((0, 0, 0))  # Black background, replace with any other color if you prefer

        for x_offset in [bg_x]:
            canvas.blit(bg_image, (x_offset, 0))


        canvas.blit(space_stars, (250, 390))
        canvas.blit(planet_image, (planet_x, planet_y))
        canvas.blit(janitor_planet, (100, 100))
        canvas.blit(slight, (bg_x, 0))
        canvas.blit(shooting_start, (slight_tech_x1, 150))





        # Draw the health bar
        pygame.draw.rect(canvas, (169, 169, 169), (health_x, health_y, health_width, health_height), border_radius=5)  # Gray background
        health_current_width = (ship_energy/ health_max) * health_width  # Calculate the current health width
        pygame.draw.rect(canvas, (0, 255, 0), (health_x, health_y, health_current_width, health_height), border_radius=5)  # Green color


        pygame.draw.rect(canvas, (169, 169, 169), (fire_bomb_x, fire_bomb_y, fire_bomb_width, fire_bomb_height), border_radius=5)
        charged_power_width = (powered_bullets / fire_bomb_max) * fire_bomb_width
        pygame.draw.rect(canvas, (98,  190, 193), (fire_bomb_x, fire_bomb_y, charged_power_width, fire_bomb_height), border_radius=5)


        # Draw the appropriate button based on pause state
        if is_paused:
            canvas.blit(play_img, (button_x, button_y))  # Show the play button if paused
        else:
            canvas.blit(pause_img, (button_x, button_y))  # Show the pause button if playing

            # Assuming there's an 'is_paused' variable indicating pause state

            if not is_paused:
                # Game logic when not paused
                ship.move(keys, resolution)
                ship.draw(canvas)

                # Handle key presses for movement
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and ship_x > 0:
                    ship_x -= ship_speed
                if keys[pygame.K_RIGHT] and ship_x < resolution[0] - ship_width:
                    ship_x += ship_speed
                if keys[pygame.K_UP] and ship_y > 0:
                    ship_y -= ship_speed
                    ship.release_flames()
                if keys[pygame.K_DOWN] and ship_y < resolution[1] - ship_height:
                    ship_y += ship_speed

                # Shoot bullets when 'SPACE' is pressed
                if keys[pygame.K_SPACE] and bullet_ready_to_fire:

                    if powered_bullets >= fire_bomb_max:  # Check if firebomb bar is fully loaded
                        # Fire double bullets
                        bullet1 = Bullet(ship.x + ship.width // 2 - 10, ship.y)  # Left bullet
                        bullet2 = Bullet(ship.x + ship.width // 2 + 5, ship.y)  # Right bullet
                        bullets.extend([bullet1, bullet2])

                        gunshot_sound.play()  # Play gunshot sound for double shot
                        powered_bullets = 0  # Reset the firebomb bar
                    else:
                        # Fire a single bullet
                        bullet = Bullet(ship.x + 115 // 2 - 5, ship.y)  # Centered bullet
                        bullets.append(bullet)
                        gunshot_sound.play()  # Play gunshot sound for single shot

                    bullet_ready_to_fire = False  # Prevent continuous firing

                    # If the 'SPACE' key is released, allow shooting again
                if not keys[pygame.K_SPACE]:
                    bullet_ready_to_fire = True

                for meteoroid in meteoroids:
                    meteoroid.move()
                    meteoroid.shoot()
                    meteoroid.draw(canvas)

                for crashed_ufo in crashed_ufos:
                    crashed_ufo.move()
                    crashed_ufo.shoot()
                    crashed_ufo.draw(canvas)

                    # Move and draw bullets
                for bullet in bullets:
                    bullet.move()
                    bullet.draw(canvas)

                    # Remove bullet if it goes off the screen
                    if bullet.y < 0:
                        bullets.remove(bullet)

                # Bullets and Enemies Are Not Removed Properly
                # solution...
                # Ensure you remove them consistently after use or once they go off-screen


                # The error is fixed now the enemies are removed Properly

                bullets = [bullet for bullet in bullets if bullet.y > 0]
                enemies = [enemy for enemy in enemies if not enemy.is_off_screen(resolution[1])]



            if not is_paused:
                    # Iterate over enemies and bullets
                    for enemy in enemies:
                        for bullet in bullets:
                            # print(f"Bullet at ({bullet.x}, {bullet.y}) Enemy at ({enemy.x}, {enemy.y})")
                            # Collision detection
                            if (bullet.x < enemy.x + enemy.width and bullet.x + bullet.width > enemy.x and
                                    bullet.y < enemy.y + enemy.height and bullet.y + bullet.height > enemy.y):
                                    print('Collision detected')

                                     # Add to score
                                    score += 10
                                    print(f"Score: {score}")
                                    # Remove enemy and bullet after collision
                                    enemies_to_remove.append(enemy)
                                    bullets_to_remove.append(bullet)


                        # Move and draw enemies
                        enemy.move()
                        enemy.check_collision(bullets, ship)
                        enemy.update_physic()
                        enemy.draw(canvas)


                        if enemy in enemies[:]:
                            if random.randint(1, 100) < 3:
                                bullet = EnemyBullet(enemy.x + enemy.width // 2 - 2, enemy.y + enemy.height)
                                enemy_bullets.append(bullet)
                                enemy.shoot()


                        if enemy.is_off_screen(resolution[1]):
                            enemies_to_remove.append(enemy)

                            # Draw all sprites
                            all_sprites.draw(canvas)

            # asteroids they don't render correctly
            # need to be fixed I don't know where, but
            # it must be fixed (rendering show and disappear)

        
            astroid_attack_respawn = 1000

            if score >= astroid_attack_respawn and not asteroid_spawned and not asteroids:
                asteroid_spawned = True
                asteroids = [AstroidAttack() for _ in range(9)]
                all_sprites.add(*asteroids)


                # Check if asteroids are spawned, then update and draw them
            if asteroid_spawned:
                        # Iterate through the asteroid list properly
                        for asteroid in asteroids:  # Use 'asteroid' instead of 'asteroids'
                            asteroid.update_astroid()

                            # Check collision with ship for each asteroid
                            if (
                                    ship_x < asteroid.rect.x + asteroid.rect.width and
                                    ship_x + ship_width > asteroid.rect.x and
                                    ship_y < asteroid.rect.y + asteroid.rect.height and
                                    ship_y + ship_height > asteroid.rect.y
                            ):
                                print("Ship hit by asteroid!")
                                ship_energy -= 1  # Reduce ship energy
                                asteroid.hit = True  # Trigger bounce-like effect

                                # Check if ship is destroyed
                                if ship_energy <= 0:
                                    print("Player ship destroyed!")
                                    explosion_sound.play()
                                    canvas.blit(explosion_img, (ship_x, ship_y))
                                    pygame.display.update()
                                    pygame.time.wait(1000)

                                    # Show Game Over screen
                                    game_over_x = (resolution[0] - game_over_img_width) // 2
                                    game_over_y = (resolution[1] - game_over_img_height) // 2
                                    canvas.blit(game_over_img, (game_over_x, game_over_y))

                                    # Display restart and menu text
                                    font = pygame.font.Font(None, 20)
                                    color = (255, 255, 255)
                                    restart_text = font.render("Press SPACE to Restart", True, color)
                                    menu_text = font.render("Press ESC to go to Main Menu", True, color)

                                    restart_text_rect = restart_text.get_rect(
                                        center=(resolution[0] // 2, game_over_y + game_over_img_height + 50))
                                    menu_text_rect = menu_text.get_rect(
                                        center=(resolution[0] // 2, game_over_y + game_over_img_height + 100))

                                    canvas.blit(restart_text, restart_text_rect)
                                    canvas.blit(menu_text, menu_text_rect)

                                    pygame.display.update()

                                    # Handle input during Game Over
                                    game_over = True
                                    while game_over:
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                                exit()
                                            if event.type == pygame.KEYDOWN:
                                                if event.key == pygame.K_SPACE:
                                                    # Restart game variables
                                                    score = 0
                                                    ship_energy = 100
                                                    bullets = []
                                                    asteroid = None
                                                    game_over = False
                                                    running = True
                                                    break
                                                elif event.key == pygame.K_ESCAPE:
                                                    running = False
                                                    game_over = False
                                                    break

                        # Update all sprites
                        # Check collisions with asteroids
                        for sprite in all_sprites:  # Changed 'asteroids' -> 'sprite'
                            if isinstance(sprite, AstroidAttack):
                                all_sprites.draw(canvas)

                                ship.check_collision_with_asteroid(sprite)

                        all_sprites.update()

            # Handle bullets (my existing bullet collision logic)
            for enemy_bullet in enemy_bullets:
                enemy_bullet.move()
                enemy_bullet.draw(canvas)

                            # Check collision with ship for bullets
                if (
                    ship_x < enemy_bullet.x + enemy_bullet.width and
                    ship_x + ship_width > enemy_bullet.x and
                    ship_y < enemy_bullet.y + enemy_bullet.height and
                    ship_y + ship_height > enemy_bullet.y
                    ):
                        print("Ship hit by enemy bullet!")
                        ship_energy -= 5  # Decrease energy
                        enemy_bullets.remove(enemy_bullet)  # Remove bullet upon collision

                                # Check if the ship's energy is depleted
                        if ship_energy <= 0:
                            print("Player ship destroyed!")  # Debug message
                            explosion_sound.play()  # Play explosion sound
                            canvas.blit(explosion_img, (ship_x, ship_y))  # Show explosion
                            pygame.display.update()
                            pygame.time.wait(1000)  # Pause to show explosion

                            # Show Game Over screen
                            game_over_x = (resolution[0] - game_over_img_width) // 2
                            game_over_y = (resolution[1] - game_over_img_height) // 2

                            # Center the Game Over image
                            canvas.blit(game_over_img, (game_over_x, game_over_y))

                            #font and text properties
                            font = pygame.font.Font(None, 20)
                            color = (255, 255, 255)  # White color for text

                            # Render text
                            restart_text = font.render("Press SPACE to Restart", True, color)
                            menu_text = font.render("Press ESC to go to Main Menu", True, color)

                                    # Get screen dimensions
                            screen_width, screen_height = resolution

                            # Get the position to render text under the Game Over image
                            restart_text_rect = restart_text.get_rect(
                                center=(screen_width // 2, game_over_y + game_over_img_height + 50))
                            menu_text_rect = menu_text.get_rect(
                                center=(screen_width // 2, game_over_y + game_over_img_height + 100))

                            # Blit the text onto the canvas
                            canvas.blit(restart_text, restart_text_rect)
                            canvas.blit(menu_text, menu_text_rect)

                            pygame.display.update()

                            # Wait for player input to restart or quit
                            game_over = True
                            while game_over:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        exit()

                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_SPACE:  # Restart the game
                                            # Reset game variables to restart
                                            score = 0
                                            ship_energy = 100
                                            bullets = []  # Clear bullets
                                            boss_enemy = None  # Reset boss
                                            game_over = False  # Exit Game Over loop
                                            running = True  # Continue game loop
                                            break

                                        elif event.key == pygame.K_ESCAPE:  # Exit the game
                                            running = False
                                            game_over = False
                                            break




         # Power-ups
        if time.time() - last_power_spawn_time >= power_spawn_interval:
            POWER_CHARGES = 1
            if len(power_charges) < POWER_CHARGES:
                power_charges.append(PowerCharge(resolution[0], resolution[1]))

            # power_charges.append(PowerCharge(resolution[0], resolution[1]))
            BULLET_POWER = 1
            if len(bullet_powers) < BULLET_POWER:
                bullet_powers.append(BulletPower(resolution[0], resolution[1]))

            # bullet_powers.append(BulletPower(resolution[0], resolution[1]))
            last_power_spawn_time = time.time()


        if not is_paused:
            for power_charge in power_charges:
                power_charge.move()
                power_charge.draw(canvas)

                # Check collision with the ship
                if power_charge.check_collision(ship_x, ship_y, ship_width, ship_height):
                    power_charge.activate_power_up()
                    print("Health power collected!")

                    power_charges.remove(power_charge)
                    # Recharge ship energy
                    ship_energy = min(ship_energy + 31, health_max)  # Increment energy but respect the max limit
                elif power_charge.is_off_screen(resolution[1]):
                    power_charges.remove(power_charge)

            # list comprehension for better memory cleanup
            power_charges = [p for p in power_charges if not p.is_off_screen(resolution[1])]
            bullet_powers = [p for p in bullet_powers if not p.is_off_screen(resolution[1])]
            enemy_bullets = [b for b in enemy_bullets if not b.is_off_screen(resolution[1])]

            # del power_charges[:]


            for bullet_charge in bullet_powers:
                bullet_charge.move()
                bullet_charge.draw(canvas)

                # Check collision with the ship
                if bullet_charge.check_collision(ship_x, ship_y, ship_width, ship_height):
                    bullet_charge.activate_bullet_power_up()
                    print("Bullet power collected!")
                    bullet_powers.remove(bullet_charge)


                    # Recharge bullet power
                    powered_bullets = min(powered_bullets + 50, fire_bomb_max)  # Increment power but respect the max limit
                elif bullet_charge.is_off_screen(resolution[1]):
                    bullet_powers.remove(bullet_charge)


                # del bullet_powers[:]


                # Enemy spawning every 'spawn_rate' frames
                frame_count += 1  # Increment frame count to control spawn rate
                if frame_count % spawn_rate == 0:  # Spawn an enemy every 'spawn_rate' frames
                    MAX_ENEMIES = 5
                    if len(enemies) < MAX_ENEMIES:
                        enemies.append(Enemy(resolution[0], resolution[1]))
                    # enemy = Enemy(resolution[0], resolution[1])  # Create a new enemy at the top
                    # enemies.append(enemy)  # Add enemy to the list


        if slight_tech_x1 <= +shooting_start.get_width():
            slight_tech_x1 = shooting_start.get_width()

        text_ = score_font.render(f'Score : {score}', True, (255, 255, 255))
        canvas.blit(text_, (health_x + health_width + 5, score_font_y))


        ##################################################################

        boss_enemy2_respawn_score = 3000

        if score >= boss_enemy2_respawn_score and not boss_spawned and boss_enemy2 is None:
            boss_enemy2 = BossEnemy2(resolution[0] // 2, 50, health=300)  # Spawn boss at the desired position
            print("Boss no 2 spawned!")
            boss_spawned = True  # Mark boss as spawned

        # # Handle boss defeat logic
        if boss_enemy2 and boss_enemy2.health <= 0:
            print("Boss no2 defeated!")
            score += 650  # Reward the player
            show_stars_2 = True  # Set flag to show stars and reward text

            stars_start_time_2 = pygame.time.get_ticks()  # Record start time for animation
            boss_enemy2 = None  # Remove boss from the game
            boss_defeated = True  # Mark boss as defeated

        # Handle star animation and reward text
        current_time = pygame.time.get_ticks()

        if show_stars_2:
            elapsed_time = current_time - stars_start_time_2
            star_y_position = resolution[1] // 2 - (elapsed_time / 5)

            if star_y_position < -100:
                show_stars_2 = False
            else:
                star_rect = star_image.get_rect(center=(resolution[0] // 2, star_y_position))

                canvas.blit(star_image, star_rect)

                # Render the "+650" text above the star
                font_text = pygame.font.Font(None, 64)
                bonus_text_value = font_text.render("650+", True, (255, 255, 255))
                text_rect_value = bonus_text_value.get_rect(center=(resolution[0] // 2, star_y_position - 50))

                canvas.blit(bonus_text_value, text_rect_value)

            pygame.display.update()

            if score >= boss_enemy2_respawn_score and boss_enemy2 and not boss_enemy2.alive:
                print("Score reached threshold! Boss exploded and disappeared!")
                boss_enemy2.handle_explosion()  # Trigger the boss explosion
                boss_enemy2 = None  # Remove the boss from the game

        if boss_enemy2 and boss_enemy2.alive:
            boss_enemy2.update(canvas, resolution[0], bullets)  # Update position and shield mechanics
            boss_enemy2.check_bullet_collision(bullets)  # Check collision with player bullets
            boss_enemy2.shoot()  # Boss fires bullets



            # Render explosion if boss is defeated
            if boss_enemy2 and  boss_enemy2.health <= 0:

                # Render the explosion image at Boss 2's last known position
                explosion_rect = explosion_img.get_rect(center=(boss_enemy2.x, boss_enemy2.y))
                canvas.blit(explosion_img, explosion_rect)

                # Start an asynchronous delay for explosion
                explosion_start_time = pygame.time.get_ticks()
                while pygame.time.get_ticks() - explosion_start_time < 700:  # 500ms delay
                    # Show the explosion without freezing the game
                    canvas.blit(explosion_img, explosion_rect)
                    pygame.display.update()



                print("Boss2 defeated!")
                score += 650

                # Set flag to show stars and text
                show_stars_2 = True
                stars_start_time_2 = pygame.time.get_ticks()

                boss_enemy2 = None  # Remove the boss from the game
                boss_defeated = True  # Mark that the boss was defeated

            current_time = pygame.time.get_ticks()

            if show_stars_2:
                elapsed_time = current_time - stars_start_time_2
                star_y_position = initial_y_position - (elapsed_time / 5)
                if star_y_position < -100:
                    show_stars_2 = False

            if show_stars_2:
                elapsed_time = current_time - stars_start_time_2
                star_y_offset = - (elapsed_time / 50)

                star_rect = star_image.get_rect(center=(resolution[0] // 2, resolution[1] // 2 + star_y_offset))
                canvas.blit(star_image, star_rect)

                font_text = pygame.font.Font(None, 64)
                bonus_text_value = font_text.render("650+", True, (255, 255, 255))
                text_rect_value = bonus_text_value.get_rect(center=(resolution[0] // 2, resolution[1] // 2 + 100 + star_y_offset))
                canvas.blit(bonus_text_value, text_rect_value)
            pygame.display.update()  # Update the display to show the explosion


            if boss_enemy2 and  boss_enemy2.update_bullets_and_missiles(canvas, player_x, player_y, player_width, player_height):
                    ship_energy -= 20  # Reduce player's ship energy if hit
                    if ship_energy <= 0:
                        explosion_sound.play()
                        canvas.blit(explosion_img, (ship_x, ship_y))
                        pygame.display.update()
                        pygame.time.wait(1000)
                        print('Game Over')
                        running = False  # Stop the game loop

                        # Show Game Over screen
                        game_over_x = (resolution[0] - game_over_img_width) // 2
                        game_over_y = (resolution[1] - game_over_img_height) // 2

                        # Center the Game Over image
                        canvas.blit(game_over_img, (game_over_x, game_over_y))

                        # font and text properties
                        font = pygame.font.Font(None, 20)
                        color = (255, 255, 255)  # White color for text

                        # Render text
                        restart_text = font.render("Press SPACE to Restart", True, color)
                        menu_text = font.render("Press ESC to go to Main Menu", True, color)

                        # Get screen dimensions
                        screen_width, screen_height = resolution

                        # Get the position to render text under the Game Over image
                        restart_text_rect = restart_text.get_rect(
                            center=(screen_width // 2, game_over_y + game_over_img_height + 50))
                        menu_text_rect = menu_text.get_rect(
                            center=(screen_width // 2, game_over_y + game_over_img_height + 100))

                        # Blit the text onto the canvas
                        canvas.blit(restart_text, restart_text_rect)
                        canvas.blit(menu_text, menu_text_rect)

                        pygame.display.update()

                        # Wait for player input to restart or quit
                        game_over = True
                        while game_over:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()

                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_SPACE:  # Restart the game
                                        # Reset game variables to restart
                                        score = 0
                                        ship_energy = 100
                                        bullets = []  # Clear bullets
                                        boss_enemy2 = None  # Reset boss
                                        game_over = False  # Exit Game Over loop
                                        running = True  # Continue game loop
                                        break

                                    elif event.key == pygame.K_ESCAPE:  # Exit the game
                                        running = False
                                        game_over = False
                                        break

                ##############################################################################
                    # Just discovered an error the boss it respawn correctly
                    # but when the score threshold is above 1000, the boss hides
                    # keeps decrementing the  player health etc.
                    # Actually is astroid attack is rendering anonymous under the matrix
                    # the bug is recovered but the astroid they only appear on top screen
                    # resolution frozen

        boss_respawn_score = 2000  # Set the score threshold for boss spawning 2000 score

        # Spawn the boss for the first time if score >= threshold and no boss exists
        if score >= boss_respawn_score and boss_enemy is None and not boss_defeated:
            boss_enemy = BossEnemy(resolution[0] // 2, 50, health=300)
            print("Boss spawned!")  # First time spawning the boss


        # Handle boss defeat and removal
        if boss_enemy and boss_enemy.health <= 0:
            print("Boss defeated!")
            score += 550

            # Set flag to show stars and text
            show_stars_1 = True
            stars_start_time_1 = pygame.time.get_ticks()

            boss_enemy = None  # Remove the boss from the game
            boss_defeated = True  # Mark that the boss was defeated

        current_time = pygame.time.get_ticks()
            # Check if stars should disappear after 3 seconds

        if show_stars_1:
            elapsed_time = current_time - stars_start_time_1

            # Calculate the new Y-position based on elapsed time
            star_y_position = resolution[1] // 2 - (elapsed_time / 5)

            # Stop displaying when the star and text are off the screen
            if star_y_position < -100:  # Adjust this threshold if necessary
                show_stars_1 = False
            else:
                star_rect = star_image.get_rect(center=(resolution[0] // 2, star_y_position))
                canvas.blit(star_image, star_rect)


            # Render the 550+ text in white with upward motion
            font = pygame.font.Font(None, 64)
            bonus_text = font.render("550+", True, (255, 255, 255))
            text_rect = bonus_text.get_rect(center=(resolution[0] // 2, star_y_position - 50))

            canvas.blit(bonus_text, text_rect)
        pygame.display.flip()

        if score >= boss_respawn_score and boss_enemy and not boss_enemy.alive:
            print("Score reached threshold! Boss exploded and disappeared!")
            boss_enemy.handle_explosion()  # Trigger the boss explosion
            boss_enemy = None  # Remove the boss from the game

        # Check collision with boss
        if boss_enemy:
            if (
                    ship_x < boss_enemy.x + boss_enemy.width and
                    ship_x + ship_width > boss_enemy.x and
                    ship_y < boss_enemy.y + boss_enemy.height and
                    ship_y + ship_height > boss_enemy.y
            ):
                print("Ship collided with the Boss!")
                ship_energy = -6  # Set ship energy to 0
                if ship_energy <= 0:

                    # Trigger explosion effect
                    explosion_sound.play()
                    canvas.blit(explosion_img, (ship_x, ship_y))
                    pygame.display.update()
                    pygame.time.wait(500)  # Pause briefly to show explosion

                    print('Game Over')

                # Show Game Over screen
                game_over_x = (resolution[0] - game_over_img_width) // 2
                game_over_y = (resolution[1] - game_over_img_height) // 2

                # Center the Game Over image
                canvas.blit(game_over_img, (game_over_x, game_over_y))

                # Font and text properties
                font = pygame.font.Font(None, 20)
                color = (255, 255, 255)  # White color for text

                # Render text
                restart_text = font.render("Press SPACE to Restart", True, color)
                menu_text = font.render("Press ESC to go to Main Menu", True, color)

                # Get the position to render text under the Game Over image
                restart_text_rect = restart_text.get_rect(
                    center=(resolution[0] // 2, game_over_y + game_over_img_height + 50))
                menu_text_rect = menu_text.get_rect(
                    center=(resolution[0] // 2, game_over_y + game_over_img_height + 100))

                # Blit the text onto the canvas
                canvas.blit(restart_text, restart_text_rect)
                canvas.blit(menu_text, menu_text_rect)

                pygame.display.update()

                # Wait for player input to restart or quit
                game_over = True
                while game_over:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:  # Restart the game
                                # Reset game variables to restart
                                score = 0
                                ship_energy = 100
                                bullets = []  # Clear bullets
                                boss_enemy = None  # Reset boss

                                game_over = False  # Exit Game Over loop
                                running = True  # Continue game loop
                                break

                            elif event.key == pygame.K_ESCAPE:  # Exit the game
                                running = False
                                game_over = False
                                break

        # Handle boss actions
        if boss_enemy:
            boss_enemy.move_randomly(player_x=ship_x, player_y=ship_y, screen_width=resolution[0],
                                     screen_height=resolution[1])
            boss_enemy.check_bullet_collision(bullets)  # Handle collision with player bullets
            boss_enemy.shoot()
            boss_enemy.draw(canvas)

            # Check for bullets hitting the spaceship
            if boss_enemy.update_bullets(canvas, ship_x, ship_y, ship_width, ship_height):
                ship_energy -= 3
                if ship_energy <= 0:
                    explosion_sound.play()
                    canvas.blit(explosion_img, (ship_x, ship_y))
                    pygame.display.update()
                    pygame.time.wait(1000)

                    print('Game Over')

                    # Show Game Over screen
                    game_over_x = (resolution[0] - game_over_img_width) // 2
                    game_over_y = (resolution[1] - game_over_img_height) // 2

                    # Center the Game Over image
                    canvas.blit(game_over_img, (game_over_x, game_over_y))

                    # Font and text properties
                    font = pygame.font.Font(None, 20)
                    color = (255, 255, 255)  # White color for text

                    # Render text
                    restart_text = font.render("Press SPACE to Restart", True, color)
                    menu_text = font.render("Press ESC to go to Main Menu", True, color)

                    restart_text_rect = restart_text.get_rect(
                        center=(resolution[0] // 2, game_over_y + game_over_img_height + 50))
                    menu_text_rect = menu_text.get_rect(
                        center=(resolution[0] // 2, game_over_y + game_over_img_height + 100))

                    canvas.blit(restart_text, restart_text_rect)
                    canvas.blit(menu_text, menu_text_rect)

                    pygame.display.update()

                    # Wait for player input
                    game_over = True
                    while game_over:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()

                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:  # Restart the game
                                    score = 0
                                    ship_energy = 100
                                    bullets = []
                                    boss_enemy = None
                                    game_over = False
                                    running = True
                                    break

                                elif event.key == pygame.K_ESCAPE:
                                    running = False
                                    game_over = False
                                    break


        ###############################################################################
        # The final boss code section

        final_boss_respawn_score = 3000  # The score threshold to spawn the final boss

        # Check if the final boss should spawn
        if score >= final_boss_respawn_score and not final_boss_spawned and final_boss is None:
            final_boss = TheFinalBoss(x=resolution[0] // 2, y=50, health=400)
            print("Score reached threshold! Final Boss spawned!")
            final_boss_spawned = True

        # Check if the final boss is defeated
        if final_boss and final_boss.health <= 0:
            print("Final Boss defeated!")
            score += 950  # Add score for defeating the boss
            final_boss.handle_explosion()  # Trigger the explosion effect
            final_boss.bullets.clear()  # Clear the bullets after boss defeat

        current_time = pygame.time.get_ticks()

        if the_final_boss_star:
            elapsed_time = current_time - stars_start_time_3
            star_y_position = resolution[1] // 2 - (elapsed_time / 5)

            if star_y_position < -100:
                the_final_boss_star = False
            else:
                star_rect = star_image.get_rect(center=(resolution[0] // 2, star_y_position))
                canvas.blit(star_image, star_rect)

                font_text = pygame.font.Font(None, 64)
                boss_bonus_text_value = font_text.render("950+", True, (255, 255, 255))

                final_boss_text_rect = boss_bonus_text_value.get_rect(center=(resolution[0] // 2, star_y_position - 50))
                canvas.blit(boss_bonus_text_value, final_boss_text_rect)

                alert_text = pygame.font.Font(None, 44)
                notice_text_value = alert_text.render("The Final Boss has been Defeated", True, (255, 255, 255))
                notice_rect = notice_text_value.get_rect(center=(resolution[0] // 2, star_y_position + 120))
                canvas.blit(notice_text_value, notice_rect)

            pygame.display.update()

            # Handle respawning after defeating the boss (only if the boss is not alive)
            if score >= final_boss_respawn_score and final_boss and not final_boss.alive:
                print("Final Boss exploded and disappeared!")
                final_boss = None  # Remove the boss from the game after explosion

        # The Problem now is the blink of the boss
        # the time I stopped working 22:22

        # Main game loop where the boss behavior is updated
        if final_boss and final_boss.alive:
            final_boss.update(canvas, resolution[0], resolution[1], bullets)


            # If the boss is defeated, handle the explosion and game state
            if final_boss.health <= 0:
                # Trigger explosion effect
                explosion_rect = explosion_img.get_rect(center=(final_boss.x, final_boss.y))
                canvas.blit(explosion_img, explosion_rect)
                explosion_rect_rep = explosion_img.get_rect(center=(final_boss.x, final_boss.y))
                canvas.blit(explosion_img, explosion_rect_rep)

                explosion_start_time = pygame.time.get_ticks()
                while pygame.time.get_ticks() - explosion_start_time < 500:  # Explosion lasts 500ms
                    canvas.blit(explosion_img, explosion_rect)
                    canvas.blit(explosion_img, explosion_rect_rep)
                    pygame.display.update()

                print("Final Boss Defeated!")
                score += 950
                the_final_boss_star = True
                stars_start_time_3 = pygame.time.get_ticks()
                # After explosion, mark the boss as defeated
                final_boss.alive = False
                final_boss = None  # Remove the boss from the game



            # If the final boss is still alive, draw its bullets and check for collisions with player
            elif final_boss and final_boss.bullets:  # Ensure the boss is still alive and has bullets
                for bullet in final_boss.bullets:
                    bullet.draw(canvas)
                    # print(f"Bullet at position: {bullet.x}, {bullet.y}")



            # Check if any bullet hits the player
            if final_boss and  final_boss.update_bullets(canvas, player_x, player_y, player_width, player_height):
                    ship_energy -= 10  # Decrease player's energy on hit
                    if ship_energy <= 0:  # If ship energy is 0 or less, game over
                        explosion_sound.play()
                        canvas.blit(explosion_img, (ship_x, ship_y))
                        pygame.display.update()
                        pygame.time.wait(2000)  # Wait for 2 seconds before exiting
                        running = False  # End the game

                        # Show Game Over screen
                        game_over_x = (resolution[0] - game_over_img_width) // 2
                        game_over_y = (resolution[1] - game_over_img_height) // 2

                        # Center the Game Over image
                        canvas.blit(game_over_img, (game_over_x, game_over_y))

                        # font and text properties
                        font = pygame.font.Font(None, 20)
                        color = (255, 255, 255)  # White color for text

                        # Render text
                        restart_text = font.render("Press SPACE to Restart", True, color)
                        menu_text = font.render("Press ESC to go to Main Menu", True, color)

                        # Get screen dimensions
                        screen_width, screen_height = resolution

                        # Get the position to render text under the Game Over image
                        restart_text_rect = restart_text.get_rect(
                            center=(screen_width // 2, game_over_y + game_over_img_height + 50))
                        menu_text_rect = menu_text.get_rect(
                            center=(screen_width // 2, game_over_y + game_over_img_height + 100))

                        # Blit the text onto the canvas
                        canvas.blit(restart_text, restart_text_rect)
                        canvas.blit(menu_text, menu_text_rect)

                        pygame.display.update()

                        # Wait for player input to restart or quit
                        game_over = True
                        while game_over:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()

                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_SPACE:  # Restart the game
                                        # Reset game variables to restart
                                        score = 0
                                        ship_energy = 100
                                        bullets = []  # Clear bullets
                                        boss_enemy2 = None  # Reset boss
                                        game_over = False  # Exit Game Over loop
                                        running = True  # Continue game loop
                                        break

                                    elif event.key == pygame.K_ESCAPE:  # Exit the game
                                        running = False
                                        game_over = False
                                        break

            pygame.display.update()  # Always update the display after drawing

              # The End For now!
######################################################################################

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

            elif event.type == pygame.VIDEORESIZE:
                # Get the new size of the window
                resolution = event.w, event.h
                if not background_scaled:
                    bg_image = pygame.transform.scale(bg_image, resolution)
                    background_scaled = True


                # This is responsible for centering the pause & play button
                WIDTH, HEIGHT = event.w, event.h
                button_x = WIDTH // 2 - BUTTON_WIDTH // 2

                bg_image = pygame.transform.scale(bg_image, resolution)



                planet_x, planet_y = resolution[0] // 2 - 50, resolution[1] - 150
                slight_tech_x1 = resolution[0] // 2 - 100

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if the click is inside the play/pause button
                if button_x <= mouse_x <= button_x + 50 and button_y <= mouse_y <= button_y + 50:
                    is_paused = not is_paused  # Toggle pause state





        canvas.blit(bg_image, (bg_x, 0))









        clock.tick(80)

        # Optional: Print frame rate (useful for debugging)
        # elapsed_time = time.time() - start_time
        # print(f"Frame time: {elapsed_time:.3f} seconds")

def new_func(enemy):
    return enemy

