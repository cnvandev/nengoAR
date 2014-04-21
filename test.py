import libardrone
import time

# Connect to the quad and take off.
drone = libardrone.ARDrone()
drone.reset()

drone.manual(250, 250, 250, 250)
time.sleep(3)

drone.manual(0, 0, 0, 0)
drone.halt()
