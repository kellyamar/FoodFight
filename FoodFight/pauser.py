
from drawable import Drawable
from vector2D import Vector2
import pygame

class Pauser(Drawable):
   def __init__(self, screenSize):
      self._active = False
      super().__init__("paused.png", screenSize // 2, parallax=0)
      
      self._position -= Vector2(*self.getSize()) // 2
      
   
   def handleEvent(self, event):
      #stops program if 'p' is pressed
      if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
         self._active = not self._active
   
   
   def draw(self, surface):
      #draws the pauser
      if self._active:
         super().draw(surface)
   
   
   def isActive(self):
      #returns state of pausert
      return self._active

class Win(Drawable):
   def __init__(self, screenSize):
      self._active = False
      super().__init__("youwin.png", screenSize // 2, parallax=0)
      self._position -= Vector2(*self.getSize()) // 2

   def handleEvent(self, event):
      #if the space bar is pressed, message stops displaying
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
         self._active = not self._active
   
   def draw(self, surface):
      #draws you win 
      if self._active:
         super().draw(surface)

   def isActive(self):
      #returns state of win
      return self._active
   
class Lose(Drawable):
   def __init__(self, screenSize):
      self._active = False
      super().__init__("youlose.png", screenSize // 2, parallax=0)
      self._position -= Vector2(*self.getSize()) // 2
   
   def handleEvent(self, event):
      #if the space bar is pressed, message stops displaying
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
         self._active = not self._active
         
   def draw(self, surface):
      #draws you lose
      if self._active:
         super().draw(surface)
         
   def isActive(self):
      #returns state of lose
      return self._active
   
      
