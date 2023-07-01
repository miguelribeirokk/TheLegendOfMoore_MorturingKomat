import tkinter as tk

from viewTuring.start_window_turing import StartWindow

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Duelo Medieval")
    start_window = StartWindow(root)
    root.mainloop()
