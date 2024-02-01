import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_info, execute_stored_procedure

class SimpleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Lager og Logistikk System (LOLS)")

        # Create Treeviews
        self.vareliste_tree = ttk.Treeview(self.master, columns=("Varenummer", "Betegnelse", "Pris", "Antall"), show="headings")
        self.configure_treeview(self.vareliste_tree, ("Varenummer", "Betegnelse", "Pris", "Antall"))

        self.vis_ordre_tree = ttk.Treeview(self.master, columns=("Ordrenummer", "Bestillingsdato", "Sendt", "Betalt", "Kundenummer"), show="headings")
        self.configure_treeview(self.vis_ordre_tree, ("Ordrenummer", "Bestillingsdato", "Sendt", "Betalt", "Kundenummer"))

        # Create buttons
        self.btn_vareliste = tk.Button(master, text="Vareliste", command=self.show_vareliste)
        self.btn_vis_ordre = tk.Button(master, text="Vis Ordre", command=self.show_vis_ordre)
        self.btn_lag_faktura = tk.Button(master, text="Lag Faktura", command=self.show_lag_faktura)

        # Grid layout for buttons
        self.btn_vareliste.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.btn_vis_ordre.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.btn_lag_faktura.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # Initially hide the Treeviews
        self.vareliste_tree.grid_forget()
        self.vis_ordre_tree.grid_forget()

    def configure_treeview(self, tree, columns):
        for column in columns:
            tree.heading(column, text=column)
        tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)

    def show_vareliste(self):
        # Hide Vis Ordre Treeview
        self.vis_ordre_tree.grid_forget()

        # Connect to the database
        connection = connect_info()

        if connection:
            try:
                # Call the stored procedure
                results = execute_stored_procedure("GetVareinfo")

                if results is not None:
                    # Clear previous content
                    self.vareliste_tree.delete(*self.vareliste_tree.get_children())

                    # Insert new content into the Treeview
                    for row in results:
                        self.vareliste_tree.insert("", "end", values=row)

                    # Show the Treeview
                    self.vareliste_tree.grid()

            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")

    def show_vis_ordre(self):
        # Hide Vareliste Treeview
        self.vareliste_tree.grid_forget()

        # Connect to the database
        connection = connect_info()

        if connection:
            try:
                # Call the stored procedure
                results = execute_stored_procedure("GetOrdreinfo")

                if results is not None:
                    # Clear previous content
                    self.vis_ordre_tree.delete(*self.vis_ordre_tree.get_children())

                    # Insert new content into the Treeview
                    for row in results:
                        self.vis_ordre_tree.insert("", "end", values=row)

                    # Show the Treeview
                    self.vis_ordre_tree.grid()

            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")

    def show_lag_faktura(self):
        messagebox.showinfo("Button Clicked", "Lag Faktura button clicked!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()
