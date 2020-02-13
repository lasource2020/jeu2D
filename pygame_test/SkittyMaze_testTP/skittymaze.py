"""
Skitty Maze
Game in which a Skitty has to go through a maze to find an evolution stone.

With the help of
https://openclassrooms.com/fr/courses/1399541-interface-graphique-pygame-pour-python/1400238-tp-dk-labyrinthe
https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python/232721-apprehendez-les-classes

Python script
Files: skittymaze.py, lv1, lv2 + images


NOTES:
- skitty duplicates when moving: problem when blitting?
+ need to implement checking if there's a wall or the window border
+ and checking if we won
+ win screen?

"""

import pygame
from pygame.locals import *
pygame.init()


### CONSTANTES #######################################################################################

# window size
nbSprites = 15   # window is 15x15 (sprites)
SideSprite = 30
SideWindow = nbSprites*SideSprite

# we actually need the window here for the .convert() and .convert_alpha() to work
window = pygame.display.set_mode((SideWindow, SideWindow))

icon = pygame.image.load("icon.png")     # game icon
title = "Skitty Maze (test)"     # window title

# getting the sprites
menu = pygame.image.load("menu.png").convert()
fond = pygame.image.load("fond.png").convert()
wall = pygame.image.load("wall.png").convert()
start = pygame.image.load("start.png").convert()
goal = pygame.image.load("stone.png").convert_alpha()

### /CONSTANTES ######################################################################################



### CLASSES ##########################################################################################

class Level:
    """
    in which we attempt to generate levels with a (file).
    """

    def __init__(self, file):
        self.file = file
        self.orga = []  # we'll put the level from the file in there later
        self.start = 0  # where's the start
        self.goal = 0  # where's the goal

    def GetLevel(self):
        """
        - we are getting the levels as a list of lines (str)
        - use orga[i][i] to access each square?
        """

        with open(self.file) as lv:
            self.orga = lv.read().split("\n")
    
    def BlitLevel(self, window):
        """
        - we make the level appear
        - we need .BlitLevel(window)
        """
        
        window.blit(fond, (0,0))

        CurrentLine = 0
        for line in self.orga:
            CurrentChar = 0

            for char in line:
                x = CurrentChar *SideSprite
                y = CurrentLine *SideSprite

                if char == "S":    #start
                    window.blit(start, (x, y))
                    self.start = (x, y)   # start's coordinates
                elif char == "G":  #goal
                    window.blit(goal, (x, y))
                    self.goal = (x, y)    # goal's coordinates
                elif char == "W":  #wall
                    window.blit(wall, (x, y))
                
                CurrentChar +=1
            CurrentLine +=1


class Skitty:
    """
    - for the playable character.
    - takes (position, current sprite)
    """

    up, down, right, left = pygame.image.load("skit-up.png").convert_alpha(), \
    pygame.image.load("skit-down.png").convert_alpha(), \
    pygame.image.load("skit-right.png").convert_alpha(), \
    pygame.image.load("skit-left.png").convert_alpha()

    def __init__(self, pos, spr):
        self.pos = pos  #position
        self.spr = spr  #current sprite

    def move(self):
        """
        checks if the arrows are being pressed & then moves skitty
        """

        if event.key == K_DOWN:
            self.spr = Skitty.down
            self.pos[1] += SideSprite
        elif event.key == K_UP:
            self.spr = Skitty.up
            self.pos[1] -= SideSprite
        elif event.key == K_LEFT:
            self.spr = Skitty.left
            self.pos[0] -= SideSprite
        elif event.key == K_RIGHT:
            self.spr = Skitty.right
            self.pos[0] += SideSprite


### /CLASSES #########################################################################################



pygame.display.set_icon(icon)
pygame.display.set_caption(title)  # window title

Level1, Level2 = Level("lv1"), Level("lv2")
Menu = True   # menu (or game)
Level = 0  # what level we're on

skitty = Skitty((0,0), Skitty.down)  # creating skitty


def begin(event):
    """
    what level did we choose? + makes it appear
    """

    if event.key == K_a:
        Level = 1
        Level1.GetLevel()
        Level1.BlitLevel(window)
        skitty.pos = list(Level1.start).copy()  # it's a list so that we can edit it when moving

    elif event.key == K_b:
        Level = 2
        Level2.GetLevel()
        Level2.BlitLevel(window)
        skitty.pos = list(Level2.start).copy()  # it's a list so that we can edit it when moving


# MAIN LOOP
while True:
    while Menu:
        """ menu loop """
        pygame.time.Clock().tick(15)  # restricting the looping
        window.blit(menu, (0,0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit() 

            if event.type == KEYDOWN:
                if event.key == K_a or event.key == K_b:
                    Menu = False   # for exiting the menu
                    begin(event)
                    window.blit(skitty.spr, skitty.pos)
                    pygame.display.flip()

    while not Menu:
        """ game loop """
        pygame.time.Clock().tick(20)  # restricting the looping
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit() 

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Menu = True   # back to the menu
                    skitty.spr = Skitty.down  # back to the starting sprite
                else:
                    skitty.move()
            
        # this is supposed to prevent the duplicating skitty by re-blitting everything
        # but apparently it doesn't
        if Level ==1:
            Level1.BlitLevel(window)
        elif Level ==2:
            Level2.BlitLevel(window)
        window.blit(skitty.spr, skitty.pos)
        pygame.display.flip()