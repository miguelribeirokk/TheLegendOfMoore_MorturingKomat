import tkinter as tk

from view.start_window import StartWindow

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Duelo Medieval")
    start_window = StartWindow(root)
    root.mainloop()
