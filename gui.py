import tkinter as tk
from tkinter import messagebox

class SimpleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple GUI")

        # Create buttons
        self.btn_vareliste = tk.Button(master, text="Vareliste", command=self.show_vareliste)
        self.btn_vis_ordre = tk.Button(master, text="Vis Ordre", command=self.show_vis_ordre)
        self.btn_lag_faktura = tk.Button(master, text="Lag Faktura", command=self.show_lag_faktura)

        # Grid layout
        self.btn_vareliste.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.btn_vis_ordre.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.btn_lag_faktura.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    def show_vareliste(self):
        messagebox.showinfo("Button Clicked", "Vareliste button clicked!")

    def show_vis_ordre(self):
        messagebox.showinfo("Button Clicked", "Vis Ordre button clicked!")

    def show_lag_faktura(self):
        messagebox.showinfo("Button Clicked", "Lag Faktura button clicked!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()


