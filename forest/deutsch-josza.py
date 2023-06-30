import numpy as np
from pyquil import Program, get_qc
from pyquil.gates import H, X, CNOT, MEASURE
import random
import time
import timeout_decorator

def balanced(n, qubits):
    p = Program()
    b_str = format(np.random.randint(1,2**n), '0'+str(n)+'b')

    [p.inst(X(qubits[i])) for i in range(n) if b_str[qubits[i]] == '1']
    [p.inst(CNOT(qubits[i], qubits[n])) for i in range(n)]
    [p.inst(X(qubits[i])) for i in range(n) if b_str[qubits[i]] == '1']

    return p

def constant(n, qubits):
    p = Program()
    if random.randint(0, 1) == 1:
        p.inst(X(qubits[n]))
    return p

def deutsch_josza(oracle_type, n, qc):
    p = Program()
    qubits = qc.qubits()

    p += X(qubits[n])
    p += H(qubits[n])
    [p.inst(H(qubits[i])) for i in range(n)]
    p += balanced(n, qubits) if oracle_type == "balanced" else constant(n, qubits)
    [p.inst(H(qubits[i])) for i in range(n)]

    ro = p.declare("ro", "BIT", n)
    [p.inst(MEASURE(qubits[i], ro[i])) for i in range(n)]

    return p

@timeout_decorator.timeout(7200)
def calculate_time(qc, circuit):
    start = time.time()
    res = qc.run(circuit)
    end = time.time()
    return end - start, np.sum(res.readout_data['ro'])

sum_times = [0] * 30
for i in range(5):
    times = []
    for n in range(1, 31):
        print(f"for {n + 1} qubits:")
        try:
            qc = get_qc(f"{n+1}q-qvm")
            circuit = deutsch_josza("balanced", n, qc)
            elapsed_time = calculate_time(qc, circuit)
            times.append(elapsed_time)
            print(f"took {elapsed_time}s")
        except Exception as e:
            print(str(e))
    for j in range(30):
        sum_times[j] += times[j]
avg_times = [t / 5 for t in sum_times]
print(avg_times)

