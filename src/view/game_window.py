import tkinter as tk


class GameWindow:
    def __init__(self, root, duelist1, duelist2):
        self.duelist1_state_label = None
        self.duelist2_life_label = None
        self.duelist2_state_label = None
        self.play_button = None
        self.duelist1_life_label = None
        self.turn_label = None
        self.choice_entry = None
        self.result_label = None
        self.current_player_label = None
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
        tk.Label(self.root, text="Medieval Duel", font=("Arial", 20, "bold")).pack(pady=10)

        self.current_player_label = tk.Label(self.root, text=f"Current Player: {self.current_player.name}",
                                             font=("Arial", 12, "bold"))
        self.current_player_label.pack(pady=5)

        duelist1_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        tk.Label(duelist1_frame, text=f"Name: {self.duelist1.name}").pack()
        self.duelist1_life_label = tk.Label(
            duelist1_frame,
            text=f"Life Points: {self.duelist1.life_points}/{self.duelist1.max_life_points}"
        )
        self.duelist1_life_label.pack()
        self.duelist1_state_label = tk.Label(duelist1_frame, text=f"State: {self.duelist1.state}")
        self.duelist1_state_label.pack()
        duelist1_frame.pack(side=tk.LEFT, padx=20)

        duelist2_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        tk.Label(duelist2_frame, text=f"Name: {self.duelist2.name}").pack()
        self.duelist2_life_label = tk.Label(
            duelist2_frame,
            text=f"Life Points: {self.duelist2.life_points}/{self.duelist2.max_life_points}"
        )
        self.duelist2_life_label.pack()
        self.duelist2_state_label = tk.Label(duelist2_frame, text=f"State: {self.duelist2.state}")
        self.duelist2_state_label.pack()
        duelist2_frame.pack(side=tk.RIGHT, padx=20)

        self.turn_label = tk.Label(self.root, text=f"Turn: {self.turn}")
        self.turn_label.pack(pady=20)

        tk.Label(self.root, text="Choose a reading:", font=("Arial", 12, "bold")).pack()

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

        tk.Button(
            self.root,
            text="Show Machines",
            font=("Arial", 12, "bold"),
            bg="blue",
            fg="white",
            command=self.show_machines
        ).pack(pady=10)

    def update_stats(self):
        self.duelist1_life_label.config(
            text=f"Life Points: {self.duelist1.life_points}/{self.duelist1.max_life_points}"
        )
        self.duelist1_state_label.config(text=f"State: {self.duelist1.state}")

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
