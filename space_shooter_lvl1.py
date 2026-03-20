import random
import pygame
from pygame import mixer
from pygame.locals import *


pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

# frames per second
clock = pygame.time.Clock()
fps = 60

screen_width = 500
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Shooter')


# define fonts
font30 = pygame.font.SysFont('Costantia', 30)
font40 = pygame.font.SysFont('Costantia', 40)

# load sounds
explosion_fx = pygame.mixer.Sound('C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\explosion.wav')
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound('C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\explosion2.wav')
explosion2_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound('C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\laser.wav')
laser_fx.set_volume(0.25)

# game variables
ROWS = 4
COLS = 5
alien_cooldown = 1000 #milliseconds
last_alien_shot = pygame.time.get_ticks()
COUNTDOWN = 3
last_count = pygame.time.get_ticks()
GAMEOVER = 0 #0 means game is running, 1 means player won, -1 means player lost
SCORE = 0
HIGHSCORE = 0
alien_bullet_speed = 2
num_alien_bullets = 5
alien_move_speed = 1
GAME_PAUSED = False

# screen shake variables
shake_duration = 500 # milliseconds
shake_intensity = 0
shake_start = 0

# colours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

# background image
bg = pygame.image.load('C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\background.jpg')

def draw_bg(offset_x=0, offset_y=0):
  screen.blit(bg, (offset_x, offset_y))

# function for text
def draw_text(text, font, text_col, x, y, offset_x=0, offset_y=0):
  img = font.render(text, True, text_col)
  screen.blit(img, (x + offset_x, y + offset_y))

def draw_sprite_group(group, offset_x=0, offset_y=0):
  for sprite in group:
    screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))

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

  def update(self, offset_x=0, offset_y=0):
    global shake_intensity, shake_start, shake_duration
    # movement speed
    speed = 8
    # cooldown time
    cooldown = 500  #milliseconds
    GAMEOVER = 0

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
      laser_fx.play()
      bullet = Bullets(self.rect.centerx, self.rect.top)
      bullet_group.add(bullet)
      self.last_shot = time_now

    # mask
    self.mask = pygame.mask.from_surface(self.image)

    # health bar
    pygame.draw.rect(screen, red, (self.rect.x + offset_x, (self.rect.bottom + 10) + offset_y, self.rect.width, 10))
    if self.health_remaining > 0:
      pygame.draw.rect(screen, green, (self.rect.x + offset_x, (self.rect.bottom + 10) + offset_y, int(self.rect.width * (self.health_remaining / self.health_start)), 10))
    elif self.health_remaining <= 0:
      explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
      explosion_group.add(explosion)
      shake_duration = 1000
      shake_intensity = 10
      shake_start = pygame.time.get_ticks() # trigger screen shake
      self.kill()
      GAMEOVER = -1
    return GAMEOVER


# Bullets class
class Bullets(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\bullet.png')
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]

  def update(self):
    global SCORE, shake_start, shake_intensity

    self.rect.y -= 5
    if self.rect.bottom < 0:
      self.kill()
    if pygame.sprite.spritecollide(self, alien_group, True, pygame.sprite.collide_mask):
      self.kill()
      explosion_fx.play()
      explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
      explosion_group.add(explosion)
      SCORE += 1
      shake_intensity = 2
      shake_start = pygame.time.get_ticks() # trigger screen shake

# Shake the Screen

# Aliens class
class Aliens(pygame.sprite.Sprite):
  def __init__(self, x, y):
    global alien_move_speed

    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\alien' + str(random.randint(1,4)) + '.png')
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]
    self.move_counter = 0
    self.move_direction = 1

  def update(self):
    self.rect.x += self.move_direction * alien_move_speed
    self.move_counter += alien_move_speed
    if abs(self.move_counter) > 50:
      self.move_direction *= -1
      self.move_counter *= self.move_direction

    # mask
    self.mask = pygame.mask.from_surface(self.image)

# Alien Bullets class
class Alien_Bullets(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\alien_bullet.png')
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]

  def update(self):
    global SCORE, alien_bullet_speed, shake_intensity, shake_start

    self.rect.y += alien_bullet_speed
    if self.rect.top > screen_height:
      self.kill()
    if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
      self.kill()
      explosion2_fx.play()
      # reduce spaceship health
      spaceship.health_remaining -= 1
      explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
      explosion_group.add(explosion)
      shake_intensity = 4
      shake_start = pygame.time.get_ticks() # trigger screen shake
      SCORE -= 2


# Explosion Class
class Explosion(pygame.sprite.Sprite):
  def __init__(self, x, y, size):
    pygame.sprite.Sprite.__init__(self)
    self.images = []
    for num in range(1,9):
      img = pygame.image.load(f'C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\exp{num}.png')
      if size == 1:
        img = pygame.transform.scale(img, (20,20))
      if size == 2:
        img = pygame.transform.scale(img, (40,40))
      if size == 3:
        img = pygame.transform.scale(img, (100,100))
      # add the image to the list
      self.images.append(img)
    self.index = 0
    self.image = self.images[self.index]
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]
    self.counter = 0

  def update(self):
    explosion_speed = 3
    # explosion animation
    self.counter += 1
    
    if self.counter >= explosion_speed and self.index < len(self.images) - 1:
      self.counter = 0
      self.index += 1
      self.image = self.images[self.index]

    # if the animation is complete delete the explosion
    if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
      self.kill()


# sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

# aliens
def create_aliens():
  for row in range(ROWS):
    for item in range(COLS):
      alien = Aliens(70 + item * 90, 80 + row * 70)
      alien_group.add(alien)


def reset_game():
  # Return everything to the original so the player can try again.  
  global SCORE, COUNTDOWN, GAMEOVER, HIGHSCORE, last_alien_shot, alien_bullet_speed, num_alien_bullets, alien_cooldown, alien_move_speed, last_count, spaceship, spaceship_group

  if SCORE > HIGHSCORE:
    HIGHSCORE = SCORE

  SCORE = 0
  COUNTDOWN = 3
  GAMEOVER = 0
  alien_bullet_speed = 2
  num_alien_bullets = 5
  alien_cooldown = 1000
  alien_move_speed = 1
  last_alien_shot = pygame.time.get_ticks()
  last_count = pygame.time.get_ticks()

  # wipe out all existing sprites
  bullet_group.empty()
  alien_group.empty()
  alien_bullet_group.empty()
  explosion_group.empty()

  # repopulate aliens
  create_aliens()

  # create a fresh spaceship
  spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
  spaceship_group.empty()
  spaceship_group.add(spaceship)


# start the first game
reset_game()


# Continue Game
def continue_game():
  global COUNTDOWN, GAMEOVER, last_alien_shot, alien_bullet_speed, num_alien_bullets, alien_cooldown, alien_move_speed, last_count, spaceship, spaceship_group

  COUNTDOWN = 3
  GAMEOVER = 0
  alien_bullet_speed += 2
  num_alien_bullets += 2
  alien_cooldown -= 200
  alien_move_speed += 1
  last_alien_shot = pygame.time.get_ticks()
  last_count = pygame.time.get_ticks()

  # wipe out all existing sprites
  bullet_group.empty()
  alien_group.empty()
  alien_bullet_group.empty()
  explosion_group.empty()

  # repopulate aliens
  create_aliens()

  # create a fresh spaceship
  spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
  spaceship_group.empty()
  spaceship_group.add(spaceship)

# Button Class
class Button():
  def __init__(self, y, x, image, scale):
    width = image.get_width()
    height = image.get_height()
    self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)
    self.clicked = False

  def draw(self, surface):
    action = False
    # mouse position
    pos = pygame.mouse.get_pos()

    # mouseover and clicked conditions
    if self.rect.collidepoint(pos):
      if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
        self.clicked = True
        action = True
    
    if pygame.mouse.get_pressed()[0] == 0:
      self.clicked = False
    
    # draw button on screen
    surface.blit(self.image, (self.rect.x, self.rect.y))

    return action

# button images
back_img = pygame.image.load('C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\BACK.png').convert_alpha()
bullet_speed_img = pygame.image.load('C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\1.5X BULLET SPEED.png').convert_alpha()
ship_speed_img = pygame.image.load('C:\\Users\\break\\OneDrive\\Home\\Programming\\Girls Who Code\\SLEEPOVER\\Space Shooter\\Images\\1.5X SHIP SPEED.png').convert_alpha()

# button instances
back_button = Button(140, 125, back_img, 1)
bullet_speed_button = Button(253, 125, bullet_speed_img, 1)
ship_speed_button = Button(366, 125, ship_speed_img, 1)


run = True
while run:

  clock.tick(fps)

  # calculate screen shake offset
  current_time = pygame.time.get_ticks()
  if current_time - shake_start < shake_duration:
    offset_x = random.randint(-shake_intensity, shake_intensity)
    offset_y = random.randint(-shake_intensity, shake_intensity)
  else:
    offset_x = 0
    offset_y = 0

  # draw background
  draw_bg(offset_x, offset_y)
  draw_text(f'Score: {SCORE}', font30, white, 10, 10, offset_x, offset_y)
  draw_text(f'High Score: {HIGHSCORE}', font30, white, 10, 30, offset_x, offset_y)

  if COUNTDOWN == 0 and GAME_PAUSED == False:

    # random alien bullets
    # record current time
    time_now = pygame.time.get_ticks()
    # shoot
    if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < num_alien_bullets and len(alien_group) > 0:
      attacking_alien = random.choice(alien_group.sprites())
      alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
      alien_bullet_group.add(alien_bullet)
      last_alien_shot = time_now

    # check if aliens are killed
    if len(alien_group) == 0:
      continue_game()
    
    if GAMEOVER == 0:

      # update spaceship
      GAMEOVER = spaceship.update(offset_x, offset_y)

      # update sprite groups
      bullet_group.update()
      alien_group.update()
      alien_bullet_group.update()



    else:
      if GAMEOVER == -1:
        draw_text('YOU LOST.', font40, white, int(screen_width / 2 - 85), int(screen_height / 2 + 50), offset_x, offset_y)
      elif GAMEOVER == 1:  
        draw_text('YOU WON!!!', font40, white, int(screen_width / 2 - 85), int(screen_height / 2 + 50), offset_x, offset_y)

      # restart
      draw_text('Press R to RESTART', font30, white, int(screen_width / 2 - 110), int(screen_height / 2 + 90), offset_x, offset_y)

  if COUNTDOWN > 0:
    draw_text('GET READY!', font40, white, int(screen_width / 2 - 85), int(screen_height / 2 + 50), offset_x, offset_y)
    draw_text(str(COUNTDOWN), font40, white, int(screen_width / 2 - 8), int(screen_height / 2 + 90), offset_x, offset_y)
    count_timer = pygame.time.get_ticks()
    if count_timer - last_count > 1000:
      COUNTDOWN -= 1
      last_count = count_timer

  if GAME_PAUSED == True:
    # create shop
    if back_button.draw(screen):
      GAME_PAUSED = False
    if bullet_speed_button.draw(screen):
      pass
    if ship_speed_button.draw(screen):
      pass

  else:
    # update explosion group
    explosion_group.update()

    # draw sprite groups
    draw_sprite_group(spaceship_group, offset_x, offset_y)
    draw_sprite_group(bullet_group, offset_x, offset_y)
    draw_sprite_group(alien_group, offset_x, offset_y)
    draw_sprite_group(alien_bullet_group, offset_x, offset_y)
    draw_sprite_group(explosion_group, offset_x, offset_y)

  # event handlers
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    elif event.type == pygame.KEYDOWN:
      # restart when game over and player presses R
      if event.key == pygame.K_r and GAMEOVER != 0:
        reset_game()
      # S for shop
      if event.key == pygame.K_s:
        GAME_PAUSED = True

  pygame.display.update()

pygame.quit()