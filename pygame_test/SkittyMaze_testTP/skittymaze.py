"""
Skitty Maze
Game in which a Skitty has to go through a maze to find an evolution stone.

With the help of
https://openclassrooms.com/fr/courses/1399541-interface-graphique-pygame-pour-python/1400238-tp-dk-labyrinthe
https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python/232721-apprehendez-les-classes

Python script
Files: skittymaze.py, lv1, lv2, lv3 (debug) + images
"""

import pygame
from pygame.locals import *
import time  # for the win animation
pygame.init()


### CONSTANTES #######################################################################################

# window size
nbSprites = 15   # window is 15x15 (sprites)
SpriteWidth = 30
WindowWidth = nbSprites*SpriteWidth

# we actually need the window here for the .convert() and .convert_alpha() to work
window = pygame.display.set_mode((WindowWidth, WindowWidth))

icon = pygame.image.load("icon.png")     # game icon
title = "Skitty Maze (test)"     # window title

# getting the sprites
menu = pygame.image.load("menu.png").convert()
fond = pygame.image.load("fond.png").convert()
wall = pygame.image.load("wall.png").convert()
start = pygame.image.load("start.png").convert()
goal = pygame.image.load("stone.png").convert_alpha()

delcatty = [pygame.image.load("delcatty/0.png").convert_alpha(), \
pygame.image.load("delcatty/1.png").convert_alpha(), \
pygame.image.load("delcatty/2.png").convert_alpha(), \
pygame.image.load("delcatty/3.png").convert_alpha(), \
pygame.image.load("delcatty/4.png").convert_alpha(), \
pygame.image.load("delcatty/5.png").convert_alpha()]
WinWidth = 150

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
        
        return self.orga  # so that we can put it in LevelOrga
    
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
                x = CurrentChar *SpriteWidth
                y = CurrentLine *SpriteWidth

                if char == "S":    #start
                    window.blit(start, (x, y))
                    self.start = (CurrentChar, CurrentLine)   # start's coordinates
                elif char == "G":  #goal
                    window.blit(goal, (x, y))
                    self.goal = (CurrentChar, CurrentLine)    # goal's coordinates
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

    def move(self, LevelOrga):
        """
        - checks if the arrows are being pressed & then moves skitty
        - we need move(LevelOrga)
        """

        if event.key == K_DOWN:
            self.spr = Skitty.down
            self.pos[1] +=1
            if LevelOrga[skitty.pos[1]][skitty.pos[0]] == "W":
                self.pos[1] -=1

        elif event.key == K_UP:
            self.spr = Skitty.up
            self.pos[1] -=1
            if LevelOrga[skitty.pos[1]][skitty.pos[0]] == "W":
                self.pos[1] +=1

        elif event.key == K_LEFT:
            self.spr = Skitty.left
            self.pos[0] -= 1
            if LevelOrga[skitty.pos[1]][skitty.pos[0]] == "W":
                self.pos[0] +=1

        elif event.key == K_RIGHT:
            self.spr = Skitty.right
            self.pos[0] += 1
            if LevelOrga[skitty.pos[1]][skitty.pos[0]] == "W":
                self.pos[0] -=1


### /CLASSES #########################################################################################



pygame.display.set_icon(icon)
pygame.display.set_caption(title)  # window title

Level1, Level2, Level3 = Level("lv1"), Level("lv2"), Level("lv3")
LevelOrga = []  # we'll put the level in there too so that skitty can access it
Menu = True   # menu (or game)
Level = 0  # what level we're on

skitty = Skitty((0,0), Skitty.down)  # creating skitty


def begin(event):
    """
    what level did we choose? + makes it appear
    """

    if event.key == K_a:
        Level = 1
        LevelOrga = Level1.GetLevel()
        Level1.BlitLevel(window)
        skitty.pos = list(Level1.start).copy()  # it's a list so that we can edit it when moving

    elif event.key == K_b:
        Level = 2
        LevelOrga = Level2.GetLevel()
        Level2.BlitLevel(window)
        skitty.pos = list(Level2.start).copy()

    elif event.key == K_SPACE:
        Level = 3
        LevelOrga = Level3.GetLevel()
        Level3.BlitLevel(window)
        skitty.pos = list(Level3.start).copy()
    
    return Level, LevelOrga
    # if we don't do this, Level is never changed bc it just creates a local variable

def win():
    for t in range(5):  # number of loops
        for i in range(6):  # 1 animation cycle
            window.blit(fond, (0, 0))
            window.blit(delcatty[i], ((0.5 *WindowWidth) -(0.5 *WinWidth), (0.5 *WindowWidth) -(0.5 *WinWidth)))
            pygame.display.flip()
            time.sleep(0.15)  # so that we can actually SEE it


##### MAIN LOOP #####

while True:
    while Menu:
        """ menu loop """
        pygame.time.Clock().tick(15)  # restricting the looping per sec
        window.blit(menu, (0,0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit() 

            if event.type == KEYDOWN:
                if event.key == K_a or event.key == K_b or event.key == K_SPACE:
                    Menu = False   # for exiting the menu
                    Level, LevelOrga = begin(event)
                    window.blit(skitty.spr, (skitty.pos[0] *SpriteWidth, skitty.pos[1] *SpriteWidth))
                    pygame.display.flip()

    while not Menu:
        """ game loop """
        pygame.time.Clock().tick(20)  # restricting the looping per sec
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit() 

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Menu = True   # back to the menu
                    skitty.spr = Skitty.down  # back to the starting sprite
                else:
                    skitty.move(LevelOrga)

                    if Level ==1:
                        Level1.BlitLevel(window)
                    elif Level ==2:
                        Level2.BlitLevel(window)
                    elif Level ==3:
                        Level3.BlitLevel(window)
                    window.blit(skitty.spr, (skitty.pos[0] *SpriteWidth, skitty.pos[1] *SpriteWidth))
                    pygame.display.flip()

        if LevelOrga[skitty.pos[1]][skitty.pos[0]] == "G":
            time.sleep(0.4)
            win()
            Menu = True
