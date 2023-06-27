import tkinter as tk

from controller.generate_moore_machine import generate_moore_machine
from model.duelist import Duelist
from view.game_window import GameWindow


class StartWindow:
    def __init__(self, root):
        self.life_entry = None
        self.duelist1_name_entry = None
        self.duelist2_name_entry = None
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Medieval Duel Setup", font=("Arial", 20, "bold")).pack(pady=10)

        tk.Label(self.root, text="Duelist 1 Name:").pack()
        self.duelist1_name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.duelist1_name_entry.pack()

        tk.Label(self.root, text="Duelist 2 Name:").pack()
        self.duelist2_name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.duelist2_name_entry.pack()

        tk.Label(self.root, text="Life Points:").pack()
        self.life_entry = tk.Entry(self.root, font=("Arial", 12))
        self.life_entry.pack()

        tk.Button(
            self.root,
            text="Start Duel",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=self.start_duel
        ).pack(pady=20)

    def start_duel(self):
        duelist1_name = self.duelist1_name_entry.get()
        duelist2_name = self.duelist2_name_entry.get()
        life_points = int(self.life_entry.get())

        self.root.destroy()

        duel_root = tk.Tk()
        duel_root.title("Medieval Duel")

        generate_moore_machine(5, "../files/file1.txt")
        generate_moore_machine(5, "../files/file2.txt")

        duelist1 = Duelist(duelist1_name, "../files/file1.txt", life_points)
        duelist2 = Duelist(duelist2_name, "../files/file2.txt", life_points)

        GameWindow(duel_root, duelist1, duelist2)
        duel_root.mainloop()
