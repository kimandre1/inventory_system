import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from customtkinter import set_appearance_mode
from database import connect_info, execute_stored_procedure, add_user

class SimpleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Lager og Logistikk System (LOLS)")
        set_appearance_mode("Dark")
        print(ctk.get_appearance_mode())

        # Create Treeviews
        self.vareliste_tree = ttk.Treeview(self.master, columns=("Varenummer", "Betegnelse", "Pris", "Antall"), show="headings")
        self.configure_treeview(self.vareliste_tree, ("Varenummer", "Betegnelse", "Pris", "Antall"))

        self.vis_ordre_tree = ttk.Treeview(self.master, columns=("Ordrenummer", "Bestillingsdato", "Sendt", "Betalt", "Kundenummer"), show="headings")
        self.configure_treeview(self.vis_ordre_tree, ("Ordrenummer", "Bestillingsdato", "Sendt", "Betalt", "Kundenummer"))

        self.kundeliste_tree = ttk.Treeview(self.master, columns=("Kundenummer", "Fornavn", "Etternavn", "Addresse", "Postnummer"), show="headings")
        self.configure_treeview(self.kundeliste_tree, ("Kundenummer", "Fornavn", "Etternavn", "Addresse", "Postnummer"))

        # Create buttons
        self.btn_kundeliste = ctk.CTkButton(master, text="Kundeliste", command=lambda: self.show_vareliste("GetKundeInfo", self.kundeliste_tree))
        self.btn_vareliste = ctk.CTkButton(master, text="Vareliste", command=lambda: self.show_vareliste("GetVareinfo", self.vareliste_tree))
        self.btn_vis_ordre = ctk.CTkButton(master, text="Vis Ordre", command=lambda: self.show_vareliste("GetOrdreinfo", self.vis_ordre_tree))
        self.btn_lag_faktura = ctk.CTkButton(master, text="Lag Faktura", command=self.show_lag_faktura)
        self.btn_inspiser_ordre = ctk.CTkButton(master, text="Inspiser Ordre", command=self.inspect_order)
        self.btn_addkunde = ctk.CTkButton(master, text="Legg til ny kunde", command=self.add_user_form)

        # Grid layout for buttons
        self.btn_kundeliste.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.btn_addkunde.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.btn_vareliste.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.btn_vis_ordre.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        self.btn_lag_faktura.grid(row=0, column=4, padx=10, pady=10, sticky="w")
        self.btn_inspiser_ordre.grid(row=0, column=5, padx=10, pady=10, sticky="w")

        # Initially hide the Treeviews
        self.vareliste_tree.grid_forget()
        self.vis_ordre_tree.grid_forget()
        self.kundeliste_tree.grid_forget()

    def configure_treeview(self, tree, columns):
        for column in columns:
            tree.heading(column, text=column)
        tree.grid(row=1, column=0, columnspan=6, padx=10, pady=10, sticky="w")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)

    def show_vareliste(self, procedure, tree):
        # Hide Vis Ordre Treeview
        self.vis_ordre_tree.grid_forget()
        self.kundeliste_tree.grid_forget()
        self.vareliste_tree.grid_forget()

        # Connect to the database
        connection = connect_info()

        if connection:
            try:
                # Call the stored procedure
                results = execute_stored_procedure(procedure)

                if results is not None:
                    # Clear previous content
                    tree.delete(*tree.get_children())

                    # Insert new content into the Treeview
                    for row in results:
                        tree.insert("", "end", values=row)

                    # Show the Treeview
                    tree.grid()

            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
    
    def show_lag_faktura(self):
        messagebox.showinfo("Button Clicked", "Lag Faktura button clicked!")

    def add_user_form(self):
        window = tk.Toplevel(self.master)
        window.title("Legg til bruker")
        first_name_label = tk.Label(window, text="Fornavn")
        first_name_label.pack()
        self.first_name_input = tk.Entry(window)
        self.first_name_input.pack()
        last_name_label = tk.Label(window, text="Etternavn")
        last_name_label.pack()
        self.last_name_input = tk.Entry(window)
        self.last_name_input.pack()
        address_label = tk.Label(window, text="Addresse")
        address_label.pack()
        self.address_label_input = tk.Entry(window)
        self.address_label_input.pack()
        postnr_label = tk.Label(window, text="Postnummer")
        postnr_label.pack()
        self.postnr_label_input = tk.Entry(window)
        self.postnr_label_input.pack()
        poststed_label = tk.Label(window, text="Poststed")
        poststed_label.pack()
        self.poststed_input = tk.Entry(window)
        self.poststed_input.pack()
        btn_register = tk.Button(window, text="Registrer ny bruker", command=self.register_user)
        btn_register.pack()
    
    def register_user(self):
        firstname = self.first_name_input.get()
        lastname = self.last_name_input.get()
        address = self.address_label_input.get()
        postnr = self.postnr_label_input.get()
        poststed = self.postnr_label_input.get()

        # Connect to database
        connection = connect_info()

        if connection:
            try:
                # Use the return value of add_user to check if the operation was successful
                success = add_user(firstname, lastname, address, postnr, poststed)
            
                if success:
                    messagebox.showinfo("Bruker Registrert", "Brukeren er registrert!")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")

    
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

        # Calculate the total sum of order
        total_sum = 0
        for item_id in combined_tree.get_children():
            price_total = float(combined_tree.item(item_id, "values")[5])
            total_sum += price_total

        # Fetch customer information using the stored procedure
        customer_info = execute_stored_procedure("GetClientinfo", (order_id,))

        # Check if there are any results
        if customer_info:
            # Extract customer information from the result
            customer_name = f"{customer_info[0][0]} {customer_info[0][1]}"
            customer_address = f"{customer_info[0][2]}, {customer_info[0][3]}"

            # Show customer info that doesn't need repeating
            label_customer_name = tk.Label(combined_window, text=f"Navn: {customer_name} ")
            label_customer_address = tk.Label(combined_window, text=f" Addresse: {customer_address}")
            label_total_price = tk.Label(combined_window, text=f"Totalt: {total_sum} kr" )
            label_customer_name.pack(side="left")
            label_customer_address.pack(side="left")
            label_total_price.pack(side="right")
        else:
            messagebox.showwarning("Advarsel", "Kundeinfo ikke funnet!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()
