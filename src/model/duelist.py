import random
import tkinter as tk

from model.action_enum import Action

max_attack = 20
max_heal = 10
max_defense = 10


class Duelist:
    def __init__(self, name, machine_file, max_life):
        self.opponent = None
        self.name = name
        self.state = "S1"
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

        initial_state_line = lines[1].strip().split(' ')[1]
        transitions_lines = lines[2:]

        self.initial = initial_state_line

        for line in transitions_lines:
            line = line.strip().split(' ')
            current_state = line[0]
            next_state = line[2]
            input_ = line[4]
            production = random.choice(list(Action))
            self.add_transition(current_state, next_state, input_)
            self.add_production(current_state, production)

    def get_actions(self):
        return self.actions

    def add_transition(self, current_state, next_state, input_):
        if current_state not in self.transitions:
            self.transitions[current_state] = {}
        self.transitions[current_state][input_] = next_state

    def add_production(self, state, production):
        self.productions[state] = production

    def execute_machine(self, next_state, target):
        production = self.productions[next_state]

        if production == Action.ATAQUE:
            damage = random.randint(1, max_attack)
            self.actions[self.name] = [damage, Action.ATAQUE, target.name]
        elif production == Action.DEFESA:
            defense = random.randint(1, max_defense)
            self.actions[self.name] = [defense, Action.DEFESA, self.name]
        elif production == Action.CURA:
            heal = random.randint(1, max_heal)
            self.actions[self.name] = [heal, Action.CURA, self.name]
        self.state = next_state

    def play_turn(self, opponent, choice):
        self.opponent = opponent


        self.actions = {}
        self.opponent.actions = {}



        if self.state is None:
            self.state = self.initial
        if opponent.state is None:
            opponent.state = opponent.initial

        self.execute_machine(self.transitions[self.state][choice], self.opponent)
        opponent.execute_machine(opponent.transitions[opponent.state][choice], self)

        self.resolve_actions()

        self.opponent = None

    def resolve_actions(self):
        if self.name in self.actions and self.opponent.name in self.opponent.actions:
            action_self = self.actions[self.name]
            action_opponent = self.opponent.actions[self.opponent.name]

            if action_self[1] == Action.ATAQUE and action_opponent[1] == Action.ATAQUE:
                damage_self = action_self[0]
                damage_opponent = action_opponent[0]
                self.life_points -= damage_opponent
                self.opponent.life_points -= damage_self
            elif action_self[1] == Action.DEFESA and action_opponent[1] == Action.DEFESA:
                pass  # No action taken
            else:
                if action_self[1] == Action.ATAQUE and action_opponent[1] == Action.DEFESA:
                    damage_self = action_self[0]
                    defense_opponent = action_opponent[0]
                    damage_opponent = max(0, damage_self - defense_opponent)
                    self.opponent.life_points -= damage_opponent
                elif action_self[1] == Action.DEFESA and action_opponent[1] == Action.ATAQUE:
                    defense_self = action_self[0]
                    damage_opponent = action_opponent[0]
                    damage_self = max(0, damage_opponent - defense_self)
                    self.life_points -= damage_self

            if action_self[1] == Action.CURA and action_opponent[1] == Action.CURA:
                heal_self = action_self[0]
                heal_opponent = action_opponent[0]
                self.life_points += heal_self
                self.opponent.life_points += heal_opponent
            else:
                if action_self[1] == Action.CURA and action_opponent[1] != Action.CURA:
                    if action_opponent[1] == Action.ATAQUE:
                        damage_self = action_opponent[0]
                        self.life_points -= damage_self
                    heal_self = action_self[0]
                    self.life_points += heal_self
                elif action_self[1] != Action.CURA and action_opponent[1] == Action.CURA:
                    if action_self[1] == Action.ATAQUE:
                        damage_opponent = action_self[0]
                        self.opponent.life_points -= damage_opponent
                    heal_opponent = action_opponent[0]
                    self.opponent.life_points += heal_opponent

            self.life_points = min(self.life_points, self.max_life_points)
            self.opponent.life_points = min(self.opponent.life_points, self.opponent.max_life_points)



    def show_transitions(self):
        transitions_window = tk.Toplevel()
        transitions_window.title(f"{self.name}")

        for current_state, transitions in self.transitions.items():
            state_label = tk.Label(transitions_window,
                                   text=f"Estado: {current_state} "
                                        f" → Produção: {self.productions[current_state].value}",
                                   font=("Arial", 12, "bold"))
            state_label.pack()

            for input_, next_state in transitions.items():
                production = self.productions[next_state]
                transition_label = tk.Label(
                    transitions_window,
                    text=f"{input_} → {next_state}",
                    font=("Arial", 10)
                )
                transition_label.pack()

    # def show_actions(self, opponent):














