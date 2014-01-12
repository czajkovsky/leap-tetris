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

  def start_move(self, direction):
    if direction == 'DOWN':
      self.board.key_down_flag = True
    else:
      if self.board.last_strafe == 0:
        if direction == 'LEFT':
          self.board.current_gp.move_left()
          self.board.key_left_flag = True
        elif direction == 'RIGHT':
          self.board.current_gp.move_right()
          self.board.key_right_flag = True
        self.board.last_strafe = (pygame.time.get_ticks()+250)

  def stop_move(self, direction):
    if direction == 'DOWN':
      self.board.key_down_flag = False
    else:
      self.board.last_strafe = 0
      if direction == 'LEFT':
        self.board.key_left_flag = False
      elif direction == 'RIGHT':
        self.board.key_right_flag = False

  def rotate(self):
    self.board.current_gp.rotate()

  def redraw(self):
    self.board.update(pygame.time.get_ticks())
    screen.fill((175,175,175))
    self.board.draw(screen)
    if self.board.game_over:
      self.board.puase = True
      x = screen_w
      y = screen_h
      xx = game_over_image.get_width()
      yy = game_over_image.get_height()
      screen.blit(game_over_image, ((x - xx)/2, (y - yy)/2))
    pygame.display.flip()

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
        if event.key == pygame.K_LEFT:
          game.start_move('LEFT')
        if event.key == pygame.K_RIGHT:
          game.start_move('RIGHT')
        if event.key == pygame.K_DOWN:
          game.start_move('DOWN')
        if event.key == pygame.K_UP:
          game.rotate()
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
          game.stop_move('DOWN')
        if event.key == pygame.K_LEFT:
          game.stop_move('LEFT')
        if event.key == pygame.K_RIGHT:
          game.stop_move('RIGHT')
    game.redraw()
  pygame.quit()

if __name__ == "__main__":
    main()



