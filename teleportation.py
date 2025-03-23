# A quantum circuit for demonstrating the protocol for one qubit teleportation in Cirq.
import cirq

msg = cirq.NamedQubit("Message")
a = cirq.NamedQubit("Alice")
b = cirq.NamedQubit("Bob")


def teleportation(gate):
    circuit = cirq.Circuit()
    # We first write a circuit that prepares the input state after specifying a gate to prepare the message qubit.
    circuit.append(gate(msg))
    # The operation that creates a Bell state between Alice and Bob.
    circuit.append([cirq.H(a), cirq.CNOT(a, b)])
    # Then come the operations that Alice does before sending classical messages to Bob.
    circuit.append([cirq.CNOT(msg, a), cirq.H(msg), cirq.measure(msg, a)])
    # Then finally Bob does operations according to the message he receives. This is performed by control gates with control on ALice's side.
    circuit.append([cirq.CNOT(a, b), cirq.CZ(msg, b)])


    return circuit

# msg_gate prepares the msg state by acting on the state $\ket{0}$.
msg_gate = cirq.H
circuit = teleportation(msg_gate)
simulator = cirq.Simulator()
results = simulator.simulate(circuit)
print(results)

