import random
import pygame
from pygame.locals import *

# frames per second
clock = pygame.time.Clock()
fps = 60

screen_width = 500
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Shooter')

# game variables
ROWS = 4
COLS = 5

# colours
red = (255, 0, 0)
green = (0, 255, 0)

# background image
bg = pygame.image.load('C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\background.jpg')

def draw_bg():
  screen.blit(bg, (0, 0))

# Spaceship class
class Spaceship(pygame.sprite.Sprite):
  def __init__(self, x, y, health):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\spaceship.png')
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]
    self.health_start = health
    self.health_remaining = health
    self.last_shot = pygame.time.get_ticks()

  def update(self):
    # movement speed
    speed = 8
    # cooldown time
    cooldown = 500  #milliseconds

    # key press to move
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and self.rect.left > 0:
      self.rect.x -= speed
    if key[pygame.K_RIGHT] and self.rect.right < screen_width:
      self.rect.x += speed

    # record current time
    time_now = pygame.time.get_ticks()

    # key press to shoot
    if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
      bullet = Bullets(self.rect.centerx, self.rect.top)
      bullet_group.add(bullet)
      self.last_shot = time_now

    # health bar
    pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 10))
    if self.health_remaining > 0:
      pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 10))

# Bullets class
class Bullets(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\bullet.png')
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]

  def update(self):
    self.rect.y -= 5
    if self.rect.bottom < 0:
      self.kill()

# Aliens class
class Aliens(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\alien' + str(random.randint(1,4)) + '.png')
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]
    self.move_counter = 0
    self.move_direction = 1

  def update(self):
    self.rect.x += self.move_direction
    self.move_counter += 1
    if abs(self.move_counter) > 50:
      self.move_direction *= -1
      self.move_counter *= self.move_direction

# sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()

# aliens
def create_aliens():
  for row in range(ROWS):
    for item in range(COLS):
      alien = Aliens(70 + item * 90, 60 + row * 70)
      alien_group.add(alien)

create_aliens()

# player
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)

run = True
while run:

  clock.tick(fps)
  # draw background
  draw_bg()

  # event handlers
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  # update sprite groups
  bullet_group.update()
  alien_group.update()

  # draw sprite groups
  spaceship_group.draw(screen)
  bullet_group.draw(screen)
  alien_group.draw(screen)

  # update spaceship
  spaceship.update()

  pygame.display.update()

pygame.quit()