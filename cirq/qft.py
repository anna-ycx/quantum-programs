import cirq
from cirq import H, SWAP, CZ

def qft(n):
    circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(n)
    for j in range(n - 1, -1, -1):
        circuit.append((H(qubits[j])))
        for i in range(j):
            circuit.append((CZ ** (1 / 2 ** (j - i)))(qubits[i], qubits[j]))
    for i in range(n//2):
        circuit.append(SWAP(qubits[i], qubits[n - i - 1]))
    return circuit