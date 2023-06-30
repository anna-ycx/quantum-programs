from projectq import MainEngine
from projectq.meta import Compute, Control, Loop, Uncompute
from projectq.ops import All, H, Measure, X, Z
from functools import partial
import time
import timeout_decorator
import random
import numpy as np

def grover(eng, n, oracle, no_iterations):
    x = eng.allocate_qureg(n)
    All(H) | x

    oracle_out = eng.allocate_qubit()
    X | oracle_out
    H | oracle_out

    with Loop(eng, no_iterations):
        oracle(eng, x, oracle_out)

        with Compute(eng):
            All(H) | x
            All(X) | x

        with Control(eng, x[0:-1]):
            Z | x[-1]

        Uncompute(eng)

    All(Measure) | x
    Measure | oracle_out

    eng.flush()
    return [int(qubit) for qubit in x]

def make_oracle(xprime, eng, qubits, output):
    with Compute(eng):
        for i in range(len(xprime)):
            if not xprime[i]:
                X | qubits[i]
    
    with Control(eng, qubits):
        X | output

    Uncompute(eng)

@timeout_decorator.timeout(7200)
def calculate_time(oracle, eng, n, no_iterations):
        start = time.time()
        result = grover(eng, n, oracle, no_iterations)
        end = time.time()
        return end - start, result

sum_times = [0] * 30
for i in range(5):
    times = []
    for n in range(2, 32):
        eng = MainEngine()
        xprime = [random.randint(0, 1) for _ in range(n)]
        no_iterations = int(np.floor(np.pi / 4 * np.sqrt(2 ** n)))
        oracle = partial(make_oracle, xprime)

        print(f"for {n} qubits:")
        try:
            elapsed_time, result = calculate_time(oracle, eng, n, no_iterations)
            times.append(elapsed_time)
            print(f"took {elapsed_time}s, with x'={''.join([str(x) for x in xprime])} and {no_iterations} iterations, found={result == xprime}")
        except Exception as e:
            print(str(e))
            break
    for j in range(30):
        sum_times[j] += times[j]
avg_times = [t / 5 for t in sum_times]
print(avg_times)