import numpy as np
from qiskit import Aer, transpile
from qiskit import QuantumCircuit
import random
import time
import timeout_decorator

def grover(xprime):
    qubits = [qubit for qubit in range(n)]
    grover_circuit = QuantumCircuit(n, n)
    oracle = make_oracle(xprime)
    diff = diffuser(n)
    [grover_circuit.h(qubit) for qubit in qubits]
        
    for _ in range(int(np.floor(np.pi / 4 * np.sqrt(2 ** n)))):
        grover_circuit.append(oracle, qubits)
        grover_circuit.append(diff, qubits)

    grover_circuit.measure(qubits, qubits[::-1])
    return grover_circuit

def make_oracle(xprime):
    n = len(xprime)
    oracle_circuit = QuantumCircuit(n)
    [oracle_circuit.x(qubit) for qubit, x in enumerate(xprime) if not x]
    oracle_circuit.mcp(np.pi, list(range(n-1)), n-1)
    [oracle_circuit.x(qubit) for qubit, x in enumerate(xprime) if not x]
    return oracle_circuit

def diffuser(n):
    circuit = QuantumCircuit(n)
    [circuit.h(qubit) for qubit in range(n)]
    [circuit.x(qubit) for qubit in range(n)]
    circuit.mcp(np.pi, list(range(n-1)), n-1)
    [circuit.x(qubit) for qubit in range(n)]
    [circuit.h(qubit) for qubit in range(n)]
    return circuit

@timeout_decorator.timeout(7200)
def calculate_time(circuit, simulator):
        start = time.time()
        transpiled_circuit = transpile(circuit, simulator)
        result = simulator.run(transpiled_circuit).result().get_counts()
        end = time.time()
        return end - start, result

sum_times = [0] * 30
for i in range(5):
    times = []
    for n in range(2, 32):
        no_iterations = int(np.floor(np.pi / 4 * np.sqrt(2 ** n)))
        xprime = [random.randint(0, 1) for _ in range(n)]
        grover_circuit = grover(xprime)
        simulator = Aer.get_backend('aer_simulator_statevector')
        print(f"for {n} qubits:")
        xprime = ''.join([str(x) for x in xprime])
        try:
            elapsed_time, result = calculate_time(grover_circuit, simulator)
            times.append(elapsed_time)
            print(f"took {elapsed_time}s, with x'={xprime} and {no_iterations} iterations, found={max(result, key=result.get) == xprime}")
        except Exception as e:
            print(str(e))
            break
    for j in range(30):
        sum_times[j] += times[j]
avg_times = [t / 5 for t in sum_times]
print(avg_times)