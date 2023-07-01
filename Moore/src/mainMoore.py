import tkinter as tk

from viewMoore.start_window_moore import StartWindow

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Duelo Medieval Moore")
    start_window = StartWindow(root)
    root.mainloop()
