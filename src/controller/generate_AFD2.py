import random


def generate_afd(num_states, limit_c, limit_a, limit_d, max_states, output_file):
    states = []

    for i in range(1, num_states + 1):
        c = 'C' + str(random.randint(1, limit_c + 1))
        a = 'A' + str(random.randint(1, limit_a + 1))
        d = 'D' + str(random.randint(1, limit_d + 1))

        states.extend([c, a, d])

    # Verificar se o número de estados excede o limite máximo
    if len(states) > max_states:
        states = states[:max_states]

    initial_state = random.choice(states)
    transitions = []

    for state in states:
        for symbol in ['0', '1']:
            if symbol == '0':
                valid_symbol = '1'
            else:
                valid_symbol = '0'

            if state.startswith('C'):
                valid_next_state = random.choice(['A', 'D']) + state[1:]
            elif state.startswith('A'):
                valid_next_state = random.choice(['C', 'D']) + state[1:]
            else:
                valid_next_state = random.choice(['C', 'A']) + state[1:]

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


generate_afd(10, 5, 7, 3, 2, 'afd.txt')


