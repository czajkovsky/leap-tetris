import pygame
from pygame.locals import *
from Game_Board import *
from sys import exit
import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class Move:

  def __init__(self):
    print 'New move'
    self.needs_reset = True
    self.initial = 0
    self.last_change_pos = Leap.Vector(0, 0, 0)

  def is_blocked(self):
    return self.needs_reset

  def update(self, position):
    self.last_change_pos = Leap.Vector(position)

  def reset(self):
    self.needs_reset = False
    self.update(Leap.Vector(0, 0, 0))

  def current_distance(self, x):
    return self.last_change_pos.x - x

class Listener(Leap.Listener):

  def on_init(self, controller):
    print "Leap controller initialized"
    self.game = GameEngine()
    self.current_move = Move()
    self.current_progress = 0

  def on_connect(self, controller):
    print "Leap controller connected"
    controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

  def on_disconnect(self, controller):
    print "Leap controller disconnected"

  def on_exit(self, controller):
    print "Leap controller exited"

  def on_frame(self, controller):
    frame = controller.frame()
    if not frame.hands.is_empty:
      hand = frame.hands[0]
      if -5 < hand.palm_position.x < 5 and self.current_move.is_blocked():
        print 'reset'
        self.current_move.reset()

      if not self.current_move.is_blocked():
        # print self.current_move.last_change_pos
        # print self.current_move.current_distance(hand.palm_position.x)

        if self.current_move.current_distance(hand.palm_position.x) > 20:
          print self.current_move.last_change_pos
          self.current_move.update(hand.palm_position)
          self.initial -=1
          self.game.start_move('LEFT')


        if self.current_move.current_distance(hand.palm_position.x) < -20:
          print self.current_move.last_change_pos
          self.current_move.update(hand.palm_position)
          self.initial +=1
          self.game.start_move('RIGHT')

      # for gesture in frame.gestures():
      #   if gesture.type == Leap.Gesture.TYPE_CIRCLE:
      #     circle = CircleGesture(gesture)
      #     if circle.state == Leap.Gesture.STATE_STOP:
      #       if circle.progress >= 0.8:
      #         self.game.rotate()
      #   if gesture.type == Leap.Gesture.TYPE_SWIPE:
      #     swipe = SwipeGesture(gesture)
      #     if swipe.direction.y < -0.5:
      #       self.game.start_move('DOWN')
      #       if swipe.state == Leap.Gesture.STATE_STOP:
      #         self.game.stop_move('DOWN')
      #     elif swipe.direction.x < -0.5:
      #       self.game.start_move('RIGHT')
      #       if swipe.state == Leap.Gesture.STATE_STOP:
      #         self.game.stop_move('RIGHT')
      #     elif swipe.direction.x > 0.5:
      #       self.game.start_move('LEFT')
      #       if swipe.state == Leap.Gesture.STATE_STOP:
      #         self.game.stop_move('LEFT')

    self.game.redraw()

  def state_string(self, state):
    if state == Leap.Gesture.STATE_START:
      return "STATE_START"
    if state == Leap.Gesture.STATE_UPDATE:
      return "STATE_UPDATE"
    if state == Leap.Gesture.STATE_STOP:
      return "STATE_STOP"
    if state == Leap.Gesture.STATE_INVALID:
      return "STATE_INVALID"

class GameEngine:

  def __init__(self):
    print 'Game engine initialzed'
    self.running = True
    self.board = GameBoard()
    self.board.initialize(pygame.time.get_ticks())

  def blocks(self):
    return self.board.number_of_blocks()

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
    if direction == 'LEFT':
      self.board.current_gp.move_left()
    elif direction == 'RIGHT':
      self.board.current_gp.move_right()

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

  listener = Listener()
  controller = Leap.Controller()
  controller.add_listener(listener)

  print "Press Enter to quit..."
  sys.stdin.readline()

  pygame.quit()

  controller.remove_listener(listener)

  # while game.isRunning():
  #   for event in pygame.event.get():
  #     if game.isPaused():
  #       break
  #     if event.type == pygame.QUIT:
  #       game.stop()
  #     if event.type == pygame.KEYDOWN:
  #       if event.key == pygame.K_ESCAPE:
  #         game.stop()
  #       if event.key == pygame.K_g:
  #         game.showGrid()
  #       if event.key == pygame.K_LEFT:
  #         game.start_move('LEFT')
  #       if event.key == pygame.K_RIGHT:
  #         game.start_move('RIGHT')
  #       if event.key == pygame.K_DOWN:
  #         game.start_move('DOWN')
  #       if event.key == pygame.K_UP:
  #         game.rotate()
  #     if event.type == pygame.KEYUP:
  #       if event.key == pygame.K_DOWN:
  #         game.stop_move('DOWN')
  #       if event.key == pygame.K_LEFT:
  #         game.stop_move('LEFT')
  #       if event.key == pygame.K_RIGHT:
  #         game.stop_move('RIGHT')
  #   game.redraw()
  # pygame.quit()

if __name__ == "__main__":
    main()



