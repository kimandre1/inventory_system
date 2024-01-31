import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_info, execute_stored_procedure

class SimpleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Lager og Logistikk System (LOLS)")

        # Create buttons
        self.btn_vareliste = tk.Button(master, text="Vareliste", command=lambda: self.show_table("GetVareinfo"))
        self.btn_vis_ordre = tk.Button(master, text="Vis Ordre", command=self.show_vis_ordre)
        self.btn_lag_faktura = tk.Button(master, text="Lag Faktura", command=self.show_lag_faktura)

        # Grid layout for buttons
        self.btn_vareliste.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.btn_vis_ordre.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.btn_lag_faktura.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    def show_table(self, procedure_name):
        # Create a Treeview widget
        tree = ttk.Treeview(self.master, columns=("Varenummer", "Betegnelse", "Pris", "Antall"), show="headings")
        tree.heading("Varenummer", text="Varenummer")
        tree.heading("Betegnelse", text="Betegnelse")
        tree.heading("Pris", text="Pris")
        tree.heading("Antall", text="Antall")

        # Initially hide the Treeview
        tree.grid_forget()

        # Grid layout for Treeview with row and column configuration
        tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.master.columnconfigure(0, weight=1)  # Allow column 0 to expand
        self.master.rowconfigure(1, weight=1)     # Allow row 1 to expand

        # Call the stored procedure when the button is clicked
        self.show_vareliste(tree, procedure_name)

    def show_vareliste(self, tree, procedure_name):
        # Connect to the database
        connection = connect_info()

        if connection:
            try:
                # Call the stored procedure
                results = execute_stored_procedure("GetVareinfo")

                if results is not None:
                    # Clear previous content
                    tree.delete(*tree.get_children())

                    # Insert new content into the Treeview
                    for row in results:
                        tree.insert("", "end", values=row)

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
