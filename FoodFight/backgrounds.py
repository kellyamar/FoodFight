from drawable import Drawable
from vector2D import Vector2
import pygame

class RepeatingBackground(object):
   
   def __init__(self, areaRect, fileName="background.png", position=(0,0), offset=None, parallax=1):
      self._area = areaRect
      self._position = Vector2(*position)
      
      # Load one tile to get the width and height
      self._tiles = [Drawable(fileName, (self._position.x, self._position.y), offset, parallax)]
      
      tileSize = self._tiles[0].getSize()
         
      for x in range(self._area.left + tileSize[0], self._area.width, tileSize[0]):
         for y in range(self._area.top, self._area.height, tileSize[1]):
         
            self._tiles.append(Drawable(fileName, (self._position.x + x, self._position.y + y), offset, parallax))
         
   
   
   def draw(self, surface):
      
      for tile in self._tiles:
         tile.draw(surface)
         

class SemiTransparentBackground(RepeatingBackground):
   def __init__(self, areaRect, fileName="background.png", position=(0,0), offset=None, parallax=1):
      super().__init__(areaRect, fileName, position, offset, parallax)
      
      for tile in self._tiles:
         tile._image.set_alpha(100)
   
