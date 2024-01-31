import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_info, execute_stored_procedure

class SimpleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Lager og Logistikk System (LOLS)")

        # Create a Treeview widget
        self.tree = ttk.Treeview(master, columns=("Varenummer", "Betegnelse", "Pris", "Antall"), show="headings")
        self.tree.heading("Varenummer", text="Varenummer")
        self.tree.heading("Betegnelse", text="Betegnelse")
        self.tree.heading("Pris", text="Pris")
        self.tree.heading("Antall", text="Antall")

        # Create buttons
        self.btn_vareliste = tk.Button(master, text="Vareliste", command=self.toggle_treeview)
        self.btn_vis_ordre = tk.Button(master, text="Vis Ordre", command=self.show_vis_ordre)
        self.btn_lag_faktura = tk.Button(master, text="Lag Faktura", command=self.show_lag_faktura)

        # Grid layout for buttons
        self.btn_vareliste.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.btn_vis_ordre.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.btn_lag_faktura.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # Grid layout for Treeview
        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        # Initially hide the Treeview
        self.tree.grid_forget()
    
    def toggle_treeview(self):
    # Toggle the visibility of the Treeview
        if self.tree.winfo_ismapped():
        # If currently visible, hide it
            self.tree.grid_remove()
        else:
        # If currently hidden, show it
            self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        # Call the stored procedure when the button is clicked
            self.show_vareliste()


    def show_vareliste(self):
        # Connect to the database
        connection = connect_info()

        if connection:
            try:
                # Call the stored procedure
                results = execute_stored_procedure("GetVareinfo")

                if results is not None:
                    # Clear previous content
                    self.tree.delete(*self.tree.get_children())

                    # Insert new content into the Treeview
                    for row in results:
                        self.tree.insert("", "end", values=row)

            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")

    def show_vis_ordre(self):
        messagebox.showinfo("Button Clicked", "Vis Ordre button clicked!")

    def show_lag_faktura(self):
        messagebox.showinfo("Button Clicked", "Lag Faktura button clicked!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()