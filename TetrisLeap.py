import pygame
from pygame.locals import *
from Game_Board import *
from sys import exit

class GameEngine:

  def __init__(self):
    self.running = True
    self.board = GameBoard()
    self.board.initialize(pygame.time.get_ticks())

  def stop(self):
    self.running = False

  def isRunning(self):
    return self.running

  def isPaused(self):
    return self.board.paused

  def showGrid(self):
    self.board.toggle_grid()
    self.board.update(pygame.time.get_ticks())

def main():

  game = GameEngine()

  while game.isRunning():
    for event in pygame.event.get():
      if game.isPaused():
        break
      if event.type == pygame.QUIT:
        game.stop()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          game.stop()
        if event.key == pygame.K_g:
          game.showGrid()
  pygame.quit()

if __name__ == "__main__":
    main()



