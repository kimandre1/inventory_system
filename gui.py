import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from database import connect_info, execute_stored_procedure
from billing import create_pdf

class SimpleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Lager og Logistikk System (LOLS)")


        # Create Treeviews
        self.vareliste_tree = ttk.Treeview(self.master, columns=("Varenummer", "Betegnelse", "Pris", "Antall"), show="headings")
        self.configure_treeview(self.vareliste_tree, ("Varenummer", "Betegnelse", "Pris", "Antall"))

        self.vis_ordre_tree = ttk.Treeview(self.master, columns=("Ordrenummer", "Bestillingsdato", "Sendt", "Betalt", "Kundenummer"), show="headings")
        self.configure_treeview(self.vis_ordre_tree, ("Ordrenummer", "Bestillingsdato", "Sendt", "Betalt", "Kundenummer"))

        self.kundeliste_tree = ttk.Treeview(self.master, columns=("Kundenummer", "Fornavn", "Etternavn", "Addresse", "Postnummer"), show="headings")
        self.configure_treeview(self.kundeliste_tree, ("Kundenummer", "Fornavn", "Etternavn", "Addresse", "Postnummer"))

        # Create buttons
        self.btn_kundeliste = ctk.CTkButton(master, text="Kundeliste", command=lambda: self.display_grid("GetKundeInfo", self.kundeliste_tree))
        self.btn_vareliste = ctk.CTkButton(master, text="Vareliste", command=lambda: self.display_grid("GetVareinfo", self.vareliste_tree))
        self.btn_vis_ordre = ctk.CTkButton(master, text="Ordreliste", command=lambda: self.display_grid("GetOrdreinfo", self.vis_ordre_tree))
        self.btn_addkunde = ctk.CTkButton(master, text="Legg til ny kunde", command=self.add_user_form)
        self.btn_context = None
        self.btn_lag_faktura = None

        # Grid layout for buttons
        self.btn_kundeliste.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.btn_addkunde.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.btn_vareliste.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        self.btn_vis_ordre.grid(row=0, column=4, padx=10, pady=10, sticky="w")

        # Initially hide the Treeviews
        self.vareliste_tree.grid_forget()
        self.vis_ordre_tree.grid_forget()
        self.kundeliste_tree.grid_forget()

    def configure_treeview(self, tree, columns):
        for column in columns:
            tree.heading(column, text=column)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)

    def display_grid(self, procedure, tree):
        # Hide treeviews and buttons
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
                    tree.grid(row=1, column=1, columnspan=6, padx=10, pady=10)
                    
                    #Show extra buttons depending on the method
                    if procedure == "GetOrdreinfo":
                        self.button_context(self, "Inspiser Ordre", self.inspect_order, procedure)
                    
                    elif procedure == "GetKundeInfo":
                        self.button_context(self, "Slett Kunde", self.delete_client, procedure)

                    elif procedure not in "GetOrdreinfo" or "GetKundeInfo":
                        self.button_context(self, "empty", "empty", procedure)
                        self.btn_context.grid_forget()       
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
    
    def button_context(btn_context, self, buttontext, method, procedure):
        self.btn_context = ctk.CTkButton(self.master, text=buttontext, command=method)
        self.btn_context.grid(row=2, column=5, padx=10, pady=10, sticky="w")

    def add_user_form(self):
        self.window = tk.Toplevel(self.master)
        self.window.title("Legg til bruker")
        first_name_label = tk.Label(self.window, text="Fornavn")
        first_name_label.pack()
        self.first_name_input = tk.Entry(self.window)
        self.first_name_input.pack()
        last_name_label = tk.Label(self.window, text="Etternavn")
        last_name_label.pack()
        self.last_name_input = tk.Entry(self.window)
        self.last_name_input.pack()
        address_label = tk.Label(self.window, text="Addresse")
        address_label.pack()
        self.address_label_input = tk.Entry(self.window)
        self.address_label_input.pack()
        postnr_label = tk.Label(self.window, text="Postnummer")
        postnr_label.pack()
        self.postnr_label_input = tk.Entry(self.window)
        self.postnr_label_input.pack()
        poststed_label = tk.Label(self.window, text="Poststed")
        poststed_label.pack()
        self.poststed_input = tk.Entry(self.window)
        self.poststed_input.pack()
        btn_register = tk.Button(self.window, text="Registrer ny bruker", command=self.register_user)
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
                execute_stored_procedure("AddUser", (firstname, lastname, address, postnr, poststed))
           
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")

            finally:
                self.window.destroy()
                messagebox.showinfo("Bruker Registrert", "Brukeren er registrert!")
                self.display_grid("GetKundeInfo", self.kundeliste_tree)
    def delete_client(self):
        #Check row selection
        selected_client = self.kundeliste_tree.selection()

        if not selected_client:
            messagebox.showinfo("Informasjon", "Velg en kunde først")
            return
        
        client_value = self.kundeliste_tree.item(selected_client)['values']
        client_id = client_value[0]

        # Call stored procedure
        connection = connect_info()

        if connection:
            try:
                # Call stored procedure using client id
                execute_stored_procedure("DeleteClient", (client_id,))
                messagebox.showinfo("Kunde slettet", f"Kunde med Kundenummer: {client_id} er slettet.")
                self.display_grid("GetKundeInfo", self.kundeliste_tree)

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


            #Add billing button
            self.btn_lag_faktura = ctk.CTkButton(combined_window, text="Lag Faktura", command=lambda: self.lag_faktura(order_id))
            self.btn_lag_faktura.pack(side="right")
            label_total_price.pack(side="right")
        else:
            messagebox.showwarning("Advarsel", "Kundeinfo ikke funnet!")
    
    def lag_faktura(self, order_id):
        # Called stored procedure using order id
        connection = connect_info()

        if connection:
            try:
                # Call the stored procedure
                results_inspect_order = execute_stored_procedure("InspectOrder", (order_id,))

                # Fetch customer information using the stored procedure
                customer_info = execute_stored_procedure("GetClientinfo", (order_id,))

                # Calculate the total sum of order
                total_sum = sum(float(row[5]) for row in results_inspect_order)

                if customer_info:
                    create_pdf(order_id, results_inspect_order, customer_info, total_sum)
                else:
                    messagebox.showwarning("Advarsel", "Kundeinfo ikke funnet!")

            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()