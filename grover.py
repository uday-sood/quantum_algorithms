# Example of Grover search in Cirq.
import cirq


# Finding the item (1,1) out of a database of 4 items : (0,0), (0,1), (1,0), (1,1).
# target_search = (1,1)
# The oracle is the Toffoli gate.

q0, q1 = cirq.LineQubit.range(2)
ancilla = cirq.NamedQubit('ancilla')

oracle_11 = cirq.TOFFOLI(q0, q1, ancilla)

grover_circuit = cirq.Circuit()

def grover_algo(oracle):
    # state preparation gates
    grover_circuit.append(cirq.X(ancilla))
    grover_circuit.append([cirq.H.on_each(q0,q1,ancilla)])
    # apply the Grover operator, the first part is the oracle.
    grover_circuit.append(oracle)
    # second part is the 2*outer product of \psi's - identity operator.
    grover_circuit.append(cirq.H.on_each(q0,q1))
    grover_circuit.append([cirq.X.on_each(q1,q0)])
    grover_circuit.append(cirq.H(q1))
    grover_circuit.append(cirq.CNOT(q0,q1))
    grover_circuit.append(cirq.H(q1))
    grover_circuit.append([cirq.X.on_each(q1, q0)])
    grover_circuit.append(cirq.H.on_each(q0, q1))
    grover_circuit.append(cirq.measure(q0, q1))

grover_algo(oracle_11)
print(grover_circuit)

simulator = cirq.Simulator()
result = simulator.run(grover_circuit, repetitions=5)
print(result)