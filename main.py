import random
import pygame
from pygame.constants import QUIT
# Python has no constants on it's own, 
# so UPPERCASED var names are meant to mark vars that must not be changed since their creation to be used as constants

def random_color(): # returns a random, non-dark color
    return (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255))

screen = width, height = 800, 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
main_surface = pygame.display.set_mode(screen)

ball = pygame.Surface((20, 20))
ball.fill(WHITE) # fills the ball with a color
ball_rect = ball.get_rect()
ball_speed = [1, 1] # "speed"? looks more like a shift amount while moving the ball

is_working = True

while is_working:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

    ball_rect = ball_rect.move(ball_speed)

    if ball_rect.bottom >= height or ball_rect.top <= 0: # if the ball reaches the bottom or the top of the screen...
        ball_speed[1] = -ball_speed[1] # ...change it vertical direction
        ball.fill(random_color())

    if ball_rect.right >= width or ball_rect.left <= 0: # if the ball reaches the right edge or the left edge of the screen...
        ball_speed[0] = -ball_speed[0] # ...change it horizontal direction
        ball.fill(random_color())

    main_surface.fill(BLACK) # fills the screen with a color
    main_surface.blit(ball, ball_rect) # puts the ball to the screen
    pygame.display.flip() # refreshes the screen
