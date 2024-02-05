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
        self.btn_inspiser_ordre = tk.Button(master, text="Inspiser Ordre", command=self.inspect_order)

        # Grid layout for buttons
        self.btn_vareliste.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.btn_vis_ordre.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.btn_lag_faktura.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.btn_inspiser_ordre.grid(row=0, column=3, padx=10, pady=10, sticky="w")

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
    
    def inspect_order(self):
        # Check if a row is selected
        selected_item = self.vis_ordre_tree.selection()
    
        if not selected_item:
            messagebox.showinfo("Informasjon", "Trykk på en ordre først")
            return

        item_values = self.vis_ordre_tree.item(selected_item)['values']
        order_id = item_values[0]

        # Called stored procedure using order id
        connection = connect_info()

        if connection:
            try:
                # Call the stored procedure
                results_inspect_order = execute_stored_procedure("InspectOrder", (order_id,))

                # Show the results in a new window with a combined Treeview and additional information
                self.show_combined_results(order_id, results_inspect_order)
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")

    def show_combined_results(self, order_id, results_inspect_order):
        # Create a new window to display combined results
        combined_window = tk.Toplevel(self.master)
        combined_window.title(f"Inspiser Ordre: {order_id}")

        # Create a Treeview to display combined results
        combined_tree = ttk.Treeview(combined_window, columns=("Ordrenummer", "Betegnelse", "Varenummer", "Antall Solgt", "Pris per enhet", "Pris Totalt"), show="headings")
        self.configure_treeview(combined_tree, ("Ordrenummer", "Betegnelse", "Varenummer", "Antall Solgt", "Pris per enhet", "Pris Totalt"  ))

        # Insert results from InspectOrder into the Treeview
        for row in results_inspect_order:
            combined_tree.insert("", "end", values=row)

        # Pack the combined Treeview
        combined_tree.pack()

        # Fetch customer information using the stored procedure
        customer_info = execute_stored_procedure("GetClientinfo", (order_id,))

        # Check if there are any results
        if customer_info:
            # Extract customer information from the result
            customer_name = f"{customer_info[0][0]} {customer_info[0][1]}"
            customer_address = f"{customer_info[0][2]}, {customer_info[0][3]}"

            # Show customer info that doesn't need repeating
            label_customer_name = tk.Label(combined_window, text=f"Navn: {customer_name}")
            label_customer_address = tk.Label(combined_window, text=f"Addresse: {customer_address}")
            label_customer_name.pack(side="bottom")
            label_customer_address.pack(side="bottom")
        else:
            messagebox.showwarning("Advarsel", "Kundeinfo ikke funnet!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()
