import random

max_states = 20
max_cura = 10
max_ataque = 10
max_defesa = 10
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

class DueloAFD:
    def __init__(self, vida_inicial):
        self.duelista1 = Duelista(vida_inicial)
        self.duelista2 = Duelista(vida_inicial)
        self.transicoes1,self.st1,self.ini1 = self.ler_afd("D1.txt")
        self.transicoes2,self.st2,self.ini2 = self.ler_afd("D2.txt")

    def ler_afd(self, input_file):
        tran = []
        generate_afd(max_states, max_cura, max_ataque, max_defesa, max_states, input_file)
        with open(input_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('Q:'):
                    states = line[3:].split()
                elif line.startswith('I:'):
                    initial_state = line[3:]
                elif '->' in line and '|' in line:
                    transition_info = line.split('->')
                    current_state = transition_info[0].strip()
                    next_state, symbol = transition_info[1].split('|')
                    next_state = next_state.strip()
                    symbol = symbol.strip()
                    tran.append((current_state, symbol, next_state))
        print(tran, states, initial_state)
        return tran, states, initial_state
    def turno(self, valor: str):
        for v in valor:
            print(v)


class Duelista:
    def __init__(self, vida_inicial):
        self.vida = vida_inicial
        self.afd = None

    def executar_movimento(self, next_state):
        if next_state.startswith('C'):
            self.estado_atual = next_state
            self.cura(int(next_state[1]))
        elif next_state.startswith('A'):
            self.estado_atual = next_state
            self.ataque(int(next_state[1]))
        elif next_state.startswith('D'):
            self.estado_atual = next_state
            self.defesa(int(next_state[1]))

    def cura(self, pontos_cura):
        self.vida += pontos_cura

    def ataque(self, pontos_ataque):
        self.vida -= pontos_ataque

    def defesa(self, pontos_defesa):
        self.vida += pontos_defesa



