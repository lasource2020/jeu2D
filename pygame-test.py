### testin stuff out

import pygame
from pygame.locals import *
pygame.init()

Wx, Wy = 1080, 864   # width and height
follow = False       # for moving by arrows (not mouse)

window = pygame.display.set_mode((Wx, Wy))

def keydown(event):             # moving w/ arrows
    if event.key == K_DOWN:
        coord_mite[1] += 3
    elif event.key == K_UP:
        coord_mite[1] -= 3
    elif event.key == K_LEFT:
        coord_mite[0] -= 3
    elif event.key == K_RIGHT:
        coord_mite[0] += 3

pygame.key.set_repeat(400, 30)
        
# background loop
bckg = pygame.image.load('blue_crystal.png').convert()
for x in range(0, Wx, 500):
    for y in range(0, Wy, 500):
        window.blit(bckg, (x, y))

# character
mite = pygame.image.load('shardmite.png').convert_alpha()
coord_mite = mite.get_rect()
window.blit(mite, coord_mite)
   
pygame.display.flip()

# GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        
        elif event.type == KEYDOWN and not follow:
            keydown(event)
        
        elif event.type == MOUSEBUTTONDOWN:
            if follow:
                follow = False
            else: # not follow
                follow = True
        
        elif event.type == MOUSEMOTION and follow:
            coord_mite = list(event.pos).copy()
        
    for x in range(0, Wx, 500):
        for y in range(0, Wy, 500):
            window.blit(bckg, (x, y))
    window.blit(mite, coord_mite)
    pygame.display.flip()