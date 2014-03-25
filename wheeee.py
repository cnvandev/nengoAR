# Create the model object
import nengo
model = nengo.Model('Addition')

# Create 3 ensembles each containing 100 leaky integrate-and-fire neurons
A = nengo.Ensemble(nengo.LIF(100), dimensions=1)
B = nengo.Ensemble(nengo.LIF(100), dimensions=1)
C = nengo.Ensemble(nengo.LIF(100), dimensions=1)

# Create input nodes representing constant values
input_a = nengo.Node(output=0.5)
input_b = nengo.Node(output=0.3)

# Connect the input nodes to the appropriate ensembles
nengo.Connection(input_a, A)
nengo.Connection(input_b, B)

# Connect input ensembles A and B to output ensemble C
nengo.Connection(A, C)
nengo.Connection(B, C)

# Set up probes for the output data we'll want to look at.
input_a_probe = nengo.Probe(input_a, 'output')
input_b_probe = nengo.Probe(input_b, 'output')
A_probe = nengo.Probe(A, 'decoded_output', filter=0.01)
B_probe = nengo.Probe(B, 'decoded_output', filter=0.01)
C_probe = nengo.Probe(C, 'decoded_output', filter=0.01)

# Create the simulator
sim = nengo.Simulator(model)
# Run it for 5 seconds
sim.run(5)

import matplotlib.pyplot as plt

# Plot the input signals and decoded ensemble values
t = sim.trange()
plt.plot(sim.trange(), sim.data(A_probe), label="Decoded Ensemble A")
plt.plot(sim.trange(), sim.data(B_probe), label="Decoded Ensemble B")
plt.plot(sim.trange(), sim.data(C_probe), label="Decoded Ensemble C")
plt.plot(sim.trange(), sim.data(input_a_probe), label="Input A", color='k', linewidth=2.0)
plt.plot(sim.trange(), sim.data(input_b_probe), label="Input B", color='0.75', linewidth=2.0)
plt.legend()
plt.ylim(0, 1)
plt.show()
