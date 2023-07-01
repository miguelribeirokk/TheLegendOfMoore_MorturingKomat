import random

from modelTuring.action_enum_turing import  Action

max_attack = 20
max_heal = 10
max_defense = 10


class Duelist:
    def __init__(self, name, machine_file, max_life):
        self.name = name
        self.state = "S1"
        self.transitions = {}
        self.tape = ['<', ' ']
        self.head = 1
        self.actions = {}
        self.initial = None
        self.max_life_points = max_life
        self.life_points = max_life
        self.load_machine(machine_file)

    def load_machine(self, machine_file):
        with open(machine_file, 'r') as file:
            lines = file.readlines()

        initial_state_line = lines[1].strip().split(' ')[1]
        transitions_lines = lines[2:]

        self.initial = initial_state_line

        for line in transitions_lines:
            line = line.strip().split(' ')
            current_state = line[0]
            next_state = line[2]
            read = line[4]
            write = line[6]
            direction = line[7]
            self.add_transition(current_state, next_state, read, write, direction)

    @property
    def get_actions(self):
        return self.actions

    def add_transition(self, current_state, next_state, read, write, direction):
        if current_state not in self.transitions:
            self.transitions[current_state] = {}
        self.transitions[current_state][read] = [next_state, write, direction]

    def remove_actions(self):
        self.actions = {}

    def execute_machine(self, choice, target):
        if self.tape[self.head] == ' ':
            self.tape[self.head] = str(choice)
            self.tape.append(' ')

        next_state = self.transitions[self.state][self.tape[self.head]][0]
        write = self.transitions[self.state][self.tape[self.head]][1]
        direction = self.transitions[self.state][self.tape[self.head]][2]

        self.tape[self.head] = write

        if self.tape[self.head] == Action.ATAQUE.value:
            damage = random.randint(1, max_attack)
            self.actions[self.name] = [damage, Action.ATAQUE.value, target.name]
        elif self.tape[self.head] == Action.DEFESA.value:
            defense = random.randint(1, max_defense)
            self.actions[self.name] = [defense, Action.DEFESA.value, self.name]
        elif self.tape[self.head] == Action.CURA.value:
            heal = random.randint(1, max_heal)
            self.actions[self.name] = [heal, Action.CURA.value, self.name]
        if direction == 'D':
            self.head += 1
        elif direction == 'E':
            self.head -= 1
        self.state = next_state



    def play_turn(self, opponent, choice):
        self.actions = {}
        opponent.remove_actions()

        if self.state is None:
            self.state = self.initial
        if opponent.state is None:
            opponent.state = opponent.initial

        self.execute_machine(choice, opponent)
        opponent.execute_machine(choice, self)

        self.resolve_actions(opponent)

    def resolve_actions(self, opponent):
        if self.name in self.actions and opponent.name in opponent.actions:
            action_self = self.actions[self.name]
            action_opponent = opponent.actions[opponent.name]

            if action_self[1] == Action.ATAQUE.value and action_opponent[1] == Action.ATAQUE.value:
                damage_self = action_self[0]
                damage_opponent = action_opponent[0]
                self.life_points -= damage_opponent
                opponent.life_points -= damage_self
            elif action_self[1] == Action.DEFESA.value and action_opponent[1] == Action.DEFESA.value:
                pass  # No action taken
            else:
                if action_self[1] == Action.ATAQUE.value and action_opponent[1] == Action.DEFESA.value:
                    damage_self = action_self[0]
                    defense_opponent = action_opponent[0]
                    damage_opponent = max(0, damage_self - defense_opponent)
                    opponent.life_points -= damage_opponent
                elif action_self[1] == Action.DEFESA.value and action_opponent[1] == Action.ATAQUE.value:
                    defense_self = action_self[0]
                    damage_opponent = action_opponent[0]
                    damage_self = max(0, damage_opponent - defense_self)
                    self.life_points -= damage_self

            if action_self[1] == Action.CURA.value and action_opponent[1] == Action.CURA.value:
                heal_self = action_self[0]
                heal_opponent = action_opponent[0]
                self.life_points += heal_self
                opponent.life_points += heal_opponent
            else:
                if action_self[1] == Action.CURA.value and action_opponent[1] != Action.CURA.value:
                    if action_opponent[1] == Action.ATAQUE.value:
                        damage_self = action_opponent[0]
                        self.life_points -= damage_self
                    heal_self = action_self[0]
                    self.life_points += heal_self
                elif action_self[1] != Action.CURA.value and action_opponent[1] == Action.CURA.value:
                    if action_self[1] == Action.ATAQUE.value:
                        damage_opponent = action_self[0]
                        opponent.life_points -= damage_opponent
                    heal_opponent = action_opponent[0]
                    opponent.life_points += heal_opponent

            self.life_points = min(self.life_points, self.max_life_points)
            opponent.life_points = min(opponent.life_points, opponent.max_life_points)
