from pyquil import Program, get_qc
from pyquil.gates import H, PHASE, SWAP
from math import pi

def qft(n, qc):
    p = Program()
    qubits = qc.qubits()
    for j in range(n - 1, -1, -1):
        p.inst(H(qubits[j]))
        for i in range(j):
            p.inst(PHASE(pi/2**(j - i), qubits[i]).controlled(j))    
    for i in range(n//2):
        p.inst(SWAP(qubits[i], qubits[n - i - 1]))
    return p

n = 4
qc = get_qc(f"{n}q-qvm")
qc.run(circuit = qft(n, qc))