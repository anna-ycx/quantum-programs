import cirq
from cirq import H, measure, CNOT, CZ, Moment

def shors():
    circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(5) 
    for i in range(3):  
        circuit.append(H(qubits[i]))
    circuit.append(CNOT(qubits[2], qubits[3]))
    circuit.append(CNOT(qubits[2], qubits[4]))
    circuit.append(Moment(H(qubits[1])))
    circuit.append((CZ ** (1 / 2))(qubits[1], qubits[0]))
    circuit.append(H(qubits[0]))
    circuit.append(Moment((CZ ** (1 / 4))(qubits[1], qubits[2])))
    circuit.append((CZ ** (1 / 2))(qubits[0], qubits[2]))
    for i in range(3):  
        circuit.append(measure(qubits[i]))
    return circuit