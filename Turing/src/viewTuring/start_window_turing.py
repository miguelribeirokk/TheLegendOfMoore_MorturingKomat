import tkinter as tk

from controllerTuring.generate_turing_machine import generate_turing_machine
from modelTuring.duelist_turing import Duelist
from viewTuring.game_window_turing import GameWindow

duelist1_states_quantity = 8
duelist2_states_quantity = 8

duelist1_machine_file = '../files/turing1.txt'
duelist2_machine_file = '../files/turing2.txt'


class StartWindow:
    def __init__(self, root):
        self.life_entry = None
        self.duelist1_name_entry = "Scorpion"
        self.duelist2_name_entry = "Sub-Zero"
        self.root = root
        self.create_widgets()

    def create_widgets(self):


        tk.Label(self.root, text="MORTURING KOMBAT", font=("GodOfWar", 20, "bold"), fg="red").pack(pady=10)


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

        life_points = int(self.life_entry.get())

        self.root.destroy()

        duel_root = tk.Tk()
        duel_root.title("Duelo Turing")

        generate_turing_machine(duelist1_states_quantity, duelist1_machine_file)
        generate_turing_machine(duelist2_states_quantity, duelist2_machine_file)

        duelist1 = Duelist(self.duelist1_name_entry, duelist1_machine_file, life_points)
        duelist2 = Duelist(self.duelist2_name_entry, duelist2_machine_file, life_points)

        GameWindow(duel_root, duelist1, duelist2)
        duel_root.mainloop()
