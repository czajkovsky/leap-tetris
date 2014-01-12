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

  def run(self):
    running = self.running
    board = self.board
    while running:
      for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            stop_game()
          if event.key == pygame.K_g:
            board.toggle_grid()
            board.update(pygame.time.get_ticks())
          if event.key == pygame.K_s:
            board.slow_time = not board.slow_time
          if event.key == pygame.K_LEFT:
            if board.last_strafe == 0:
              board.current_gp.move_left()
              board.last_strafe = (pygame.time.get_ticks()+250)
              board.key_left_flag = True
          if event.key == pygame.K_RIGHT:
            if board.last_strafe == 0:
              board.current_gp.move_right()
              board.last_strafe = (pygame.time.get_ticks()+250)
              board.key_right_flag = True
          if event.key == pygame.K_DOWN:
            board.key_down_flag = True
          if event.key == pygame.K_UP:
            board.current_gp.rotate()
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_DOWN:
            board.key_down_flag = False
          if event.key == pygame.K_LEFT:
            board.key_left_flag = False
            board.last_strafe = 0
          if event.key == pygame.K_RIGHT:
            board.key_right_flag = False
            board.last_strafe = 0
      board.update(pygame.time.get_ticks())
      screen.fill((175,175,175))
      board.draw(screen)
      if board.game_over:
        board.puase = True
        x = screen_w
        y = screen_h
        xx = game_over_image.get_width()
        yy = game_over_image.get_height()
        screen.blit(game_over_image, ((x - xx)/2, (y - yy)/2))
      pygame.display.flip()
    pygame.quit()

def main():

  game = GameEngine()
  # game.run()

  while game.isRunning():
    for event in pygame.event.get():
      if game.isPaused():
        break
      if event.type == pygame.QUIT:
        game.stop()
      if event.type == pygame.KEYDOWN:
        game.stop()
  pygame.quit()

if __name__ == "__main__":
    main()



