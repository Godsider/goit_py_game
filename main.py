import random
from copy import copy
from os import listdir
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
# Python has no constants on it's own, 
# so UPPERCASED var names are meant to mark vars that must not be changed since their creation to be used as constants

scores = 0

# colors definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# size definition
PLAYER_SIZE = (121, 51)
ENEMY_SIZE = (68, 24)
BONUS_SIZE = (90, 149)

pygame.init()

screen = width, height = 800, 600
main_surface = pygame.display.set_mode(screen)

FPS = pygame.time.Clock()
font = pygame.font.SysFont('Verdana', 20)

IMGS_PATH = 'goose'
player_imgs = [pygame.transform.scale(pygame.image.load(IMGS_PATH + '/' + file).convert_alpha(), PLAYER_SIZE) for file in listdir(IMGS_PATH)]
player = player_imgs[0]
img_index = 0 # the index of the player's current sprite
player_rect = player.get_rect()
player_speed = 5

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), ENEMY_SIZE)
    enemy_width = enemy.get_size()[0]
    enemy_height = enemy.get_size()[1]
    enemy_rect = pygame.Rect((width + enemy_width), random.randint(10, (height - enemy_height - 10)), *enemy.get_size())
    enemy_speed = random.randint(bg_speed + 1, bg_speed + 3)
    return [enemy, enemy_rect, enemy_speed]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies = []

def create_bonus():
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), BONUS_SIZE)
    bonus_width = bonus.get_size()[0]
    bonus_height = bonus.get_size()[1]
    bonus_rect = pygame.Rect(random.randint(10, (width - bonus_width - 10)), -bonus_height, *bonus.get_size())
    bonus_speed = random.randint(2, 5)
    return [bonus, bonus_rect, bonus_speed]

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)
bonuses = []

is_working = True

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]

    pressed_keys = pygame.key.get_pressed()

    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    main_surface.blit(player, player_rect) # puts the player to the screen

    main_surface.blit(font.render(str(scores), True, BLUE), (width - 30, 0)) # drawing scores

    # for enemy in enemies:
    for enemy in copy(enemies):
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1]) # puts the enemy to the screen

        if enemy[1].left < -enemy[0].get_size()[0]:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]): # test for the collision of 2 objects
            is_working = False

    # for bonus in bonuses:
    for bonus in copy(bonuses):
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1]) # puts the bonus to the screen

        if bonus[1].bottom > (height + bonus[0].get_size()[1]):
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]): # test for the collision of 2 objects
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move(0, player_speed)

    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, -player_speed)

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)

    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0)

    pygame.display.flip() # refreshes the screen
