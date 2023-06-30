import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from pathlib import Path

class Algorithm(Enum):
    deutsch_josza = ['the Deutsch-Josza algorithm', 'deutsch_josza']
    grover = ['Grover\'s algorithm', 'grover']
    qft = ['the quantum Fourier transform', 'qft']
    shor = ['Shor\'s algorithm', 'shor']

language_colour_map = {'qiskit': 'tab:blue', 'q#': 'tab:orange', 'cirq': 'tab:green', 'silq': 'tab:red', 'projectQ': 'tab:purple', 'forest': 'tab:brown'}
line_style = {'qiskit': '-', 'q#': '--', 'cirq': '-.', 'silq': '-', 'projectQ': '--', 'forest': '--'}

def get_data_for_language(language, algorithm, results_folder=Path("results/data_linux/"), simulator=None, cloud=False):
    counter = 0
    no_qubits, time_taken = [], []

    if cloud:
        filename = f"{language}_{algorithm.value[1]}_cloud"
    elif simulator:
        filename = f"{language}_{algorithm.value[1]}_{simulator}"
    else:
        filename = f"{language}_{algorithm.value[1]}"

    with open(results_folder / f"{filename}.txt") as f:
        for line in f:
            counter += 1
            if line[0] != '#':
                if counter % 2 == 0:
                    time_taken.append(float(line.split(' ')[1][:-2]))
                else:
                    no_qubits.append(line.split(' ')[1])
    return no_qubits, time_taken

def gen_sim_graph(algorithm):
    data = []
    for language in language_colour_map.keys():
        no_qubits, time_taken = get_data_for_language(language, algorithm)
        data.append((language, no_qubits, time_taken))

    plt.title(f"Time taken against the number of qubits for simulators to run {algorithm.value[0]}")
    plt.xlabel("Number of qubits")
    plt.ylabel("Time taken, s")

    for lang, no_qubits, time_taken in data:
        print(lang)
        plt.plot(no_qubits, time_taken, line_style[lang], label=f"{lang[0].upper() + lang[1:] if lang != 'forest' else 'PyQuil'}", color=language_colour_map[lang])

    plt.legend(loc="upper left")
    plt.xticks(np.arange(0, 28, step=2))
    ax = plt.gca()
    ax.set_ylim([0, 800])

    plt.savefig(f'sim_{algorithm.value[1]}.png', bbox_inches='tight')


def gen_cloud_graph(algorithm):
    data = []
    for language in ['qiskit', 'q#', 'cirq']:
        no_qubits, time_taken = get_data_for_language(language, algorithm, cloud=True)
        data.append((language, no_qubits, time_taken))

    plt.title(f"Time taken against the number of qubits for simulators to run {algorithm.value[0]} on the cloud", wrap=True)
    plt.xlabel("Number of qubits")
    plt.ylabel("Time taken, s")

    for lang, no_qubits, time_taken in data:
        plt.plot(no_qubits, time_taken, line_style[lang], label=f"{lang[0].upper() + lang[1:]}", color=language_colour_map[lang])

    plt.legend(loc="upper left")
    plt.xticks(np.arange(0, 28, step=2))
    ax = plt.gca()
    ax.set_ylim([0, 600])

    plt.savefig(f'sim_{algorithm.value[1]}_cloud.png', bbox_inches='tight')

def gen_qiskit_sim_graph(algorithm):
    data = []
    for sim in ['statevector', 'mps', 'stabilizer']:
        no_qubits, time_taken = get_data_for_language('qiskit', algorithm, results_folder=Path("results/data_mac/"), simulator=sim)
        data.append((sim, no_qubits, time_taken))
        # data.append((sim, no_qubits, time_taken))

    plt.title(f"Time taken against the number of qubits for various Qiskit simulators to run {algorithm.value[0]}", wrap=True)
    plt.xlabel("Number of qubits")
    plt.ylabel("Time taken, s")

    for sim, no_qubits, time_taken in data:
        if sim == 'mps':
            plt.plot(no_qubits, time_taken, '--', label=f"MPS")
        else:
            plt.plot(no_qubits, time_taken, label=f"{sim[0].upper() + sim[1:]}")
    # plt.axis('scaled')
    plt.legend(loc="upper left")
    plt.xticks(np.arange(0, 800, step=100)) #np.arange(0, 800, step=100)
    ax = plt.gca()
    ax.set_ylim([0, 2500])

    plt.savefig(f'sim_{algorithm.value[1]}_qiskit.png', bbox_inches='tight')

def gen_line_count_graph(algorithm):
    if algorithm == Algorithm.deutsch_josza:
        # added 1 to silq's line count to account for the fact that random numbers cannot be generated in silq so an oracle bitstring was not created
        line_counts = {'qiskit': 21, 'q#': 42, 'cirq': 22, 'silq': 19, 'projectQ': 22, 'forest': 23}
    elif algorithm == Algorithm.grover:
        line_counts = {'qiskit': 26, 'q#': 28, 'cirq': 27, 'silq': 21, 'projectQ': 26, 'forest': 26}
    elif algorithm == Algorithm.qft:
        line_counts = {'qiskit': 9, 'q#': 12, 'cirq': 10, 'silq': 12, 'projectQ': 9, 'forest': 9}
    elif algorithm == Algorithm.shor:
        line_counts = {'qiskit': 13, 'q#': 18, 'cirq': 14, 'silq': 15, 'projectQ': 14, 'forest': 15}

    plt.rcdefaults()
    _, ax = plt.subplots()
    y_pos = np.arange(len(language_colour_map))
    ax.barh(y_pos, [line_counts[lang] for lang in language_colour_map.keys()], align='center', color=language_colour_map.values())
    ax.set_yticks(y_pos, labels=[lang[0].upper() + lang[1:] if lang != 'forest' else 'PyQuil' for lang in language_colour_map.keys()])
    ax.invert_yaxis()
    ax.set_xlabel('Line count')
    if algorithm == Algorithm.shor:
        ax.set_title(f'Line count for {algorithm.value[0]} with N=15, b=11')
    else:
        ax.set_title(f'Line count for {algorithm.value[0]}')

    plt.savefig(f'{algorithm.value[1]}_line_count.png', bbox_inches='tight')

def gen_gate_count_data(algorithm, graph=True):
    # exclude measurements
    if algorithm == Algorithm.deutsch_josza:
        # no_ones: the number of 1s in the oracle bitstring (i.e. whether the oracle is balanced or constant)
        gate_counts = {'qiskit': (lambda n, no_ones: 2 + 3 * n + 2 * no_ones), 'q#': (lambda n, no_ones: 2 + 2 * n + no_ones), 'cirq': (lambda n, no_ones: 2 + 3 * n + 2 * no_ones), 'silq': (lambda n, no_ones: 2 + 2 * n + no_ones), 'projectQ': (lambda n, no_ones: 2 + 2 * n + no_ones), 'forest': (lambda n, no_ones: 2 + 3 * n + 2 * no_ones)}
    elif algorithm == Algorithm.grover:
        # no_ones: the number of 1s in the value we are searching for
        gate_counts = {'qiskit': (lambda n, no_ones, no_its: n + no_its * (6 * n + 2 * no_ones)), 'q#': (lambda n, no_ones, no_its: n + no_its * (2 + 2 * n + no_ones)), 'cirq': (lambda n, no_ones, no_its: n + no_its * (6 * n + 2 * no_ones)), 'silq': (lambda n, no_ones, no_its: n + no_its * (2 + 2 * n + no_ones)), 'projectQ': (lambda n, no_ones, no_its: n + no_its * (2 + 2 * n + no_ones)), 'forest': (lambda n, no_ones, no_its: n + no_its * (6 * n + 2 * no_ones))}
    elif algorithm == Algorithm.qft:
        gate_counts = lambda n: n + n * (n-1) / 2

    ns = range(2, 11)

    no_ones_dj = lambda n: 2**(n-1) # oracle is balanced
    no_ones_grover = lambda n: int(n/2) # take half of the values in the bitstring we are searching for to be equal to 1
    no_its_grover = lambda n: int(np.floor(np.pi / 4 * np.sqrt(2 ** n)))

    if graph:
        for lang in language_colour_map.keys():
            label = lang[0].upper() + lang[1:] if lang != 'forest' else 'PyQuil'
            if algorithm == Algorithm.deutsch_josza:
                plt.plot(ns, [gate_counts[lang](n, no_ones_dj(n)) for n in ns], line_style[lang], label=label)
            elif algorithm == Algorithm.grover:
                plt.plot(ns, [gate_counts[lang](n, no_ones_grover(n), no_its_grover(n)) for n in ns], line_style[lang], label=label)
            elif algorithm == Algorithm.qft:
                plt.plot(ns, [gate_counts(n) for n in ns], line_style[lang], label=label)
                
        plt.legend(loc="upper left")
        plt.xticks(ns)
        plt.xlabel("Number of qubits")
        plt.ylabel("Number of low-level gates")
        plt.title(f"Number of low-level gates for {algorithm.value[0]}")
        plt.savefig(f'{algorithm.value[1]}_gate_count.png', bbox_inches='tight')
    else:
        latex_table = ""
        for n in ns:
            latex_table += f"{n} "
            for lang in language_colour_map.keys():
                if algorithm == Algorithm.deutsch_josza:
                    latex_table += f"& {gate_counts[lang](n, no_ones_dj(n))} "
                elif algorithm == Algorithm.grover:
                    latex_table += f"& {gate_counts[lang](n, no_ones_grover(n), no_its_grover(n))} "
            latex_table += "\\\\ \n"
        print(latex_table)

gen_sim_graph(Algorithm.deutsch_josza)