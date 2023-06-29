import tkinter as tk


class GameWindow:
    def __init__(self, root, duelist1, duelist2):
        self.duelist1_state_label = None
        self.duelist2_life_label = None
        self.duelist2_state_label = None
        self.play_button = None
        self.duelist1_life_label = None
        self.duelist1_actions_label = None
        self.duelist2_actions_label = None
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

        tk.Label(self.root, text="DUELO MEDIEVAL", font=("GodOfWar", 20, "bold")).pack(pady=10)

        self.current_player_label = tk.Label(self.root, text=f"Turno de {self.current_player.name}",
                                             font=("GodOfWar", 14, "bold"), fg="purple")
        self.current_player_label.pack(pady=5)

        self.current_player_label = tk.Label(self.root, text=f"Qual leitura você deseja fazer? ",
                                             font=("Arial", 12, "bold"))
        self.current_player_label.pack(pady=5)

        duelist1_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        tk.Label(duelist1_frame, text="DUELISTA 1", font=("GodOfWar", 12)).pack()
        tk.Label(duelist1_frame, text=f"Nome: {self.duelist1.name}", font=("Arial", 12)).pack()
        self.duelist1_life_label = tk.Label(
            duelist1_frame,
            text=f"Vida atual: {self.duelist1.life_points}/{self.duelist1.max_life_points}",
            font=("Arial", 12)
        )
        self.duelist1_life_label.pack()
        self.duelist1_state_label = tk.Label(duelist1_frame, text=f"Estado atual: {self.duelist1.state}",
                                             font=("Arial", 12))
        self.duelist1_state_label.pack()

        duelist1_frame.pack(side=tk.LEFT, padx=20)

        duelist2_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        tk.Label(duelist2_frame, text="DUELISTA 2", font=("GodOfWar", 12)).pack()
        tk.Label(duelist2_frame, text=f"Nome: {self.duelist2.name}", font=("Arial", 12)).pack()

        self.duelist2_life_label = tk.Label(
            duelist2_frame,
            text=f"Vida atual: {self.duelist2.life_points}/{self.duelist2.max_life_points}",
            font=("Arial", 12)
        )
        self.duelist2_life_label.pack()
        self.duelist2_state_label = tk.Label(duelist2_frame, text=f"Estado atual: {self.duelist2.state}",
                                             font=("Arial", 12))
        self.duelist2_state_label.pack()
        duelist2_frame.pack(side=tk.RIGHT, padx=20)

        self.turn_label = tk.Label(self.root, text=f"Turno: {self.turn}")
        self.turn_label.pack(pady=20)

        tk.Label(self.root, text="Digite uma leitura:", font=("Arial", 12, "bold")).pack()

        self.choice_entry = tk.Entry(self.root, font=("Arial", 12))
        self.choice_entry.pack()

        self.play_button = tk.Button(
            self.root,
            text="Ler",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=self.check_choice
        )
        self.play_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"))
        self.result_label.pack(pady=20)

        # ver produções a cada turno

        duelist_actions_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        tk.Label(duelist_actions_frame, text=f"Produções: ", font=("GodOfWar", 12, "bold")).pack()
        self.duelist1_actions_label = tk.Label(duelist_actions_frame,
                                               text=f"", font=("Arial", 12))

        self.duelist1_actions_label.pack()
        self.duelist2_actions_label = tk.Label(duelist_actions_frame, text=f"", font=("Arial", 12))
        self.duelist2_actions_label.pack()
        # no meio
        duelist_actions_frame.pack(side=tk.BOTTOM, padx=20)

        tk.Button(
            self.root,
            text="Ver máquinas",
            font=("Arial", 12, "bold"),
            bg="blue",
            fg="white",
            command=self.show_machines
        ).pack(pady=10)

    def update_stats(self):
        self.duelist1_life_label.config(
            text=f"Vida atual: {self.duelist1.life_points}/{self.duelist1.max_life_points}"
        )
        self.duelist1_state_label.config(text=f"Estado atual: {self.duelist1.state}")

        self.duelist2_life_label.config(
            text=f"Vida atual: {self.duelist2.life_points}/{self.duelist2.max_life_points}"
        )
        self.duelist2_state_label.config(text=f"Estado atual: {self.duelist2.state}")

        self.turn_label.config(text=f"Turno: {self.turn}")

        if self.current_player == self.duelist2:
            self.duelist1_actions_label.config(
                text=f"Alcançou um estado de: {', '.join(str(a[1].name) + ' ' + str(a[0]) for a in self.duelist1.actions.values())}"
                     f" no duelista {self.duelist1.name}")
            self.duelist2_actions_label.config(
                text=f"Alcançou um estado de: {', '.join(str(a[1].name) + ' ' + str(a[0]) for a in self.duelist2.actions.values())}"
                     f" no duelista {self.duelist2.name}")
        else:
            self.duelist2_actions_label.config(
                text=f"Alcançou um estado de: {', '.join(str(a[1].name) + ' ' + str(a[0]) for a in self.duelist2.actions.values())}"
                     f" no duelista {self.duelist2.name}")
            self.duelist1_actions_label.config(
                text=f"Alcançou um estado de: {', '.join(str(a[1].name) + ' ' + str(a[0]) for a in self.duelist1.actions.values())}"
                     f" no duelista {self.duelist1.name}")

    def check_choice(self):
        try:
            choice = int(self.choice_entry.get())
            if choice in [0, 1, 2]:
                self.result_label.config(text="")
                self.play_turn()
            else:
                self.result_label.config(text="Digite um número válido!", fg="red")
        except ValueError:
            self.result_label.config(text="Digite um número válido!", fg="red")


    def play_turn(self):
        choice = self.choice_entry.get()

        if self.current_player == self.duelist1:
            opponent = self.duelist2
        else:
            opponent = self.duelist1

        self.current_player.play_turn(opponent, choice)
        self.update_stats()

        if self.duelist1.life_points <= 0 and self.duelist2.life_points <= 0:
            self.result_label.config(text=f"Empate!", fg="blue")
            self.play_button.config(state=tk.DISABLED)
        elif self.duelist2.life_points <= 0:
            self.result_label.config(text=f"{self.duelist2.name} foi derrotado!", fg="red")
            self.play_button.config(state=tk.DISABLED)
        elif self.duelist1.life_points <= 0:
            self.result_label.config(text=f"{self.duelist1.name} foi derrotado!", fg="red")
            self.play_button.config(state=tk.DISABLED)

        self.turn += 1
        self.current_player = self.duelist1 if self.turn % 2 != 0 else self.duelist2  # Atualizar jogador atual
        self.choice_entry.delete(0, tk.END)
