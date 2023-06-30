from projectq import MainEngine
from projectq.ops import H, Measure, CNOT, Ph, C
from math import pi

def shor(eng):
    x = eng.allocate_qureg(5)
    for i in range(3):
        H | x[i]
    CNOT | (x[2], x[3])
    CNOT | (x[2], x[4])
    H | x[1]
    C(Ph(pi / 2)) | (x[1], x[0])
    H | x[0]
    C(Ph(pi / 4)) | (x[1], x[2])
    C(Ph(pi / 2)) | (x[0], x[2])
    for i in range(3):
        Measure | x[i]
        
    eng.flush()
    return [int(qubit) for qubit in x[:-2]]

eng = MainEngine()
print(shor(eng))