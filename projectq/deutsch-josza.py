from projectq import MainEngine
from projectq.ops import All, H, Measure, X, CNOT
from projectq.meta import Compute, Uncompute
import numpy as np
import time
import timeout_decorator

def balanced(qubits, output, n):
    b_str = format(np.random.randint(1,2**n), '0'+str(n)+'b')

    with Compute(eng):
        [X | qubit for i, qubit in enumerate(qubits) if b_str[i] == '1']
    [CNOT | (qubit, output) for qubit in qubits]
    Uncompute(eng)

def constant(output):
    if np.random.randint(2) == 1:
        X | output

def deutsch_josza(eng, n, oracle_type):
    x = eng.allocate_qureg(n)
    with Compute(eng):
        All(H) | x

    oracle_out = eng.allocate_qubit()
    X | oracle_out
    H | oracle_out

    balanced(x, oracle_out, n) if oracle_type == "balanced" else constant(oracle_out)

    Uncompute(eng)
    All(Measure) | x
    Measure | oracle_out
    eng.flush()
    return [int(qubit) for qubit in x]

@timeout_decorator.timeout(7200)
def calculate_time(eng, n):
        start = time.time()
        result = deutsch_josza(eng, n, "balanced")
        end = time.time()
        return end - start, result

sum_times = [0] * 30
for i in range(5):
    times = []
    for n in range(1, 31):
        eng = MainEngine()
        print(f"for {n + 1} qubits:")
        try:
            elapsed_time, result = calculate_time(eng, n)
            times.append(elapsed_time)
            print(f"took {elapsed_time}s")
        except Exception as e:
            print(str(e))
            break
    for j in range(30):
        sum_times[j] += times[j]
avg_times = [t / 5 for t in sum_times]
print(avg_times)