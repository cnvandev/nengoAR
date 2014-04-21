import nengo
import libardrone
import numpy
import csv
import time

# This scales the velocity proportionally to the error.
# Remember, velocity saturates at 0 and 500.
VELOCITY_SCALING = 0.05

# This scales the x- and y- turning velocity independently from the lift
# velocity. We don't care too much about lift and drop speed, but if it turns
# too fast in one direction, it gets more unstable.
TURN_SCALING = 0.001

# A filter for the output signal values.
FILTER = 0.2

MAX_SPEED = 500; # Constant defined from the quadcopter itself.

desiredfile = open('desired.csv', 'wb')
desiredwriter = csv.writer(desiredfile)

currentfile = open('current.csv', 'wb')
currentwriter = csv.writer(currentfile)

trajectoryfile = open('trajectory.csv', 'wb')
trajectorywriter = csv.writer(trajectoryfile)

enginesfile = open('engines.csv', 'wb')
engineswriter = csv.writer(enginesfile)

path = numpy.genfromtxt('path.csv', delimiter=',')

SIMULATE = False

if not SIMULATE:
    # Connect to the quad and take off.
    drone = libardrone.ARDrone()
    drone.reset()

# Quad position input.
def path_input(time, x):
    for index, point in enumerate(path):
        if len(path) > 1 and time >= min(path[index - 1][3], 0) and time < point[3]:
            return point[:-1]

    # If we're at the end, stay at the last point.
    return path[-1][:-1]

def drone_state(time):
    if not SIMULATE and drone.navdata.keys():
        return [drone.navdata[0]['vx'], drone.navdata[0]['vy'], drone.navdata[0]['vz']]
    else:
        return [0, 0, 0]

def send_motors(time, motor_values):
    if not SIMULATE:
        drone.manual(motor_values[0], motor_values[1], motor_values[2], motor_values[3])
    engineswriter.writerow([motor_values[0], motor_values[1], motor_values[2], motor_values[3]])
    return motor_values

def power(trajectory):
    engines = numpy.array([ trajectory[2] + TURN_SCALING*trajectory[0] - TURN_SCALING*trajectory[1],
                            trajectory[2] - TURN_SCALING*trajectory[0] - TURN_SCALING*trajectory[1],
                            trajectory[2] + TURN_SCALING*trajectory[0] + TURN_SCALING*trajectory[1],
                            trajectory[2] - TURN_SCALING*trajectory[0] + TURN_SCALING*trajectory[1] ])
    engines = (engines*VELOCITY_SCALING)*MAX_SPEED + MAX_SPEED/2
    engines = numpy.clip(engines, 0, 500)
    return engines

def printdesired(time, value):
    desiredwriter.writerow(value)
    return value

def printcurrent(time, value):
    currentwriter.writerow(value)
    return value

def printtrajectory(time, value):
    trajectorywriter.writerow(value)
    return value

tau = 0.1
tau_centre = 1.0
def integrator(x):
    return tau*x - x

def difference(x):
    return numpy.subtract(x[:3], x[3:])

# Build our neural model.
model = nengo.Model('Nengo AR Brain')

# Create input nodes representing the input and store it in an ensemble.
path_input = nengo.Node(output=path_input, size_in=3)
velocity_input = nengo.Node(output=drone_state, size_out=3)
motor_output = nengo.Node(send_motors, size_in=4)

print_desired = nengo.Node(printdesired, size_in=3)
print_current = nengo.Node(printcurrent, size_in=3)
print_trajectory = nengo.Node(printtrajectory, size_in=3)

desired_position = nengo.Ensemble(neurons=100, dimensions=3, radius=10)
current_position = nengo.Ensemble(neurons=1000, dimensions=3, radius=10)
trajectory_difference_holder = nengo.Ensemble(neurons=200, dimensions=6, radius=10)
trajectory = nengo.Ensemble(neurons=300, dimensions=3, radius=10)
engine_power = nengo.Ensemble(neurons=500, dimensions=4, radius=500)

# Store the other values in neurons.
nengo.Connection(path_input, desired_position, filter=FILTER)
nengo.Connection(desired_position, print_desired, filter=FILTER)

# Integrate the velocity to get the current position.
nengo.Connection(velocity_input, current_position, filter=FILTER)
nengo.Connection(current_position, current_position, function=integrator, filter=FILTER)
nengo.Connection(current_position, print_current, filter=FILTER)

# Trajectory is the difference between the desired and current position.
nengo.Connection(desired_position, trajectory_difference_holder, transform=[[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0]], filter=FILTER)
nengo.Connection(current_position, trajectory_difference_holder, transform=[[0, 0, 0], [0, 0, 0], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]], filter=FILTER)
nengo.Connection(trajectory_difference_holder, trajectory, function=difference, filter=FILTER)
nengo.Connection(trajectory, print_trajectory, filter=FILTER)

# Now translate the desired trajectory into engine power.
nengo.Connection(trajectory, engine_power, function=power, filter=FILTER)
nengo.Connection(engine_power, motor_output, filter=FILTER)

# Create our simulator
sim = nengo.Simulator(model)
sim.run(5)

if not SIMULATE:
    drone.manual(0, 0, 0, 0)
    drone.halt()
