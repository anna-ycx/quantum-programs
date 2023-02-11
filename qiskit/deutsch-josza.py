from enum import Enum
import numpy as np
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, assemble, transpile
from qiskit.visualization import plot_histogram

OracleType = Enum('Oracle', ['CONSTANT', 'BALANCED'])

def oracle(type, n):
    oracle_circuit = QuantumCircuit(n+1)
    
    if type == OracleType.BALANCED:
        b_str = format(np.random.randint(1,2**n), '0'+str(n)+'b') # binary string of length n

        # if digit is 1, place X-gate on corresponding qubit
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_circuit.x(qubit)
        
        # perform a CNOT for each qubit in first register, with target as qubit in second register
        for qubit in range(n):
            oracle_circuit.cx(qubit, n)

        # place final X-gates
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_circuit.x(qubit)

    elif type == OracleType.CONSTANT:
        if np.random.randint(2) == 1:
            oracle_circuit.x(n)
    
    oracle_gate = oracle_circuit.to_gate()
    oracle_gate.name = "Oracle" 
    return oracle_gate

def deutsch_josza(oracle, n):
    circuit = QuantumCircuit(n+1, n)

    # initialisation 
    circuit.x(n)
    circuit.h(n)
    [circuit.h(qubit) for qubit in range(n)]
        
    circuit.append(oracle, range(n+1))
    [circuit.h(qubit) for qubit in range(n)]
    [circuit.measure(i, i) for i in range(n)]
    
    return circuit

n = 6
circuit = deutsch_josza(oracle(OracleType.BALANCED, n), n)
circuit.draw(output='text')
# circuit.draw(output='mpl').savefig("circuit.png")

aer_sim = Aer.get_backend('aer_simulator')
transpiled_circuit = transpile(circuit, aer_sim)
res = aer_sim.run(assemble(transpiled_circuit)).result().get_counts()
# print(res)
# hist = plot_histogram(res)
# hist.savefig(f"deutsch_josza_with_{n}_qubits.png")