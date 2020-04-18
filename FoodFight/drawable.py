import pygame
from pygame import image
import os
from frameManager import FrameManager
from vector2D import Vector2

class Drawable(object):
   """Anything that can be drawn in the game inherits from this class."""
   
   WINDOW_OFFSET = Vector2(0,0)
   SCALE = 3
   
   def __init__(self, imageName, position, offset=None, parallax=1):
      self._imageName = imageName
      if self._imageName != "":
         self._image = FrameManager.getInstance().getFrame(imageName, offset)
      self._worldBound = True
      self._position = Vector2(*position)
      self._parallax = parallax
      
   @classmethod   
   def updateOffset(cls, trackingObject, screenSize, worldSize):
   # Offset is based on the thing we are following
   #  Using max(0, NUM) will clip it to a positive number
   #  Using min(NUM, MAX_SIZE) will clip it to the size of the world boundaries
   #  Using min(max(0, NUM), MAX_SIZE) will clip it to inside the world boundaries
      position = trackingObject.getPosition()
      size = trackingObject.getSize()
      Drawable.WINDOW_OFFSET = [min(max(0, position[x] - screenSize[x] // 2 + size[x] // 2), worldSize[x] - screenSize[x]) for x in range(2)]


   @classmethod   
   def adjustMousePos(cls, mousePos):
      #given a mouse position relative to the screen, returns mouse position adjusted to the world
      ret = Vector2(*mousePos)
      ret //= Drawable.SCALE
      ret += Drawable.WINDOW_OFFSET
      
      return ret
      
   def getPosition(self):
      return self._position

   def setPosition(self, newPosition):
      self._position = newPosition
      
   def getSize(self):
      return self._image.get_size()

   def getCollideRect(self):
      #returns a rect variable representing the collision area of the object
      newRect =  self._position + self._image.get_rect()
      return newRect
   
   def draw(self, surface):
      #draws image at curent position based on window offset
      #if self._worldBound:
      surface.blit(self._image, (int(self._position[0] - Drawable.WINDOW_OFFSET[0] * self._parallax),
                                 int(self._position[1] - Drawable.WINDOW_OFFSET[1] * self._parallax)))
      #else:
      #   surface.blit(self._image, self._position)

   def getX(self):
      return self._position[0]
   
   def getY(self):
      return self._position[1]

   def getWidth(self):
      return self._image.get_width()
    
   def getHeight(self):
      return self._image.get_height()

     

