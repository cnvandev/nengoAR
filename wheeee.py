# Create the model object
import nengo
import libardrone

# Quad position input.
def position_input(t):
    if t < 1:
        return [0, 0, 1]
    elif t < 2:
        return [0, 1, 0]
    else:
        return [1, 0, 0]

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
    A_data = sim.data(A_probe)
    print A_data[-1]
