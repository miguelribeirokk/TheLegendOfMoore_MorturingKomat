import random


class Duelist:
    def __init__(self, name, machine_file, max_life):
        self.opponent = None
        self.name = name
        self.state = None
        self.transitions = {}
        self.productions = {}
        self.actions = {}
        self.initial = None
        self.max_life_points = max_life
        self.life_points = max_life
        self.load_machine(machine_file)

    def load_machine(self, machine_file):
        with open(machine_file, 'r') as file:
            lines = file.readlines()

        states_line = lines[0].strip().split(' ')[1:]
        initial_state_line = lines[1].strip().split(' ')[1]
        transitions_lines = lines[2:]

        self.initial = initial_state_line

        for line in transitions_lines:
            line = line.strip().split(' ')
            current_state = line[0]
            next_state = line[2]
            input_ = line[4]
            production = random.choice(["Ataque", "Defesa", "Curar"])  # Gerar aleatoriamente a produção
            self.add_transition(current_state, next_state, input_)
            self.add_production(current_state, production)

    def add_transition(self, current_state, next_state, input_):
        if current_state not in self.transitions:
            self.transitions[current_state] = {}
        self.transitions[current_state][input_] = next_state

    def add_production(self, state, production):
        self.productions[state] = production

    def execute_machine(self, next_state, target):
        print(f"Próximo estado: {next_state}")
        print(f"Vida de {self.name}: {self.life_points}")
        production = self.productions[next_state]
        print(f"Produção: {production}")

        if production == "Ataque":
            damage = random.randint(0, 10)
            self.actions[self.name] = [damage, "Ataque", target.name]
        elif production == "Defesa":
            defense = random.randint(0, 10)
            self.actions[self.name] = [defense, "Defesa", self.name]
        elif production == "Curar":
            heal = random.randint(0, 10)
            self.actions[self.name] = [heal, "Curar", self.name]
        self.state = next_state

    def play_turn(self, opponent):
        self.opponent = opponent
        print(f"Turno de {self.name}:")
        choice = input("Qual leitura deseja? ")
        if self.state is None:
            self.state = self.initial
        if opponent.state is None:
            opponent.state = opponent.initial
        print(f"Estado atual do duelista de {self.name}: {self.state}")
        print(f"Estado atual do duelista de {opponent.name}: {opponent.state}")
        print(f"Leitura: {choice}")
        self.execute_machine(self.transitions[self.state][choice], self.opponent)
        opponent.execute_machine(opponent.transitions[opponent.state][choice], self)

        # Executar as ações dos dois duelistas simultaneamente
        print(f"Ações do duelista de {self.name}: {self.actions[self.name]}")
        print(f"Ações do duelista de {opponent.name}: {opponent.actions[opponent.name]}")
        self.resolve_actions()

        # Atualizar pontos de vida dos duelistas
        print(f"Vida restante do duelista de {self.name}: {self.life_points}")
        print(f"Vida restante do duelista de {opponent.name}: {opponent.life_points}")
        self.opponent = None

    def resolve_actions(self):
        if self.name in self.actions and self.opponent.name in self.opponent.actions:
            print("Resolvendo ações...")
            action_self = self.actions[self.name]

            action_opponent = self.opponent.actions[self.opponent.name]
            print(action_self[1])
            print(action_opponent[1])
            # Ataque
            if action_self[1] == "Ataque" and action_opponent[1] == "Ataque":
                print("Ambos atacam")
                damage_self = action_self[0]
                damage_opponent = action_opponent[0]
                self.life_points -= damage_opponent
                self.opponent.life_points -= damage_self



            # Ambos defendem
            elif action_self[1] == "Defesa" and action_opponent[1] == "Defesa":
                print("Ambos defendem")
                pass  # Nada acontece

            # Apenas um oponente ataca e o outro defende
            else:
                if action_self[1] == "Ataque" and action_opponent[1] == "Defesa":
                    print("Apenas um ataca e o outro defende")
                    damage_self = action_self[0]
                    defense_opponent = action_opponent[0]
                    damage_opponent = max(0, damage_self - defense_opponent)
                    self.opponent.life_points -= damage_opponent

                elif action_self[1] == "Defesa" and action_opponent[1] == "Ataque":
                    print("Apenas um ataca e o outro defende, mas ao contrário")
                    defense_self = action_self[0]
                    damage_opponent = action_opponent[0]
                    damage_self = max(0, damage_opponent - defense_self)
                    self.life_points -= damage_self

            # Ambos se curam
            if action_self[1] == "Curar" and action_opponent[1] == "Curar":
                print("Ambos se curam")
                heal_self = action_self[0]
                heal_opponent = action_opponent[0]
                self.life_points += heal_self
                self.opponent.life_points += heal_opponent

            # Apenas um se cura
            else:
                if action_self[1] == "Curar" and action_opponent[1] != "Curar":
                    # primeiro verifica se o oponente atacou se sim ataca
                    print("Apenas um se cura")
                    if action_opponent[1] == "Ataque":
                        damage_self = action_opponent[0]
                        self.life_points -= damage_self
                    heal_self = action_self[0]
                    self.life_points += heal_self

                elif action_self[1] != "Curar" and action_opponent[1] == "Curar":
                    # primeiro verifica se o oponente atacou se sim ataca
                    print("Apenas um se cura, mas ao contrário")
                    if action_self[1] == "Ataque":
                        damage_opponent = action_self[0]
                        self.opponent.life_points -= damage_opponent
                    heal_opponent = action_opponent[0]
                    self.opponent.life_points += heal_opponent

            # Garantir que os pontos de vida não excedam o máximo
            self.life_points = min(self.life_points, self.max_life_points)
            self.opponent.life_points = min(self.opponent.life_points, self.opponent.max_life_points)

            # Limpar as ações
            self.actions = {}
            self.opponent.actions = {}

    def show_transitions(self):
        print(f"Transitions for {self.name}:")
        for current_state, transitions in self.transitions.items():
            print(f"State: {current_state}")
            for input_, next_state in transitions.items():
                production = self.productions[next_state]
                print(f"Input: {input_} -> Next State: {next_state}, Production: {production}")
            print()


print("Bem-vindo ao duelo!")
print("Insira o nome dos dois duelistas:")

duelist1 = input("Duelista 1: ")
duelist2 = input("Duelista 2: ")

print("Insira a vida máxima dos dois duelistas:")
max_life_points = int(input())

d1 = Duelist(duelist1, "../files/1.txt", max_life_points)
d2 = Duelist(duelist2, "../files/2.txt", max_life_points)

print("Máquina de:", d1.name)
d1.show_transitions()
print("Máquina de:", d2.name)
d2.show_transitions()

turn = 1
while d1.life_points > 0 and d2.life_points > 0:
    if turn % 2 == 1:
        d1.play_turn(d2)
        print()
    else:
        d2.play_turn(d1)
        print()
    print()

    turn += 1

if d1.life_points <= 0:
    print(f"{d1.name} foi derrotado!")
elif d2.life_points <= 0:
    print(f"{d2.name} foi derrotado!")

print("Fim do jogo.")
