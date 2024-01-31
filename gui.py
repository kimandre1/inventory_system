import tkinter as tk
from tkinter import messagebox

class SimpleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Lager og logistikk system (LOLS)")

        # Create buttons
        self.btn_vareliste = tk.Button(master, text="Vareliste", command=self.show_vareliste)
        self.btn_vis_ordre = tk.Button(master, text="Vis Ordre", command=self.show_vis_ordre)
        self.btn_lag_faktura = tk.Button(master, text="Lag Faktura", command=self.show_lag_faktura)

        # Pack buttons
        self.btn_vareliste.pack(pady=10)
        self.btn_vis_ordre.pack(pady=10)
        self.btn_lag_faktura.pack(pady=10)

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

