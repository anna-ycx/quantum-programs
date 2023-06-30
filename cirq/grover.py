import cirq
import numpy as np
from cirq import H, X
import time
import timeout_decorator
import random

def grover(xprime, no_iterations):
    qubits = cirq.LineQubit.range(n)
    grover_circuit = cirq.Circuit()
    oracle = make_oracle(xprime, n)
    diff = diffuser(n, qubits)

    [grover_circuit.append(H(q)) for q in qubits]
    for _ in range(no_iterations):
        grover_circuit.append(oracle, qubits)
        grover_circuit.append(diff, qubits)

    grover_circuit.append(cirq.measure(*qubits))
    return grover_circuit

def make_oracle(xprime, n):
    oracle_circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(n)

    [oracle_circuit.append(X(q)) for (q, bit) in zip(qubits, xprime) if not bit]
    oracle_circuit.append(cirq.ControlledGate(sub_gate=cirq.Z, num_controls=n - 1).on(*qubits))
    [oracle_circuit.append(X(q)) for (q, bit) in zip(qubits, xprime) if not bit]

    return oracle_circuit

def diffuser(n, qubits):
    circuit = cirq.Circuit()
    circuit.append(H.on_each(*qubits))
    circuit.append(X.on_each(*qubits))
    circuit.append(cirq.ControlledGate(sub_gate=cirq.Z, num_controls=n - 1).on(*qubits))
    circuit.append(X.on_each(*qubits))
    circuit.append(H.on_each(*qubits))
    return circuit

@timeout_decorator.timeout(7200)
def calculate_time(circuit, simulator):
        start = time.time()
        result = simulator.run(circuit)
        end = time.time()
        return end - start, result

def flatten(list):
    return [item for sublist in list for item in sublist]

sum_times = [0] * 30
for i in range(5):
    times = []
    for n in range(2, 32):
        no_iterations = int(np.floor(np.pi / 4 * np.sqrt(2 ** n)))
        xprime = [random.randint(0, 1) for _ in range(n)]
        grover_circuit = grover(xprime, no_iterations)
        simulator = cirq.Simulator()
        print(f"for {n} qubits:")
        xprime = ''.join([str(x) for x in xprime])
        try:
            elapsed_time, results = calculate_time(grover_circuit, simulator)
            results = ''.join([str(x) for x in flatten(flatten(results.measurements.values()))])
            times.append(elapsed_time)
            print(f"took {elapsed_time}s, with x'={xprime} and {no_iterations} iterations, found={results == xprime}")
        except Exception as e:
            print(str(e))
            break
    for j in range(30):
        sum_times[j] += times[j]
avg_times = [t / 5 for t in sum_times]
print(avg_times)


