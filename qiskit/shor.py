from qiskit import QuantumCircuit, Aer, execute
from numpy import pi

def shor():
    circuit = QuantumCircuit(5, 5)
    for i in range(3):
        circuit.h(i)
    circuit.cnot(2,3)
    circuit.cnot(2,4)
    circuit.h(1)
    circuit.cp(pi / 2, 1, 0)
    circuit.h(0)
    circuit.cp(pi / 4, 1, 2)
    circuit.cp(pi / 4, 0, 2)
    for i in range(3):
        circuit.measure(i, i)
    return circuit

circuit = shor()
simulator = Aer.get_backend('qasm_simulator')
counts = execute(circuit, backend=simulator, shots=1000).result().get_counts(circuit)
print(counts)