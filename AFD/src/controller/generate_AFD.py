import random

def generate_afd(num_states, alphabet_size, output_file):
    states = ['Q' + str(i) for i in range(1, num_states + 1)]

    initial_state = random.choice(states)
    accepting_states = random.sample(states, random.randint(1, num_states))
    transitions = []

    for state in states:
        for symbol in range(alphabet_size):
            next_state = random.choice(states)
            transitions.append((state, symbol, next_state))

    with open(output_file, 'w') as file:
        # Escrever os estados
        file.write("Estados: " + " ".join(states) + "\n")
        # Escrever o estado inicial
        file.write("Estado inicial: " + initial_state + "\n")
        # Escrever os estados de aceitação
        file.write("Estados de aceitação: " + " ".join(accepting_states) + "\n")

        # Escrever as transições
        for transition in transitions:
            current_state, input_symbol, next_state = transition
            file.write("(" + current_state + ", " + str(input_symbol) + ") -> " + next_state + "\n")
