import libardrone
import time

# Connect to the quad and take off.
drone = libardrone.ARDrone()
drone.reset()

while True:
  print drone.navdata

drone.halt()
