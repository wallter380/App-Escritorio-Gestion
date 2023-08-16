from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class Proveedor:
    def __init__(self, root_win):
        self.root = root_win
        self.root.geometry("1100x500+220+130")
        self.root.title("Gestion de Proveedores")
        self.root.config(bg="white")
        self.root.focus_force()
        # system variables
        self.buscarOption_var = StringVar()
        self.buscarText_var = StringVar()

        self.proveedor_nombre_var = StringVar()
        self.email_var = StringVar()
        self.detalle_var = StringVar()

        # search employee
        buscar_frame = LabelFrame(self.root, text="Buscar un proveedor", font=("Lato", 11, "normal"), bg="white", bd=2)
        buscar_frame.place(x=250, y=260, width=600, height=70)

        # search options
        buscar_label = Label(buscar_frame, text="Buscar por nombre del proveedor", font=("Lato", 11, "normal"), bg="white")
        buscar_label.place(x=10, y=10)

        buscar_box = Entry(buscar_frame, textvariable=self.buscarText_var, font=("Lato", 11, "normal"), bg="#EEE6CE")
        buscar_box.place(x=200, y=10, width=200, height=25)
        buscar_btn = Button(buscar_frame, text="Buscar", command=self.buscar_proveedor, font=("Lato", 11, "bold"), bg="#2EB086", fg="white", bd=3, cursor="hand2")
        buscar_btn.place(x=410, y=10, width=150, height=25)


        # title
        title = Label(self.root, text="Información del proveedor", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        title.place(x=50, y=20, width=1000)
        # content
        # -----first row-----
        proveedor_nombre_label = Label(self.root, text="Nombre", font=("Lato", 14, "normal"), bg="white")
        proveedor_nombre_label.place(x=50, y=70)
        proveedor_nombre_txt = Entry(self.root, textvariable=self.proveedor_nombre_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        proveedor_nombre_txt.place(x=170, y=70, width=180)

        # -----second row-----
        email_label = Label(self.root, text="Email", font=("Lato", 14, "normal"), bg="white")
        email_label.place(x=50, y=110)
        email_txt = Entry(self.root, textvariable=self.email_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        email_txt.place(x=170, y=110, width=180)

        # -----third row-----
        detalle_label = Label(self.root, text="Detalle", font=("Lato", 14, "normal"), bg="white")
        detalle_label.place(x=50, y=150)
        detalle_txt = Entry(self.root, textvariable=self.detalle_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        detalle_txt.place(x=170, y=150, width=180)

        # -----fourth row-----
        #descuento_desc = Label(self.root, text="Descuento", font=("Lato", 14, "normal"), bg="white")
        #descuento_desc.place(x=50, y=190)
        #self.desc_txt = Text(self.root, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        #self.desc_txt.place(x=170, y=190, width=300, height=60)

        # buttons
        add_btn = Button(self.root, text="Agregar", command=self.add_proveedor, font=("Lato", 11, "bold"), bg="#2EB086", fg="white", bd=3, cursor="hand2")
        add_btn.place(x=500, y=225, width=110, height=25)
        update_btn = Button(self.root, text="Modificar", command=self.update_proveedor, font=("Lato", 11, "bold"), bg="#0AA1DD", fg="white", bd=3, cursor="hand2")
        update_btn.place(x=620, y=225, width=110, height=25)
        delete_btn = Button(self.root, text="BORRAR", command=self.delete_proveedor, font=("Lato", 11, "bold"), bg="#B8405E", fg="white", bd=3, cursor="hand2")
        delete_btn.place(x=740, y=225, width=110, height=25)
        clear_btn = Button(self.root, text="Borrar", command=self.clear, font=("Lato", 11, "bold"), bg="#313552", fg="white", bd=3, cursor="hand2")
        clear_btn.place(x=860, y=225, width=110, height=25)

        # supplier list
        proveedor_list_frame = Frame(self.root, bd=3, relief=RIDGE)
        proveedor_list_frame.place(x=0, y=350, relwidth=1, height=150)

        scroll_y = Scrollbar(proveedor_list_frame, orient=VERTICAL)
        scroll_x = Scrollbar(proveedor_list_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        list_columns = ("nombre", "email", "detalle")
        self.proveedor_list_table = ttk.Treeview(proveedor_list_frame, columns=list_columns, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.proveedor_list_table.pack(fill=BOTH, expand=1)
        scroll_x.config(command=self.proveedor_list_table.xview)
        scroll_y.config(command=self.proveedor_list_table.yview)

        self.proveedor_list_table.heading("nombre", text="Nombre")
        self.proveedor_list_table.heading("email", text="Email")
        self.proveedor_list_table.heading("detalle", text="Detalle")
        self.proveedor_list_table["show"] = "headings"

        self.proveedor_list_table.column("nombre", width=100)
        self.proveedor_list_table.column("email", width=100)
        self.proveedor_list_table.column("detalle", width=100)

        self.proveedor_list_table.bind("<ButtonRelease-1>", self.get_data)

        self.show_proveedor()

    # supplier methods
    def add_proveedor(self):
        con = sqlite3.connect("DB-gestion.sql")
        cur = con.cursor()
        try:
            if self.proveedor_nombre_var.get() == "":
                messagebox.showerror("Error", "Se debe ingresar el número de factura del proveedor", parent=self.root)
            else:
                cur.execute("SELECT * FROM proveedor WHERE nombre=?", (self.proveedor_nombre_var.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Nº de factura ya existe, introduzca otro", parent=self.root)
                else:
                    values_to_insert = (self.proveedor_nombre_var.get(),
                                        self.email_var.get(),
                                        self.detalle_txt.get('1.0', END),
                                        )
                    cur.execute("INSERT INTO proveedor (nombre, email, detalle) VALUES (?,?,?)", values_to_insert)
                    con.commit()
                    messagebox.showinfo("Éxito", "Proveedor agregado con éxito", parent=self.root)
                    self.show_proveedor()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def show_proveedor(self):
        con = sqlite3.connect("DB-gestion.sql")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM proveedor")
            rows = cur.fetchall()
            self.proveedor_list_table.delete(*self.proveedor_list_table.get_children())
            for row in rows:
                self.proveedor_list_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        table_focus = self.proveedor_list_table.focus()
        table_content = (self.proveedor_list_table.item(table_focus))
        row = table_content["values"]
        # print(row)

        self.proveedor_nombre_var.set(row[0])
        self.email_var.set(row[1])
        self.detalle_txt.delete('1.0', END)
        self.detalle_txt.insert(END, row[2])

    def update_proveedor(self):
        con = sqlite3.connect("DB-gestion.sql")
        cur = con.cursor()
        try:
            if self.proveedor_nombre_var.get() == "":
                messagebox.showerror("Error", "Se debe ingresar el nombre del proveedor", parent=self.root)
            else:
                cur.execute("SELECT * FROM proveedor WHERE nombre=?", (self.proveedor_nombre_var.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Número de factura no válido", parent=self.root)
                else:
                    values_to_insert = (
                                        self.email_var.get(),
                                        self.detalle_txt.get('1.0', END),
                                        self.proveedor_nombre_var.get(),
                                        )
                    cur.execute("UPDATE proveedor set nombre=?, email=?, detalle=? where nombre=?", values_to_insert)
                    con.commit()
                    messagebox.showinfo("Éxito", "Proveedor cambiado con éxito", parent=self.root)
                    self.show_proveedor()
                    con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def delete_proveedor(self):
        con = sqlite3.connect('DB-gestion.sql')
        cur = con.cursor()
        try:
            if self.proveedor_nombre_var.get() == "":
                messagebox.showerror("Error", "Se debe ingresar el nombre del proveedor", parent=self.root)
            else:
                cur.execute("SELECT * FROM proveedor WHERE nombre=?", (self.proveedor_nombre_var.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Nombre no válido", parent=self.root)
                else:
                    user_confirm = messagebox.askyesno("Confirmación", "¿Confirmar eliminación?", parent=self.root)
                    if user_confirm:
                        cur.execute("DELETE FROM proveedor WHERE invoice=?", (self.proveedor_nombre_var.get(),))
                        con.commit()
                        messagebox.showinfo("Éxito", "Proveedor eliminado con éxito", parent=self.root)
                        self.show_proveedor()
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def clear(self):
        self.proveedor_nombre_var.set("")
        self.email_var.set("")
        self.detalle_txt.delete('1.0', END)
        self.buscarText_var.set("")
        self.show_proveedor()

    def buscar_proveedor(self):
        con = sqlite3.connect('DB-gestion.sql')
        cur = con.cursor()
        try:
            if self.buscarText_var.get() == "":
                messagebox.showerror("Error", "Campo de búsqueda vacío", parent=self.root)
            else:
                cur.execute("SELECT * FROM proveedor WHERE nombre=?", (self.buscarText_var.get(),))
                row = cur.fetchone()
                if row is not None:
                    self.proveedor_list_table.delete(*self.proveedor_list_table.get_children())
                    self.proveedor_list_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "¡No se encontró ningún proveedor!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    system = Proveedor(root)
    root.mainloop()
