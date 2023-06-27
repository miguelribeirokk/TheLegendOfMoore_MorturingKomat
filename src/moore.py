import tkinter as tk
import random
from enum import Enum
import generate_moore_machine as gmm

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
            damage = random.randint(0, 20)
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
            state_label = tk.Label(transitions_window, text=f"State: {current_state} -- Production: {self.productions[current_state].value}", font=("Arial", 12, "bold"))
            state_label.pack()

            for input_, next_state in transitions.items():
                production = self.productions[next_state]
                transition_label = tk.Label(
                    transitions_window,
                    text=f"Input: {input_} --- Next State: {next_state} --- Production: {production.value}",
                    font=("Arial", 10)
                )
                transition_label.pack()


class StartWindow:
    def __init__(self, root):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Medieval Duel Setup", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)

        self.duelist1_name_label = tk.Label(self.root, text="Duelist 1 Name:")
        self.duelist1_name_label.pack()
        self.duelist1_name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.duelist1_name_entry.pack()

        self.duelist2_name_label = tk.Label(self.root, text="Duelist 2 Name:")
        self.duelist2_name_label.pack()
        self.duelist2_name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.duelist2_name_entry.pack()

        self.life_label = tk.Label(self.root, text="Life Points:")
        self.life_label.pack()
        self.life_entry = tk.Entry(self.root, font=("Arial", 12))
        self.life_entry.pack()

        self.start_button = tk.Button(
            self.root,
            text="Start Duel",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=self.start_duel
        )
        self.start_button.pack(pady=20)

    def start_duel(self):
        duelist1_name = self.duelist1_name_entry.get()
        duelist2_name = self.duelist2_name_entry.get()
        life_points = int(self.life_entry.get())

        self.root.destroy()

        duel_root = tk.Tk()
        duel_root.title("Medieval Duel")

        gmm.generate_moore_machine(5, "../files/file1.txt")
        gmm.generate_moore_machine(5, "../files/file2.txt")

        duelist1 = Duelist(duelist1_name, "../files/file1.txt", life_points)
        duelist2 = Duelist(duelist2_name, "../files/file2.txt", life_points)

        game_window = GameWindow(duel_root, duelist1, duelist2)
        duel_root.mainloop()


class GameWindow:
    def __init__(self, root, duelist1, duelist2):
        self.root = root
        self.duelist1 = duelist1
        self.duelist2 = duelist2

        self.turn = 1
        self.current_player = self.duelist1 if self.turn % 2 != 0 else self.duelist2  # Definir jogador atual
        self.create_widgets()
        self.update_stats()

    def show_machines(self):
        self.duelist1.show_transitions()
        self.duelist2.show_transitions()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Medieval Duel", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)

        self.current_player_label = tk.Label(self.root, text=f"Current Player: {self.current_player.name}",
                                             font=("Arial", 12, "bold"))
        self.current_player_label.pack(pady=5)

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

        self.show_machines_button = tk.Button(
            self.root,
            text="Show Machines",
            font=("Arial", 12, "bold"),
            bg="blue",
            fg="white",
            command=self.show_machines
        )
        self.show_machines_button.pack(pady=10)

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

        if self.current_player == self.duelist1:
            opponent = self.duelist2
        else:
            opponent = self.duelist1

        self.current_player.play_turn(opponent, choice)
        self.update_stats()

        if self.duelist1.life_points <= 0:
            self.result_label.config(text=f"{self.duelist1.name} has been defeated!", fg="red")
            self.play_button.config(state=tk.DISABLED)
        elif self.duelist2.life_points <= 0:
            self.result_label.config(text=f"{self.duelist2.name} has been defeated!", fg="red")
            self.play_button.config(state=tk.DISABLED)

        self.turn += 1
        self.current_player = self.duelist1 if self.turn % 2 != 0 else self.duelist2  # Atualizar jogador atual
        self.current_player_label.config(text=f"Current Player: {self.current_player.name}")  # Atualizar rótulo
        self.choice_entry.delete(0, tk.END)








if __name__ == "__main__":
    root = tk.Tk()
    start_window = StartWindow(root)
    root.mainloop()