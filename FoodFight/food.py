from drawable import Drawable
from vector2D import Vector2
import random
import pygame
import math



class Food(Drawable):
    def __init__(self, position):
        
        super().__init__("", position)
        #draw circles
        radius = 5


        self._image = pygame.Surface((10,10), pygame.SRCALPHA)
        #random color
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        #sets circle 
        pygame.draw.circle(self._image, color, (5,5), radius)

        self._dead = False

    def kill(self):
        #is true if food has been hit by enemy or player
        self._dead = True
        
    def isDead(self):
        #returns state of food
        return self._dead
