from drawable import Drawable
from vector2D import Vector2

import pygame
import os

class BaseMenu(Drawable):
   _MENU_FOLDER = os.path.join("resources", "menus")
   
   def __init__(self, position, fileName):
      super().__init__("", position)
      
      self._hPad = 4
      self._vPad = 4


      self._active = True
      
      if not pygame.font.get_init():
         pygame.font.init()
      #sets color and font 
      self._fontColor = pygame.Color("BLUE")
      self._fontSize = 20
      self._font = pygame.font.Font(os.path.join("resources", "fonts", "RobotoBlack.ttf"), self._fontSize)
      
      self._loadOptionList(fileName)
      
   
   def _loadOptionList(self, fileName):
      textFile = open(os.path.join(BaseMenu._MENU_FOLDER, fileName))
      
      self._list = [[y for y in x.split(",")] for x in textFile.read().split("\n")]
      self._renderList()
      
      textFile.close()
      
   def _renderList(self):
      self._renderedList = [[self._font.render(x, False, self._fontColor) for x in y] for y in self._list]

      self._width = self._renderedList[0][0].get_width() + self._hPad
      self._height = self._renderedList[0][0].get_height() + self._vPad
      
   def reset(self):
      pass

   def isActive(self):
      return self._active
      
   def draw(self, surface):
      #draws rendered list to screen
      for i in range(len(self._renderedList)):
         for j in range(len(self._renderedList[i])):
            surface.blit(self._renderedList[i][j], (self._position.x + self._width * j,
                                                    self._position.y + self._height * i))
   def handleEvent(self, event):
      #key presses for differnt levels 
      if event.type == pygame.KEYDOWN and pygame.K_1:
         self._active = not self._active
         return "easy"
      elif event.type == pygame.KEYDOWN and pygame.K_2:
         self._active = not self._active
         return "hard"

      return ""
