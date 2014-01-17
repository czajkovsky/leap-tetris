import pygame
from pygame.locals import *
from Game_Board import *
from sys import exit
import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class Move:

  def __init__(self):
    self.needs_reset = True
    self.pos = 0
    self.step = 20.0

  def is_blocked(self):
    return self.needs_reset

  def reset(self):
    self.pos = 0
    self.needs_reset = False

  def block(self):
    self.needs_reset = True

class HorizontalMove(Move):

  def check_position(self, x):
    new_pos = int(x / self.step)
    if new_pos > self.pos:
      self.pos = new_pos
      return 'RIGHT'
    elif new_pos < self.pos:
      self.pos = new_pos 
      return 'LEFT'

class VerticalMove(Move):
  
  def __init__(self):
    self.needs_reset = True
    self.pos = 400

  def reset(self):
    self.pos = 400
    self.needs_reset = False

  def check_position(self, y):
    new_pos = int(y)
    if new_pos+4 < self.pos:
      print str(new_pos) + '  ' + str(self.pos) 
      self.pos = new_pos
      #TODO block horizontal
      return 'DOWN'

class CircleMove(Move):

  def __init__(self):
    self.needs_reset = True
    self.count = 0
    self.in_row = 0
    self.check_rot = False

  def check_rotation(self, progress):
    if progress > 0.75:
      self.block()
      return True
    else:
      return False

class Listener(Leap.Listener):

  def on_init(self, controller):
    print "Leap controller initialized"
    self.game = GameEngine()
    self.horizontal_move = HorizontalMove()
    self.circle_move = CircleMove()
    self.vertical_move = VerticalMove()
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

      if self.circle_move.in_row > 1:
        if self.circle_move.in_progress:
          self.circle_move.reset()
          self.circle_move.check_rot = True
          self.circle_move.in_progress = False
      else:
        self.circle_move.in_progress = True

      self.circle_move.in_row += 1
      hand = frame.hands[0]

      # actions triggered when we have new block
      if self.game.new_block():
        self.horizontal_move.block()
        self.circle_move.block()
        self.vertical_move.block()

      # we're close to center, we can ublock block
      if -5 < hand.palm_position.x < 5 and self.horizontal_move.is_blocked():
        self.horizontal_move.reset()
      if -5 < hand.palm_position.x < 5 and hand.palm_position.x < 100 and self.vertical_move.is_blocked():
        self.vertical_move.reset()

      if not self.horizontal_move.is_blocked():
        self.game.move(self.horizontal_move.check_position(hand.palm_position.x))

      if not self.vertical_move.is_blocked():
        #print 'Y: ' + str(hand.palm_position.y)
        self.game.move(self.vertical_move.check_position(hand.palm_position.y))

      for gesture in frame.gestures():

        if gesture.type == Leap.Gesture.TYPE_CIRCLE:
          circle = CircleGesture(gesture)

          self.circle_move.in_row = 0

          if self.circle_move.check_rot and not self.circle_move.is_blocked():
            if self.circle_move.check_rotation(circle.progress):
              self.game.rotate()

          swept_angle = 0
          if circle.state != Leap.Gesture.STATE_START:
            previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
            swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI
    else :
      #TODO pause

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
    self.blocks = 0

  def current_block(self):
    return self.board.number_of_blocks()

  def new_block(self):
    if self.blocks < self.current_block():
      self.blocks = self.current_block()
      return True
    else:
      return False

  def stop(self):
    self.running = False

  def isRunning(self):
    return self.running

  def isPaused(self):
    return self.board.paused

  def showGrid(self):
    self.board.toggle_grid()
    self.board.update(pygame.time.get_ticks())

  def move(self, direction):
    if direction == 'LEFT':
      self.board.current_gp.move_left()
    elif direction == 'RIGHT':
      self.board.current_gp.move_right()
    elif direction == 'DOWN':
      self.board.current_gp.move_down()

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

if __name__ == "__main__":
    main()



