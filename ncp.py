import pygame
import random

# Initialize pygame mixer
pygame.mixer.init()

# Define the enemy bullet class
class EnemyBullet:
    __slots__ = ['x', 'y', 'width', 'height', 'speed']  # Optimize memory usage

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.speed = 4

    def move(self):
        self.y += self.speed

    def draw(self, canvas):
        pygame.draw.rect(canvas, (255, 0, 0), (self.x, self.y, self.width, self.height), border_radius=10)

    def is_off_screen(self, screen_height):
        return self.y > screen_height

    def check_collision(self, spaceship):
        return (self.x + self.width > spaceship.x and self.x < spaceship.x + spaceship.width and
                self.y + self.height > spaceship.y and self.y < spaceship.y + spaceship.height)


# Main Enemy class
class Enemy(pygame.sprite.Sprite):
    __slots__ = [
        'x', 'y', 'width', 'height', 'speed', 'image', 'rect', 'velocity_x', 'velocity_y',
        'enemy_bullets', 'last_shot_time', 'shooting_rate', 'exploded', 'explosion_image',
        'explosion_time', 'explosion_sound'
    ]  # Optimize memory usage

    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.width = 70
        self.height = 70
        self.x = random.randint(0, screen_width - self.width)
        self.y = random.randint(-100, -50)
        self.speed = random.randint(2, 5)
        self.image = pygame.image.load('assets/enemies/alien-ship.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()

        self.velocity_x = random.randint(-5, 5)
        self.velocity_y = random.randint(1, 9)

        self.enemy_bullets = []
        self.last_shot_time = 0
        self.shooting_rate = random.randint(50, 200)

        self.exploded = False
        self.explosion_image = pygame.image.load('assets/explosions/expl.png')
        self.explosion_image = pygame.transform.scale(self.explosion_image, (self.width, self.height))
        self.explosion_time = 0

        self.explosion_sound = pygame.mixer.Sound('music/expl.mp3')

    def move(self):
        self.y += self.speed

    def draw(self, canvas, spaceship=None):
        if not self.exploded:
            canvas.blit(self.image, (self.x, self.y))
        else:
            canvas.blit(self.explosion_image, (self.x, self.y))
            if pygame.time.get_ticks() - self.explosion_time > 500:
                self.exploded = False
                self.y = -1000

        # Remove bullets if they hit the spaceship
        if spaceship:
            self.enemy_bullets = [bullet for bullet in self.enemy_bullets
                                  if not bullet.is_off_screen(canvas.get_height()) and not bullet.check_collision(spaceship)]
        for bullet in self.enemy_bullets:
            bullet.move()
            bullet.draw(canvas)

    def is_off_screen(self, screen_height):
        return self.y > screen_height

    def check_collision(self, bullets, spaceship):
        hit_detected = False
        bullets_to_remove = []

        for bullet in bullets:
            if bullet.x + bullet.width > self.x and bullet.x < self.x + self.width and \
                    bullet.y + bullet.height > self.y and bullet.y < self.y + self.height:
                bullets_to_remove.append(bullet)
                hit_detected = True

        for bullet in bullets_to_remove:
            bullets.remove(bullet)

        if self.x < spaceship.x + spaceship.width and self.x + self.width > spaceship.x and \
                self.y < spaceship.y + spaceship.height and self.y + self.height > spaceship.y:
            self.crash_response(spaceship)
            hit_detected = True

        if hit_detected and not self.exploded:
            self.exploded = True
            self.explosion_time = pygame.time.get_ticks()
            self.bounce()

        return hit_detected

    def shoot(self):
        bullet = EnemyBullet(self.x + self.width // 2 - 5, self.y + self.height)
        self.enemy_bullets.append(bullet)

    def can_shoot(self, frame_count):
        if frame_count % self.shooting_rate == 0:
            self.shoot()

    def bounce(self):
        self.velocity_x = -self.velocity_x
        self.velocity_y = -self.velocity_y

    def crash_response(self, spaceship):
        direction_x = self.x - spaceship.x
        direction_y = self.y - spaceship.y
        distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
        direction_x /= distance
        direction_y /= distance
        self.velocity_x += direction_x * 10
        self.velocity_y += direction_y * 10

    def update_physic(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        if abs(self.velocity_x) < 1:
            self.velocity_x = 0
        if abs(self.velocity_y) < 1:
            self.velocity_y = 0
        if self.rect.y > 600:
            self.rect.y = -self.height
            self.rect.x = random.randint(0, 800)
