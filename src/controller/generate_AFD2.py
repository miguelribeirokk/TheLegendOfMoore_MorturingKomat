import random

def generate_afd(num_states, output_file):
    states = ['S' + str(i) for i in range(1, num_states + 1)]

    initial_state = 'S1'
    transitions = []

    for state in states:
        for symbol in ['0', '1']:
            if symbol == '0':
                valid_symbol = '1'
            else:
                valid_symbol = '0'
            valid_next_state = random.choice(states)

            transitions.append((state, symbol, valid_next_state))
            transitions.append((state, valid_symbol, 'INVALID'))

    with open(output_file, 'w') as file:
        # Escrever os estados
        file.write("Q: " + " ".join(states + ['INVALID']) + "\n")
        # Escrever o estado inicial
        file.write("I: " + initial_state + "\n")

        # Escrever as transições
        for transition in transitions:
            current_state, input_symbol, next_state = transition
            file.write(current_state + " -> " + next_state + " | " + input_symbol + "\n")

generate_afd(10, 'afd.txt')
