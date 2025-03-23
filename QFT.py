import cirq
import numpy as np

# Due to the fact that QFT (quantum fourier transform) has a recursive formulation, it is possible to write down a circuit that performs the transform even for a large number of qubits.

def n_qubit_initialise(n):
    """We use this function to initialise n qubits on which we can perform a generalised QFT."""
    qubits = cirq.LineQubit.range(n)
    return qubits

# For example, let us perform a 10-qubit QFT by initialising using the function
qubits = n_qubit_initialise(10)
circuit_qft = cirq.Circuit()


"""Defining a custom controlled gate used in QFT which applies CZPow(d) : control-Z^(1/2^d) when the distance between qubits is d. On adjacent qubits, CZpow(1) and so on."""
class CZpow(cirq.Gate):
    def __init__(self, d):
        self.d = d

    def _num_qubits_(self):
        return 2

    def _unitary_(self):
        return np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, (0.j)**(1/(2**self.d - 1))],
            ]
        )

    def _circuit_diagram_info_(self, args):
        return '@', f'CZ({self.d})'




def qft_moments(n):
    ops_1 = []
    ops_2 = []
    for i in range(n):
        ops_1 = [cirq.H(qubits[n-1-i])]
        ops_2 = [CZpow(j)(qubits[n-1-i-j],qubits[n-1-i]) for j in np.arange(1,n-i)]
        circuit_qft.append([ops_1,ops_2], strategy = cirq.InsertStrategy.NEW)

qft_moments(10)
print(circuit_qft)


simulator = cirq.Simulator()
results = simulator.simulate(circuit_qft, qubit_order = qubits)
print(results.dirac_notation())
qft_output = results.state_vector()
qft_output = qft_output.astype(float)

# Applying inverse to the output of QFT should give back the original all 0 state. We can construct the inverse in the same way as the QFT circuit but with negative powers. Here, we just use the inverse qft operation available in Cirq.
circuit_iqft = cirq.Circuit()
circuit_iqft.append(cirq.qft(*qubits, without_reverse=True, inverse=True))
print(circuit_iqft)
sim2 = cirq.Simulator()
results2 = sim2.simulate(circuit_iqft, qubit_order = qubits, initial_state = qft_output)
print(results2.dirac_notation())

# Inverse Fourier Transformation.
# To go from the QFT to the inverse QFT, we just need to use negative powers in the control operations.
#n_qubit_initialise(10)
#circuit_iqft = cirq.Circuit()
#def iqft_moments(n):
#    ops_1 = []
#    ops_2 = []
#    for i in range(n):
#        ops_1 = [cirq.H(qubits[n-1-i])]
#        ops_2 = [CZpow(-j)(qubits[n-1-i-j],qubits[n-1-i]) for j in np.arange(1,n-i)]
#        circuit_iqft.append([ops_1,ops_2], strategy = cirq.InsertStrategy.NEW)

#iqft_moments(10)
#sim2 = cirq.Simulator()
#results2 = sim2.simulate(circuit_iqft, qubit_order = qubits, initial_state = qft_output)
#print(results2.dirac_notation())