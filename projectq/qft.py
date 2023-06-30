from projectq import MainEngine
from projectq.ops import H, C, Ph, Swap
from math import pi

def qft(eng, n):
    qubits = eng.allocate_qureg(n)
    for j in range(n - 1, -1, -1):
        H | qubits[j]
        for i in range(j):
            C(Ph(pi/2 ** (j - i))) | (qubits[i], qubits[j])
    for i in range(n//2):
        Swap | (qubits[i], qubits[n - i - 1])
    
    eng.flush()

eng = MainEngine()
qft(eng, 4)
fig, axes = eng.backend.draw()