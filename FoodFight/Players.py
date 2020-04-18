import os
import pygame
import math
from vector2D import Vector2
import random
from drawable import *
from food import *



class Enemy(Drawable):
    def __init__(self, position):
        
        
        super().__init__("enemy.png", position)
        
        #sets velocity
        self._velocity = Vector2(random.random() * 100 - 50, random.random() * 100 - 50)
        self._velocity.scale(100)
        
        self.dead = False

        self.win = False
        
        #tracks each time the enemy eats 5 pieces of food
        self._foodEaten = 0
        
        #maximum size of enemies
        self.maxfoodEaten = 15
        
        #counts how big the enemy gets
        self.count = 0
        
        #displays enemy so that the edges are clean when it grows
        self.original_image = self._image
        self.scaleFactor = 0.5
        self._image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * self.scaleFactor),
                                                               int(self.original_image.get_height() * self.scaleFactor)))
        
 
    def Grow(self):
        #tracks when food eaten gets to 5
        if self._foodEaten == 5:
            #increase count by 1
            self.count += 1
            print("enemy count: " + str(self.count))
            #if count is greater than max food, resets food eaten to 0 
            if self.count >= self.maxfoodEaten:
                print("enemy at max size")
                self._foodEaten = 0
            else:
                #if count is not greater than max food, increase size and reset food eaten to 0
                self.scaleFactor *= 1.1
                self._image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * self.scaleFactor),
                                                               int(self.original_image.get_height() * self.scaleFactor)))
                print("enemygrowed")
                self._foodEaten = 0
        return self._foodEaten
                
    def update(self, ticks, worldInfo):

        #Updates the orb's position based on its current velocity

        #applies bounce behavior
        
        #increases in size if enemy has grown
        self.Grow()
        
        distanceVector = self._velocity * ticks
        newPosition = self.getPosition() + distanceVector
        
 
        
        for dim in range(len(self.getSize())):
           if newPosition[dim] + self.getSize()[dim] > worldInfo[dim] or newPosition[dim] < 0:
              self._velocity[dim] = -self._velocity[dim]

           distanceVector = self._velocity * ticks
           newPosition = self.getPosition() + distanceVector
              
        self.setPosition(newPosition)
        
    def kill(self):
        #set to true if enemy is hit by bigger player
        self.dead = True
        
    def isDead(self):
        return self.dead

    def getSize(self):
        #returns size for player/enemy comparison
        return self._image.get_size()


class EnemyHard(Drawable):
    def __init__(self, position):
        super().__init__("enemy.png", position)
        
      
        self._velocity = Vector2(random.random() * 100 - 50, random.random() * 100 - 50)
        self._velocity.scale(150)

        self.dead = False

        self.win = False
        #tracks each time the enemy eats 5 pieces of food
        self._foodEaten = 0
        
        #maximum size of enemies
        self.maxfoodEaten = 20

        #counts how big the enemy gets
        self.count = 0

        #displays enemy so that edges are clean when it grows 
        self.original_image = self._image
        self.scaleFactor = 0.5
        self._image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * self.scaleFactor),
                                                               int(self.original_image.get_height() * self.scaleFactor)))
        
 
    def Grow(self):
        #tracks when food eaten gets to 5
        if self._foodEaten == 3:
            #increases count by 1
            self.count += 1
            print("enemy count: " + str(self.count))
            #if count is greater than max size, reset food eaten to zero
            if self.count >= self.maxfoodEaten:
                print("enemy at max size")
                self._foodEaten = 0
            else:
                #player grows in size and food eaten is reset to 0
                self.scaleFactor *= 1.1
                self._image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * self.scaleFactor),
                                                               int(self.original_image.get_height() * self.scaleFactor)))
                print("enemygrowed")
                self._foodEaten = 0
        return self._foodEaten
                
    def update(self, ticks, worldInfo):

        #Updates the orb's position based on its current velocity

        #applies bounce behavior

        #increases in size if enemy has grown
        self.Grow()
        
        distanceVector = self._velocity * ticks
        newPosition = self.getPosition() + distanceVector
        
 
        
        for dim in range(len(self.getSize())):
           if newPosition[dim] + self.getSize()[dim] > worldInfo[dim] or newPosition[dim] < 0:
              self._velocity[dim] = -self._velocity[dim]

           distanceVector = self._velocity * ticks
           newPosition = self.getPosition() + distanceVector
              
        self.setPosition(newPosition)
        
    def kill(self):
        #set to true if bigger player hits enemy 
        self.dead = True
        
    def isDead(self):
        return self.dead

    def getSize(self):
        #returns size for player/enemy comparison
        return self._image.get_size()
    

class Player(Drawable):
    def __init__(self, position):

        self._velocity = Vector2(0,0)
        self._maxVelocity = 90
        self._acceleration = 30

        #tracks state of player
        self._dead = False
        self.win = False
        self.lose = False

        #tracks each time the player collects 5 food circles
        self._foodEaten = 0
        #maximum amount of food and win score
        self.max_food = 15
        #tracks how big the player gets
        self.count = 0

        self._movement = { pygame.K_UP: False,
                         pygame.K_DOWN: False,
                         pygame.K_LEFT: False,
                         pygame.K_RIGHT: False
                         }
        
        super().__init__("player.png", position)
        #displays enemy so that the edges are clean when it grows
        self.original_image = self._image
        self.scaleFactor = 0.5
        self._image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * self.scaleFactor),
                                                               int(self.original_image.get_height() * self.scaleFactor)))
      
        
        
    def handleEvent(self, event):
      #handles key press events 
      if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
         if event.key in self._movement.keys():
            self._movement[event.key] = (event.type == pygame.KEYDOWN)
            

    
    def Grow(self):
        #counts up to 5 
        if self._foodEaten == 5:
            #adds 1 to count
            self.count += 1
            print("player count: " + str(self.count))
            #if count is greater than max food doesn't change size but resets food eaten to 0
            if self.count >= self.max_food:
                self._foodEaten = 0
            else:
                #if count is kess than max food increase size and resets food eaten to 0
                self.scaleFactor *= 1.1
                self._image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * self.scaleFactor),
                                                               int(self.original_image.get_height() * self.scaleFactor)))
                print("growed")
                self._foodEaten = 0
        return self._foodEaten
    

        
    def update(self, ticks, worldInfo):
        #updates grow
        self.Grow()
        
        #when given an event, updates the velocity
        if self._movement[pygame.K_UP]:
            self._velocity[1] -= self._acceleration * ticks
        elif self._movement[pygame.K_DOWN]:
            self._velocity[1] += self._acceleration * ticks
        elif self._movement[pygame.K_LEFT]:
            self._velocity[0] -= self._acceleration * ticks
        elif self._movement[pygame.K_RIGHT]:
            self._velocity[0] += self._acceleration * ticks
      



        if self._velocity.magnitude() > self._maxVelocity:
            self._velocity.scale(self._maxVelocity)

        distanceVector = self._velocity * ticks
        newPosition = self.getPosition() + distanceVector
        
 
        
        for dim in range(len(self.getSize())):
           if newPosition[dim] + self.getSize()[dim] > worldInfo[dim] or newPosition[dim] < 0:
              self._velocity[dim] = -self._velocity[dim]

           distanceVector = self._velocity * ticks
           newPosition = self.getPosition() + distanceVector
              
        self.setPosition(newPosition)

    def kill(self):
        self._dead = True
        
    def isDead(self):
        return self._dead

    def getSize(self):
        #returns size for player/enemy comparison
        return self._image.get_size()

    def win(self):
        return self.win
    
    def lose(self):
        return self.lose

    
class PlayerHard(Drawable):
    def __init__(self, position):

        self._velocity = Vector2(0,0)
        self._maxVelocity = 75
        self._acceleration = 25

        #tracks player state 
        self._dead = False
        self.win = False
        self.lose = False

        #tracks each time a player collects 5 food circles
        self._foodEaten = 0

        #sets how big the player can get and the win size
        self.max_food = 20
        
        #tracks how big the player gets
        self.count = 0
        
        self._movement = { pygame.K_UP: False,
                         pygame.K_DOWN: False,
                         pygame.K_LEFT: False,
                         pygame.K_RIGHT: False
                         }
        
        super().__init__("playerHard.png", position)
        #sets images so that when it grows the edges are clean
        self.original_image = self._image
        self.scaleFactor = 0.5
        self._image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * self.scaleFactor),
                                                               int(self.original_image.get_height() * self.scaleFactor)))
      
        
        
    def handleEvent(self, event):
      #handles arrow key press
      if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
         if event.key in self._movement.keys():
            self._movement[event.key] = (event.type == pygame.KEYDOWN)
            

    
    def Grow(self):
        #tracks when food eaten gets to 5
        if self._foodEaten == 5:
            #increases count by 1
            self.count += 1
            print("player count: " + str(self.count))
            #if count is greater than max size, reset food eaten to 0
            if self.count >= self.max_food:
                self._foodEaten = 0
            else:
                #increase player size and reset food eaten to 0
                self.scaleFactor *= 1.1
                self._image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * self.scaleFactor),
                                                               int(self.original_image.get_height() * self.scaleFactor)))
                print("growed")
                self._foodEaten = 0
        return self._foodEaten
    

        
    def update(self, ticks, worldInfo):
        #updates grow 
        self.Grow()
        
        #when given an event, updates the velocity
        if self._movement[pygame.K_UP]:
            self._velocity[1] -= self._acceleration * ticks
        elif self._movement[pygame.K_DOWN]:
            self._velocity[1] += self._acceleration * ticks
        elif self._movement[pygame.K_LEFT]:
            self._velocity[0] -= self._acceleration * ticks
        elif self._movement[pygame.K_RIGHT]:
            self._velocity[0] += self._acceleration * ticks
      



        if self._velocity.magnitude() > self._maxVelocity:
            self._velocity.scale(self._maxVelocity)

        distanceVector = self._velocity * ticks
        newPosition = self.getPosition() + distanceVector
        
 
        
        for dim in range(len(self.getSize())):
           if newPosition[dim] + self.getSize()[dim] > worldInfo[dim] or newPosition[dim] < 0:
              self._velocity[dim] = -self._velocity[dim]

           distanceVector = self._velocity * ticks
           newPosition = self.getPosition() + distanceVector
              
        self.setPosition(newPosition)

    def kill(self):
        self._dead = True
        
    def isDead(self):
        return self._dead

    def getSize(self):
        #returns size for player/enemy comparison
        return self._image.get_size()

    def win(self):
        return self.win
    
    def lose(self):
        return self.lose 
