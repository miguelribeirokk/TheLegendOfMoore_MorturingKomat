import tkinter as tk
import random
from enum import Enum


class Action(Enum):
    ATTACK = "Attack"
    DEFENSE = "Defense"
    HEAL = "Heal"


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
            production = random.choice(list(Action))
            self.add_transition(current_state, next_state, input_)
            self.add_production(current_state, production)

    def add_transition(self, current_state, next_state, input_):
        if current_state not in self.transitions:
            self.transitions[current_state] = {}
        self.transitions[current_state][input_] = next_state

    def add_production(self, state, production):
        self.productions[state] = production

    def execute_machine(self, next_state, target):
        production = self.productions[next_state]

        if production == Action.ATTACK:
            damage = random.randint(0, 10)
            self.actions[self.name] = [damage, Action.ATTACK, target.name]
        elif production == Action.DEFENSE:
            defense = random.randint(0, 10)
            self.actions[self.name] = [defense, Action.DEFENSE, self.name]
        elif production == Action.HEAL:
            heal = random.randint(0, 10)
            self.actions[self.name] = [heal, Action.HEAL, self.name]
        self.state = next_state

    def play_turn(self, opponent, choice):
        self.opponent = opponent

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

            if action_self[1] == Action.ATTACK and action_opponent[1] == Action.ATTACK:
                damage_self = action_self[0]
                damage_opponent = action_opponent[0]
                self.life_points -= damage_opponent
                self.opponent.life_points -= damage_self
            elif action_self[1] == Action.DEFENSE and action_opponent[1] == Action.DEFENSE:
                pass  # No action taken
            else:
                if action_self[1] == Action.ATTACK and action_opponent[1] == Action.DEFENSE:
                    damage_self = action_self[0]
                    defense_opponent = action_opponent[0]
                    damage_opponent = max(0, damage_self - defense_opponent)
                    self.opponent.life_points -= damage_opponent
                elif action_self[1] == Action.DEFENSE and action_opponent[1] == Action.ATTACK:
                    defense_self = action_self[0]
                    damage_opponent = action_opponent[0]
                    damage_self = max(0, damage_opponent - defense_self)
                    self.life_points -= damage_self

            if action_self[1] == Action.HEAL and action_opponent[1] == Action.HEAL:
                heal_self = action_self[0]
                heal_opponent = action_opponent[0]
                self.life_points += heal_self
                self.opponent.life_points += heal_opponent
            else:
                if action_self[1] == Action.HEAL and action_opponent[1] != Action.HEAL:
                    if action_opponent[1] == Action.ATTACK:
                        damage_self = action_opponent[0]
                        self.life_points -= damage_self
                    heal_self = action_self[0]
                    self.life_points += heal_self
                elif action_self[1] != Action.HEAL and action_opponent[1] == Action.HEAL:
                    if action_self[1] == Action.ATTACK:
                        damage_opponent = action_self[0]
                        self.opponent.life_points -= damage_opponent
                    heal_opponent = action_opponent[0]
                    self.opponent.life_points += heal_opponent

            self.life_points = min(self.life_points, self.max_life_points)
            self.opponent.life_points = min(self.opponent.life_points, self.opponent.max_life_points)

            self.actions = {}
            self.opponent.actions = {}

    def show_transitions(self):
        transitions_window = tk.Toplevel()
        transitions_window.title(f"Transitions for {self.name}")

        for current_state, transitions in self.transitions.items():
            state_label = tk.Label(transitions_window, text=f"State: {current_state}", font=("Arial", 12, "bold"))
            state_label.pack()

            for input_, next_state in transitions.items():
                production = self.productions[next_state]
                transition_label = tk.Label(
                    transitions_window,
                    text=f"Input: {input_} -> Next State: {next_state}, Production: {production.value}",
                    font=("Arial", 10)
                )
                transition_label.pack()


class GameWindow:
    def __init__(self, root, duelist1, duelist2):
        self.root = root
        self.duelist1 = duelist1
        self.duelist2 = duelist2

        self.turn = 1
        self.create_widgets()
        self.update_stats()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Medieval Duel", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)

        self.duelist1_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        self.duelist1_name_label = tk.Label(self.duelist1_frame, text=f"Name: {self.duelist1.name}")
        self.duelist1_name_label.pack()
        self.duelist1_life_label = tk.Label(
            self.duelist1_frame,
            text=f"Life Points: {self.duelist1.life_points}/{self.duelist1.max_life_points}"
        )
        self.duelist1_life_label.pack()
        self.duelist1_state_label = tk.Label(self.duelist1_frame, text=f"State: {self.duelist1.state}")
        self.duelist1_state_label.pack()
        self.duelist1_frame.pack(side=tk.LEFT, padx=20)

        self.duelist2_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        self.duelist2_name_label = tk.Label(self.duelist2_frame, text=f"Name: {self.duelist2.name}")
        self.duelist2_name_label.pack()
        self.duelist2_life_label = tk.Label(
            self.duelist2_frame,
            text=f"Life Points: {self.duelist2.life_points}/{self.duelist2.max_life_points}"
        )
        self.duelist2_life_label.pack()
        self.duelist2_state_label = tk.Label(self.duelist2_frame, text=f"State: {self.duelist2.state}")
        self.duelist2_state_label.pack()
        self.duelist2_frame.pack(side=tk.RIGHT, padx=20)

        self.turn_label = tk.Label(self.root, text=f"Turn: {self.turn}")
        self.turn_label.pack(pady=20)

        self.choice_label = tk.Label(self.root, text="Choose a reading:", font=("Arial", 12, "bold"))
        self.choice_label.pack()

        self.choice_entry = tk.Entry(self.root, font=("Arial", 12))
        self.choice_entry.pack()

        self.play_button = tk.Button(
            self.root,
            text="Play",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=self.play_turn
        )
        self.play_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"))
        self.result_label.pack(pady=20)

    def update_stats(self):
        self.duelist1_name_label.config(text=f"Name: {self.duelist1.name}")
        self.duelist1_life_label.config(
            text=f"Life Points: {self.duelist1.life_points}/{self.duelist1.max_life_points}"
        )
        self.duelist1_state_label.config(text=f"State: {self.duelist1.state}")

        self.duelist2_name_label.config(text=f"Name: {self.duelist2.name}")
        self.duelist2_life_label.config(
            text=f"Life Points: {self.duelist2.life_points}/{self.duelist2.max_life_points}"
        )
        self.duelist2_state_label.config(text=f"State: {self.duelist2.state}")

        self.turn_label.config(text=f"Turn: {self.turn}")

    def play_turn(self):
        choice = self.choice_entry.get()
        self.duelist1.play_turn(self.duelist2, choice)
        self.update_stats()

        if self.duelist1.life_points <= 0:
            self.result_label.config(text=f"{self.duelist1.name} has been defeated!", fg="red")
            self.play_button.config(state=tk.DISABLED)
        elif self.duelist2.life_points <= 0:
            self.result_label.config(text=f"{self.duelist2.name} has been defeated!", fg="red")
            self.play_button.config(state=tk.DISABLED)

        self.turn += 1
        self.turn_label.config(text=f"Turn: {self.turn}")
        self.choice_entry.delete(0, tk.END)


def main():
    root = tk.Tk()
    root.title("Medieval Duel")

    duelist1 = Duelist("Player", "../files/1.txt", 100)
    duelist2 = Duelist("AI", "../files/2.txt", 100)

    game_window = GameWindow(root, duelist1, duelist2)

    root.mainloop()


if __name__ == "__main__":
    main()