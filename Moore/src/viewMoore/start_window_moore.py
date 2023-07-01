import tkinter as tk

from controllerMoore.generate_moore_machine import generate_moore_machine
from modelMoore.duelist_moore import Duelist
from viewMoore.game_window_moore import GameWindow

duelist1_states_quantity = 8
duelist2_states_quantity = 8

duelist1_machine_file = '../files/moore1.txt'
duelist2_machine_file = '../files/moore2.txt'


class StartWindow:
    def __init__(self, root):
        self.life_entry = None
        self.duelist1_name_entry = None
        self.duelist2_name_entry = None
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="DUELO MEDIEVAL", font=("GodOfWar", 20, "bold")).pack(pady=10)
        tk.Label(self.root, text="MÁQUINA DE MOORE", font=("GodOfWar", 20, "bold"), fg="purple").pack(pady=10)
        tk.Label(self.root, text="Nome do duelista 1:", font=("Arial", 12)).pack()
        self.duelist1_name_entry = tk.Entry(self.root, font=("Arial", 14))
        self.duelist1_name_entry.pack()

        tk.Label(self.root, text="Nome do duelista 2:", font=("Arial", 12)).pack()
        self.duelist2_name_entry = tk.Entry(self.root, font=("Arial", 14))
        self.duelist2_name_entry.pack()

        tk.Label(self.root, text="Vida:", font=("Arial", 12)).pack()
        self.life_entry = tk.Entry(self.root, font=("Arial", 14))
        self.life_entry.pack()

        tk.Button(
            self.root,
            text="Começar duelo",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=self.check_life
        ).pack(pady=20)

    def check_life(self):
        try:
            life = int(self.life_entry.get())
            if not life or life <= 0:
                self.popup_message("Vida deve ser maior que 0")
            else:
                self.start_duel()
        except ValueError:
            self.popup_message("Vida deve ser um número inteiro")

    def popup_message(self, msg):
        popup = tk.Tk()
        popup.wm_title("AVISO")
        label = tk.Label(popup, text=msg, font=("Arial", 14))
        label.pack(side="top", fill="x", pady=10)
        B1 = tk.Button(popup, text="OK", command=popup.destroy, font=("Arial", 10), bg="red", fg="white")
        B1.pack()
        popup.mainloop()

    def start_duel(self):
        duelist1_name = self.duelist1_name_entry.get()
        duelist2_name = self.duelist2_name_entry.get()
        life_points = int(self.life_entry.get())

        self.root.destroy()

        duel_root = tk.Tk()
        duel_root.title("Duelo Medieval Moore")

        generate_moore_machine(duelist1_states_quantity, duelist1_machine_file)
        generate_moore_machine(duelist2_states_quantity, duelist2_machine_file)

        duelist1 = Duelist(duelist1_name, duelist1_machine_file, life_points)
        duelist2 = Duelist(duelist2_name, duelist2_machine_file, life_points)

        GameWindow(duel_root, duelist1, duelist2)
        duel_root.mainloop()
