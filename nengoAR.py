# Create the model object
import nengo
import libardrone
from numpy import genfromtxt

path = genfromtxt('path.csv', delimiter=',')

# Quad position input.
def position_input(t):
    for index, point in enumerate(path):
        if t >= min(path[index - 1][3], 0) and t < point[3]:
            return point[:-1]

    # If we're at the end, stay at the last point.
    return path[-1][:-1]

# Connect to the quad and take off.
# drone = libardrone.ARDrone()
# drone.takeoff()

# Build our neural model.
model = nengo.Model('Quad Test')

# Create input nodes representing the input and store it in an ensemble.
input_a = nengo.Node(output=position_input)
A = nengo.Ensemble(nengo.LIF(100), dimensions=3)
nengo.Connection(input_a, A)

# Set up probes for the output data we'll want to look at.
input_a_probe = nengo.Probe(input_a, 'output')
A_probe = nengo.Probe(A, 'decoded_output', filter=0.01)

# Create the simulator
sim = nengo.Simulator(model)

while True:
    sim.step()
    position_data = sim.data(A_probe)
    print position_data[-1][0], position_data[-1][1], position_data[-1][2]
    # drone.at(drone.at_pcmd, True, position_data[-1][0], position_data[-1][1], position_data[-1][2], 0)
