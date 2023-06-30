import numpy as np
from qiskit import Aer
from qiskit import QuantumCircuit, transpile
import time
import timeout_decorator

def balanced(n):
    oracle_circuit = QuantumCircuit(n+1)
    b_str = format(np.random.randint(1,2**n), '0'+str(n)+'b')
    [oracle_circuit.x(qubit) for qubit in range(len(b_str)) if b_str[qubit] == '1']
    [oracle_circuit.cx(qubit, n) for qubit in range(n)]
    [oracle_circuit.x(qubit) for qubit in range(len(b_str)) if b_str[qubit] == '1']
    return oracle_circuit

def constant(n):
    oracle_circuit = QuantumCircuit(n+1)
    if np.random.randint(2) == 1:
        oracle_circuit.x(n)
    return oracle_circuit

def deutsch_josza(oracle_type, n):
    circuit = QuantumCircuit(n+1, n)
    circuit.x(n)
    circuit.h(n)
    [circuit.h(qubit) for qubit in range(n)]
    circuit.append(balanced(n) if oracle_type=="balanced" else constant(n), range(n + 1))
    [circuit.h(qubit) for qubit in range(n)]
    [circuit.measure(i, i) for i in range(n)]
    return circuit

@timeout_decorator.timeout(7200)
def calculate_time(circuit, simulator):
        start = time.time()
        transpiled_circuit = transpile(circuit, simulator)
        simulator.run(transpiled_circuit).result().get_counts()
        end = time.time()
        return end - start

sum_times = [0] * 30
for i in range(5):
    times = []
    for n in range(1, 31):
        circuit = deutsch_josza("balanced", n)
        simulator = Aer.get_backend('aer_simulator_statevector')
        # simulator = Aer.get_backend('aer_simulator_matrix_product_state')
        # simulator = Aer.get_backend('aer_simulator_stabilizer')
        print(f"for {n + 1} qubits:")
        try:
            elapsed_time = calculate_time(circuit, simulator)
            times.append(elapsed_time)
            print(f"took {elapsed_time}s")
        except Exception as e:
            print(str(e))
    for j in range(30):
        sum_times[j] += times[j]
avg_times = [t / 5 for t in sum_times]
print(avg_times)