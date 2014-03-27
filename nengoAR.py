# Create the model object
import nengo
import libardrone
import numpy

path = numpy.genfromtxt('path.csv', delimiter=',')

# Connect to the quad and take off.
# drone = libardrone.ARDrone()
# drone.takeoff()

# Quad position input.
def path_input(time, x):
    for index, point in enumerate(path):
        if time >= min(path[index - 1][3], 0) and time < point[3]:
            return point[:-1]

    # If we're at the end, stay at the last point.
    return path[-1][:-1]

def drone_state(time):
    # state = drone.nav_data[0]
    state = {
       'phi': -174,
       'psi': -55,
       'num_frames': 2875,
       'battery': 95,
       'altitude': 645,
       'ctrl_state': 0,
       'vx': 0.0,
       'vy': 0.0,
       'vz': 0.0,
       'theta': 11
    }
    return numpy.array([state['psi'], state['phi'], state['theta'], state['altitude'], state['vx'], state['vy'], state['vz']])

def send_motors(time, motor_values):
    print "Sending", motor_values
    #drone.at_pwm(seq, motor_values[0], motor_values[1], motor_values[2], motor_values[3])
    return motor_values

# Build our neural model.
model = nengo.Model('Quad Test')

# Create input nodes representing the input and store it in an ensemble.
path_input = nengo.Node(output=path_input, size_in=3)
state_input = nengo.Node(output=drone_state, size_out=7)
motor_output = nengo.Node(send_motors, size_in=4)

desired_position = nengo.Ensemble(neurons=100, dimensions=3)
current_state = nengo.Ensemble(neurons=500, dimensions=7)
motor_controls = nengo.Ensemble(neurons=300, dimensions=4)

nengo.Connection(path_input, desired_position)
nengo.Connection(state_input, current_state)
nengo.Connection(motor_controls, motor_output)

# Create our simulator
sim = nengo.Simulator(model)
sim.run(10)

drone.land()
drone.halt()
