import cirq
import numpy as np
from cirq import H, X, CNOT, measure, Moment
import time
import timeout_decorator

def balanced(n, qubits):
    oracle_circuit = cirq.Circuit()
    b_str = format(np.random.randint(1,2**n), '0'+str(n)+'b')

    oracle_circuit.append(Moment([X(qubits[i]) for i in range(len(b_str)) if b_str[i] == '1']))
    [oracle_circuit.append(CNOT(qubits[i], qubits[n])) for i in range(n)]
    oracle_circuit.append(Moment([X(qubits[i]) for i in range(len(b_str)) if b_str[i] == '1']))

    return oracle_circuit

def constant(n, qubits):
    oracle_circuit = cirq.Circuit()  
    if np.random.randint(2) == 1:
        oracle_circuit.append(X(qubits[n])) 

def deutsch_josza(oracle_type, n):
    circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(n + 1)
    circuit.append(X(qubits[n]))
    circuit.append(H(qubits[n]))
    circuit.append(H(qubits[i]) for i in range(n))
    circuit.append(balanced(n, qubits) if oracle_type == "balanced" else constant(n, qubits))
    circuit.append(Moment(H(qubits[i]) for i in range(n)))
    circuit.append(measure(qubits[i]) for i in range(n))
    return circuit

@timeout_decorator.timeout(7200)
def calculate_time(circuit, simulator):
    start = time.time()
    simulator.run(circuit)
    end = time.time()
    return end - start

sum_times = [0] * 30
for i in range(5):
    times = []
    for n in range(1, 31):
        circuit = deutsch_josza("balanced", n)  
        simulator = cirq.Simulator()
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