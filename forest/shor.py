from pyquil import Program, get_qc
from pyquil.gates import H, PHASE, CNOT, MEASURE
from math import pi

def shor(qc):
    p = Program()
    qubits = qc.qubits()
    for i in range(3):
        p.inst(H(qubits[i]))
    p.inst(CNOT(qubits[2], qubits[3]))
    p.inst(CNOT(qubits[2], qubits[4]))
    p.inst(H(qubits[1]))
    p.inst(PHASE(pi / 2, qubits[0]).controlled(qubits[1]))
    p.inst(H(qubits[0]))
    p.inst(PHASE(pi / 4, qubits[2]).controlled(qubits[1]))
    p.inst(PHASE(pi / 2, qubits[2]).controlled(qubits[0]))
    ro = p.declare('ro', 'BIT', 3)
    for i in range(3):
        p.inst(MEASURE(qubits[i], ro[i]))
    return p

qc = get_qc('9q-square-qvm')
program = shor(qc)
print(qc.run(program).readout_data['ro'][0])