"""
Jello
Kelly Amar
"""
import os
import pygame
import math 
from vector2D import Vector2
import random
from drawable import *
from Players import *
from pauser import *
from food import *
from backgrounds import *
from menu import *

# Two different sizes now! Screen size is the amount we show the player,
#  and world size is the size of the interactable world
SCREEN_SIZE = Vector2(600, 400)
WORLD_SIZE = Vector2(1600, 1600)

SCALE = 2
UPSCALED = [x * SCALE for x in SCREEN_SIZE]


def reset(dif = "easy"):
   global enemies
   global food
   global player
   global score
   global gameOverWin
   global gameOverLose
   global maxFood
   global timeAmount
   #list of enemies
   if dif == "easy":
      enemies = [Enemy((0,0)), Enemy((0,0)), Enemy((0,0)), Enemy((0,0)),
              Enemy((1800, 1800)), Enemy((1800, 1800)), Enemy((1800, 1800)),
              Enemy((900,1800)), Enemy((900,1800)), Enemy((900, 1200)), Enemy((900, 1200)),
              Enemy((500, 1200)), Enemy((500, 1200))]
      #player 
      player = Player((WORLD_SIZE[0]//2,WORLD_SIZE[1]//2))
      #displays food time and amount
      maxFood = 250
      timeAmount = 0.4
   else:
      enemies = [EnemyHard((0,0)), EnemyHard((0,0)), EnemyHard((0,0)), EnemyHard((0,0)),
              EnemyHard((1800, 1800)), EnemyHard((1800, 1800)), EnemyHard((1800, 1800)),
              EnemyHard((900,1800)), EnemyHard((900,1800)), EnemyHard((900, 1200)), EnemyHard((900, 1200)),
              EnemyHard((500, 1200)), EnemyHard((500, 1200)), EnemyHard((1500, 1500)), EnemyHard((1500, 1500)),
              EnemyHard((1500, 1500))]
      #player 
      player = PlayerHard((WORLD_SIZE[0]//2,WORLD_SIZE[1]//2))
      #displays food time and amount
      maxFood = 150
      timeAmount = 1.5
      

   #list of food
   food = []
   #player 
   player = Player((WORLD_SIZE[0]//2,WORLD_SIZE[1]//2))
   #player score
   score = 0
   #game status 
   gameOverWin = False
   gameOverLose = False
   print("reset easy happened")



def main():

   global enemies
   global food
   global player
   global score
   global gameOverWin
   global gameOverLose
   global maxFood
   global timeAmount
   
   # initialize the pygame module
   pygame.init()
   #initialize the mixer
   eatNoise = pygame.mixer.Sound("eat.wav")
   
   # load and set the logo

   pygame.display.set_caption("Food Fight")
   
   #display screen
   screen = pygame.display.set_mode(list(UPSCALED))
   drawSurf = pygame.Surface(list(SCREEN_SIZE))

   #create background
   background = SemiTransparentBackground(pygame.Rect(0,0,WORLD_SIZE[0],WORLD_SIZE[1]), "background.png", (0,0), None, 1)
   
   #menu setup
   menuList = BaseMenu(Vector2(50,50), "menu1.csv")

   # Make a game clock for nice, smooth animations
   gameClock = pygame.time.Clock()

   #reset
   reset()


   #properties of food
   foodTimer = 0

   #pauser to pause the game
   pauser = Pauser(SCREEN_SIZE)

   #win
   winner = Win(SCREEN_SIZE)

   #lose
   loser = Lose(SCREEN_SIZE)

   # The offset of the window into the world
   offset = Vector2(0,0)

   #on screen score properties
   font = pygame.font.SysFont('comicsans', 30, True)
   
   # define a variable to control the main loop
   running = True
   
   # main loop
   while running:

      # Let our game clock tick at 60 fps, ALWAYS
      gameClock.tick(60)
      
      
      # Draw everything, based on the offset
      drawSurf.fill((255,255,255))
      background.draw(drawSurf)
      #only draw menu if menu is active
      if menuList.isActive():
         menuList.draw(drawSurf)
      else:
         #text in top right of the screen
         text = font.render('Score: ' + str(score), 1, (0,0,0))
         drawSurf.blit(text, (475,10))
         for enemy in enemies:
            enemy.draw(drawSurf)
         player.draw(drawSurf)
         pauser.draw(drawSurf)
         loser.draw(drawSurf)
         winner.draw(drawSurf)
         for f in food:
            f.draw(drawSurf)
      



      pygame.transform.scale(drawSurf, UPSCALED, screen)
      
      # Flip the display to the monitor
      pygame.display.flip()

      
      
      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or ESCAPE is pressed
         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False, to exit the main loop
            running = False
         else:
            #displays you lose
            if loser.isActive():
               loser.handleEvent(event)
               print("loser not active")
               if not loser.isActive():
                  #reset everything
                  reset()
                  menuList._active = True
            #displays you win
            elif winner.isActive():
               winner.handleEvent(event)
               if not winner.isActive():
                  #reset everything
                  reset()
                  menuList._active = True
            #displays the menu
            elif menuList.isActive():
               ret = menuList.handleEvent(event)
               if ret != "":
                  reset(ret)
            #lets player play the game
            else:
               pauser.handleEvent(event)
               if not pauser.isActive():
                  player.handleEvent(event)
                  
         
            


      # Get some time in seconds
      ticks = min(0.5, gameClock.get_time() / 1000)
      
      # Update everything
      if not pauser.isActive() and not loser.isActive() and not winner.isActive():
         player.update(ticks, WORLD_SIZE)
         for enemy in enemies:
             enemy.update(ticks, WORLD_SIZE)
             
         #populates the screen with food circles 
         foodTimer -= ticks
         if foodTimer < 0:
            foodTimer = timeAmount
            circlePos = (random.randint(0, WORLD_SIZE[0]), random.randint(0, WORLD_SIZE[1]))
            if len(food) < maxFood:
               food.append(Food(circlePos))  

         #update offset

         Drawable.updateOffset(player, SCREEN_SIZE, WORLD_SIZE)

      #check to see if any orbs have collided with food
      #increases size of player/enemy if collided with food


      for f in food:
          if player.getCollideRect().colliderect(f.getCollideRect()) == True:
              f.kill()
              player._foodEaten += 1
              #increases the score displayed on screen
              score += 1
              #plays sound when food is eaten
              eatNoise.play()

      for f in food:
         for enemy in enemies:
            if enemy.getCollideRect().colliderect(f.getCollideRect()) == True:
               f.kill()
               enemy._foodEaten += 1
               #eatNoise.play()

      #checks if player/enemy run into each other
      #compares size and who gets killed
              
      for enemy in enemies:
         if player.getCollideRect().colliderect(enemy.getCollideRect()) == True:
            if enemy.getSize() > player.getSize():
               player.kill()
               player.isDead()
            elif enemy.getSize() < player.getSize():
               enemy.kill()
               print('enemydied')
            elif enemy.getSize() == player.getSize():
               player.kill()
               player.isDead()

      #did anyone food get eaten
      #did any enemy die         
      enemies = [enemy for enemy in enemies if not enemy.isDead()]
      food = [f for f in food if not f.isDead()]

      #check if game over
      if player.count >= player.max_food and not gameOverLose and not gameOverWin:
         gameOverWin = True
         player.win = True
      elif player.isDead() and not gameOverLose and not gameOverWin:
         gameOverLose = True
         player.lose = True
         
      #display win or lose screen
      if gameOverWin == True:
         winner._active = True
      if gameOverLose == True:
         loser._active = True




   pygame.quit()


   
if __name__ == "__main__":
   main()
