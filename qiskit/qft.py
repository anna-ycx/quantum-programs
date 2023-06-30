from qiskit import QuantumCircuit, transpile
from qiskit import Aer
from math import pi

def qft(n):
    circuit = QuantumCircuit(n)
    for j in range(n - 1, -1, -1):
        circuit.h(j)
        for qubit in range(j):
            circuit.cp(pi/2**(j - qubit), qubit, j)
    for qubit in range(n//2):
        circuit.swap(qubit, n - qubit - 1)
    return circuit

n = 4
simulator = Aer.get_backend('aer_simulator_statevector')
transpiled_circuit = transpile(qft(n), simulator)
simulator.run(transpiled_circuit)