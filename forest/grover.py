from pyquil import Program, get_qc
from pyquil.gates import H, X, Z, MEASURE
import numpy as np
import time
import timeout_decorator
import random

def grover(n, target_state, qc):
    p = Program()
    qubits = qc.qubits()

    [p.inst(H(qubits[i])) for i in range(n)]

    oracle = make_oracle(qubits, n, target_state)
    diff = diffuser(qubits, n)

    for _ in range(int(np.floor(np.pi / 4 * np.sqrt(2**n)))):
        p += oracle
        p += diff

    ro = p.declare('ro', 'BIT', n)
    [p.inst(MEASURE(qubits[i], ro[i])) for i in range(n)]
    
    return p

def make_oracle(qubits, n, target_state):
    p = Program()
    p.inst(X(qubits[i]) for i in range(n) if target_state[i] == '0')
    p.inst(Z(qubits[-1]).controlled([i for i in qubits[:-1]]))
    p.inst(X(qubits[i]) for i in range(n) if target_state[i] == '0')
    return p

def diffuser(qubits, n):
    p = Program()
    [p.inst(H(qubits[i])) for i in range(n)]
    [p.inst(X(qubits[i])) for i in range(n)]
    p.inst(Z(qubits[-1]).controlled([i for i in qubits[:-1]]))
    [p.inst(X(qubits[i])) for i in range(n)]
    [p.inst(H(qubits[i])) for i in range(n)]
    return p

@timeout_decorator.timeout(7200)
def calculate_time(qc, circuit):
        start = time.time()
        res = qc.run(circuit).readout_data['ro'][0]
        end = time.time()
        return end - start, res

sum_times = [0] * 30
for i in range(5):
    times = []
    for n in range(2, 32):
        print(f"for {n} qubits:")
        try:
            xprime = [random.randint(0, 1) for _ in range(n)]
            qc =  get_qc(f"{n}q-qvm")
            circuit = grover(n, xprime, qc)
            elapsed_time, res = calculate_time(qc, circuit)
            times.append(elapsed_time)
            print(f"took {elapsed_time}s, with x'={xprime}")
        except Exception as e:
            print(str(e))
    for j in range(30):
        sum_times[j] += times[j]
avg_times = [t / 5 for t in sum_times]
print(avg_times)