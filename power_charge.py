import random
import pygame

class PowerCharge:
    __slots__ = ['x', 'y', 'width', 'height', 'speed', 'image', 'power_up_sound']
    def __init__(self, screen_width, screen_height ):
        self.width = 50
        self.height = 50
        self.x = random.randint(0, screen_width - self.width)
        self.y = random.randint(-100, -40)
        self.speed = random.randint(2,2)
        self.image = pygame.image.load('assets/power/full-battery.png')
        self.power_up_sound = None
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # Load the power-up sound when the object is initialized
        try:
            self.power_up_sound = pygame.mixer.Sound("music/treasure.mp3")  # Replace with your sound file path
        except Exception as e:
            self.power_up_sound = None
            print("Error loading power-up sound:", e)

    def activate_power_up(self):
        if self.power_up_sound:
            self.power_up_sound.play()

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
   
   