from pygame.locals import *
import pygame

screen = pygame.display.set_mode((600, 600))
player = pygame.image.load("guy.png")
bg = pygame.image.load("bg.png")
block = 3
b_block = 50
x,y = 15,15
enemy = False
b_y, b_x = 0, 0
right, left, up, down = False, False, False ,False
b_up, b_down, b_left, b_right = False, False, False, False
while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                b_y, b_x = y, x
                if not b_up and not b_down and not b_left and not b_right:
                    b_right = True
            if event.key == K_LEFT:
                b_y, b_x, = y,x
                if not b_up and not b_down and not b_left and not b_right:
                    b_left = True
            if event.key == K_UP:
                b_y, b_x = y, x
                if not b_up and not b_down and not b_left and not b_right:
                    b_up = True
            if event.key == K_DOWN:
                b_y, b_x = y,x
                if not b_up and not b_down and not b_left and not b_right:
                    b_down = True
        if event.type == KEYDOWN and event.key == K_d:
            right = True
        else:
            right = False
        if event.type == KEYDOWN and event.key == K_a:
            left = True
        else:
            left = False
        if event.type == KEYDOWN and event.key == K_s:
            down = True
        else:
            down = False
        if event.type == KEYDOWN and event.key == K_w:
            up = True
        else:
            up = False 
    if b_up:
        b_y -= b_block
        if b_y <= 0:
            b_up = False
        screen.blit(pygame.image.load("bullet.png"), (b_x, b_y))
    if b_down:
        b_y += b_block
        if b_y >= 550:
            b_down = False
        screen.blit(pygame.image.load("bullet.png"), (b_x, b_y))
    if b_left:
        b_x -= b_block
        if b_x <= 0:
            b_left = False
        screen.blit(pygame.image.load("bullet.png"), (b_x, b_y))
    if b_right:
        b_x += b_block
        if b_x >= 550:
            b_right = False
        screen.blit(pygame.image.load("bullet.png"), (b_x, b_y))
    if up:
        if y <= 15:
            up = False
        y -= block
    if down:
        if y >= 550:
            down = False
        y += block

    if right:
        if x >= 550:
            right = False
        x += block
    if left:
        if x <= 15:
            left = False
        x -= block
    pygame.display.update() 
    screen.blit(bg, (0,0))
    screen.blit(player, (x, y))
