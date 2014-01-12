#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

def main():

  print 'leap test'
  # Create a sample listener and controller
  listener = SampleListener()
  controller = Leap.Controller()

  # Have the sample listener receive events from the controller
  controller.add_listener(listener)

  # Keep this process running until Enter is pressed
  print "Press Enter to quit..."
  sys.stdin.readline()

  # Remove the sample listener when done
  controller.remove_listener(listener)

if __name__ == '__main__':
  main()
