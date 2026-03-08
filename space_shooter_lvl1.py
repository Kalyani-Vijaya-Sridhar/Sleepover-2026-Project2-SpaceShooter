import pygame
from pygame.locals import *

# frames per second
clock = pygame.time.Clock()
fps = 60

screen_width = 400
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Shooter')

# colours
red = (255, 0, 0)
green = (0, 255, 0)

# background image
bg = pygame.image.load('C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\background.jpg')

# spaceship class
class Spaceship(pygame.sprite.Sprite):
  def __init__(self, x, y, health):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\spaceship.png')
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]
    self.health_start = health
    self.health_remaining = health

  def update(self):
    # movement speed
    speed = 8
    # key press
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and self.rect.left > 0:
      self.rect.x -= speed
    if key[pygame.K_RIGHT] and self.rect.right < screen_width:
      self.rect.x += speed

    # health bar
    pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 10))
    if self.health_remaining > 0:
      pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 10))

# sprite groups
spaceship_group = pygame.sprite.Group()

# player
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)

def draw_bg():
  screen.blit(bg, (0, 0))

run = True
while run:

  clock.tick(fps)
  # draw background
  draw_bg()

  # event handlers
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  # draw sprite groups
  spaceship_group.draw(screen)

  # update spaceship
  spaceship.update()

  pygame.display.update()

pygame.quit()