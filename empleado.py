from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class Empleado:
    def __init__(self, root_win):
        self.root = root_win
        self.root.geometry("1200x500+220+130")
        self.root.title("Gestion de Empleados")
        self.root.config(bg="white")
        self.root.focus_force()
        # system variables
        self.buscarOption_var = StringVar()
        self.buscarText_var = StringVar()

        self.nombre_var = StringVar()
        self.contacto_var = StringVar()
        self.genero_var = StringVar()
        self.fn_var = StringVar()
        self.fi_var = StringVar()
        self.email_var = StringVar()
        self.contraseña_var = StringVar()
        self.salario_var = StringVar()

        # title
        title = Label(self.root, text="Informacion del empleado", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        title.place(x=50, y=20, width=1200)
        # content
        # -----first row-----


        genero_label = Label(self.root, text="Sexo", font=("Lato", 14, "normal"), bg="white")
        genero_label.place(x=380, y=70)

        contacto_label = Label(self.root, text="Contacto", font=("Lato", 14, "normal"), bg="white")
        contacto_label.place(x=750, y=70)


        genero_opt = ttk.Combobox(self.root, textvariable=self.genero_var, values=("Seleccionar", "Masculino", "Femenino"), state="readonly", justify=CENTER, font=("Lato", 14, "normal"))
        genero_opt.place(x=500, y=70, width=180)
        genero_opt.current(0)
        contacto_txt = Entry(self.root, textvariable=self.contacto_var, font=("Lato", 14, "normal"), bd=1, bg="#EEE6CE")
        contacto_txt.place(x=850, y=70, width=180)

        # -----second row-----
        nombre_label = Label(self.root, text="Nombre", font=("Lato", 14, "normal"), bg="white")
        nombre_label.place(x=50, y=110)
        fn_label = Label(self.root, text="Fecha de Nacimiento", font=("Lato", 14, "normal"), bg="white")
        fn_label.place(x=350, y=110)
        fi_label = Label(self.root, text="Fecha de ingreso", font=("Lato", 14, "normal"), bg="white")
        fi_label.place(x=750, y=110)

        nombre_txt = Entry(self.root, textvariable=self.nombre_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        nombre_txt.place(x=150, y=110, width=180)
        fn_txt = Entry(self.root, textvariable=self.fn_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        fn_txt.place(x=550, y=110, width=180)
        fi_txt = Entry(self.root, textvariable=self.fi_var, font=("Lato", 14, "normal"), bd=1, bg="#EEE6CE")
        fi_txt.place(x=915, y=110, width=180)

        # -----third row-----
        email_label = Label(self.root, text="Email", font=("Lato", 14, "normal"), bg="white")
        email_label.place(x=50, y=150)
        contraseña_label = Label(self.root, text="Contraseña", font=("Lato", 14, "normal"), bg="white")
        contraseña_label.place(x=350, y=150)

        email_txt = Entry(self.root, textvariable=self.email_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        email_txt.place(x=150, y=150, width=180)
        contraseña_txt = Entry(self.root, textvariable=self.contraseña_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        contraseña_txt.place(x=500, y=150, width=180)

        # -----fourth row-----
        direccion_label = Label(self.root, text="Direccion", font=("Lato", 14, "normal"), bg="white")
        direccion_label.place(x=50, y=190)
        salario_label = Label(self.root, text="Salario", font=("Lato", 14, "normal"), bg="white")
        salario_label.place(x=500, y=190)

        self.direccion_txt = Text(self.root, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        self.direccion_txt.place(x=150, y=190, width=300, height=60)
        salario_txt = Entry(self.root, textvariable=self.salario_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        salario_txt.place(x=600, y=190, width=180)
        # buttons
        agregar_btn = Button(self.root, text="Agregar", command=self.add_emp, font=("Lato", 11, "bold"), bg="#2EB086", fg="white", bd=3, cursor="hand2")
        agregar_btn.place(x=500, y=225, width=110, height=25)
        modificar_btn = Button(self.root, text="Modificar", command=self.update_emp, font=("Lato", 11, "bold"), bg="#0AA1DD", fg="white", bd=3, cursor="hand2")
        modificar_btn.place(x=620, y=225, width=110, height=25)
        borrar_btn = Button(self.root, text="Suprimir", command=self.delete_emp, font=("Lato", 11, "bold"), bg="#B8405E", fg="white", bd=3, cursor="hand2")
        borrar_btn.place(x=740, y=225, width=110, height=25)
        limpiar_btn = Button(self.root, text="Limpiar", command=self.clear, font=("Lato", 11, "bold"), bg="#313552", fg="white", bd=3, cursor="hand2")
        limpiar_btn.place(x=860, y=225, width=110, height=25)

        # search employee
        buscar_frame = LabelFrame(self.root, text="Buscar Empleado", font=("Lato", 11, "normal"), bg="white", bd=2)
        buscar_frame.place(x=250, y=260, width=600, height=70)

        # search options
        opcion_box = ttk.Combobox(buscar_frame, textvariable=self.buscarOption_var, values=("Seleccionar", "ID", "Email", "Nombre", "Contacto"), state="readonly", justify=CENTER, font=("Lato", 11, "normal"))
        opcion_box.place(x=10, y=10, width=180)
        opcion_box.current(0)

        buscar_box = Entry(buscar_frame, textvariable=self.buscarText_var, font=("Lato", 11, "normal"), bg="#EEE6CE")
        buscar_box.place(x=200, y=10, width=200, height=25)
        buscar_btn = Button(buscar_frame, text="Buscar", command=self.buscar_emp, font=("Lato", 11, "bold"), bg="#2EB086", fg="white", bd=3, cursor="hand2")
        buscar_btn.place(x=410, y=10, width=150, height=25)

        # employees list
        emp_list_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_list_frame.place(x=0, y=350, relwidth=1, height=150)

        scroll_y = Scrollbar(emp_list_frame, orient=VERTICAL)
        scroll_x = Scrollbar(emp_list_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        list_columns = ("id", "nombre", "email", "sexo", "contacto", "fecha.nacimiento", "fecha.ingreso", "contraseña", "direccion", "salario")
        self.emp_list_table = ttk.Treeview(emp_list_frame, columns=list_columns, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.emp_list_table.pack(fill=BOTH, expand=1)
        scroll_x.config(command=self.emp_list_table.xview)
        scroll_y.config(command=self.emp_list_table.yview)

        self.emp_list_table.heading("id", text="ID")
        self.emp_list_table.heading("nombre", text="Nombre")
        self.emp_list_table.heading("email", text="Email")
        self.emp_list_table.heading("sexo", text="Sexo")
        self.emp_list_table.heading("contacto", text="Contacto")
        self.emp_list_table.heading("fecha.nacimiento", text="Fecha Nacimiento")
        self.emp_list_table.heading("fecha.ingreso", text="Fecha Ingreso")
        self.emp_list_table.heading("contraseña", text="Contraseña")
        self.emp_list_table.heading("direccion", text="Direccion")
        self.emp_list_table.heading("salario", text="Salario")
        self.emp_list_table["show"] = "headings"

        self.emp_list_table.column("id", width=100)
        self.emp_list_table.column("nombre", width=100)
        self.emp_list_table.column("email", width=100)
        self.emp_list_table.column("sexo", width=100)
        self.emp_list_table.column("contacto", width=100)
        self.emp_list_table.column("fecha.nacimiento", width=100)
        self.emp_list_table.column("fecha.ingreso", width=100)
        self.emp_list_table.column("contraseña", width=100)
        self.emp_list_table.column("direccion", width=100)
        self.emp_list_table.column("salario", width=100)

        self.emp_list_table.bind("<ButtonRelease-1>", self.get_data)

        self.show_emp()

    # employee methods
    def add_emp(self):
        con = sqlite3.connect("DB-gestion.sql")
        cur = con.cursor()
        try:
            if self.nombre_var.get() == "":
                messagebox.showerror("Error", "Se debe ingresar el nombre del empleado", parent=self.root)
            else:
                cur.execute("SELECT * FROM empleado WHERE nombre=?", (self.nombre_var.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Empleado ya existe, ingrese otro", parent=self.root)
                else:
                    values_to_insert = (self.nombre_var.get(),
                                        self.email_var.get(),
                                        self.genero_var.get(),
                                        self.contacto_var.get(),
                                        self.fn_var.get(),
                                        self.fi_var.get(),
                                        self.contraseña_var.get(),
                                        self.direccion_txt.get('1.0', END),
                                        self.salario_var.get()
                                        )
                    cur.execute("INSERT INTO empleado (nombre, email, genero, contacto, fn, fi, contraseña, direccion, salario) VALUES (?,?,?,?,?,?,?,?,?)", values_to_insert)
                    con.commit()
                    messagebox.showinfo("Exito", "El empleado se agrego con exito", parent=self.root)
                    self.show_emp()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def show_emp(self):
        con = sqlite3.connect("DB-gestion.sql")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM empleado")
            rows = cur.fetchall()
            self.emp_list_table.delete(*self.emp_list_table.get_children())
            for row in rows:
                self.emp_list_table.insert('', END,values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        table_focus = self.emp_list_table.focus()
        table_content = (self.emp_list_table.item(table_focus))
        row = table_content["values"]
        print(row)

        self.ID_var.set(row[0])
        self.nombre_var.set(row[1])
        self.email_var.set(row[2])
        self.genero_var.set(row[3])
        self.contacto_var.set(row[4])
        self.fn_var.set(row[5])
        self.fi_var.set(row[6])
        self.contraseña_var.set(row[7])
        self.direccion_txt.delete('1.0', END)
        self.direccion_txt.insert(END, row[8])
        self.salario_var.set(row[9])

    def update_emp(self):
        con = sqlite3.connect("DB-gestion.sql")
        cur = con.cursor()
        try:
            if self.nombre_var.get() == "":
                messagebox.showerror("Error", "Se debe ingresar la identificación del empleado", parent=self.root)
            else:
                cur.execute("SELECT * FROM empleado WHERE nombre=?", (self.nombre_var.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Identificacion de empleado no valida", parent=self.root)
                else:
                    values_to_insert = (
                                        self.nombre_var.get(),
                                        self.email_var.get(),
                                        self.genero_var.get(),
                                        self.contacto_var.get(),
                                        self.fn_var.get(),
                                        self.fi_var.get(),
                                        self.contraseña_var.get(),
                                        self.direccion_txt.get('1.0', END),
                                        self.salario_var.get()
                                        )
                    cur.execute("UPDATE empleado set nombre=?, email=?, genero=?, contacto=?, fn=?, fi=?, contraseña=?, direccion=?, salario=? where nombre=?", values_to_insert)
                    con.commit()
                    messagebox.showinfo("Éxito", "El empleado se cambió con éxito", parent=self.root)
                    self.show_emp()
                    con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def delete_emp(self):
        con = sqlite3.connect('DB-gestion.sql')
        cur = con.cursor()
        try:
            if self.nombre_var.get() == "":
                messagebox.showerror("Error", "Se debe ingresar la identificación del empleado", parent=self.root)
            else:
                cur.execute("SELECT * FROM empleado WHERE nombre=?", (self.nombre_var.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Identificacion de empleado no valida", parent=self.root)
                else:
                    user_confirm = messagebox.askyesno("Confirmación", "¿Confirmar eliminación?", parent=self.root)
                    if user_confirm:
                        cur.execute("DELETE FROM empleado WHERE nombre=?", (self.nombre_var.get(),))
                        con.commit()
                        messagebox.showinfo("Éxito", "El empleado se eliminó con éxito", parent=self.root)
                        self.show_emp()
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def clear(self):
        self.nombre_var.set("")
        self.email_var.set("")
        self.genero_var.set("Select")
        self.contacto_var.set("")
        self.fn_var.set("")
        self.fi_var.set("")
        self.contraseña_var.set("")
        self.direccion_txt.delete('1.0', END)
        self.salario_var.set("")
        self.buscarText_var.set("")
        self.buscarOption_var.set("Seleccionar")
        self.show_emp()

    def buscar_emp(self):
        con = sqlite3.connect('DB-gestion.sql')
        cur = con.cursor()
        try:
            if self.buscarOption_var.get() == "Seleccionar":
                messagebox.showerror("Error", "Seleccionar opción de búsqueda", parent=self.root)
            elif self.buscarText_var.get() == "":
                messagebox.showerror("Error", "Campo de búsqueda vacío", parent=self.root)
            else:
                if self.buscarOption_var.get() == "Nombre":
                    self.buscarOption_var.set("nombre")
                cur.execute("SELECT * FROM empleado WHERE " + self.buscarOption_var.get() + " LIKE '%" + self.buscarText_var.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.emp_list_table.delete(*self.emp_list_table.get_children())
                    for row in rows:
                        self.emp_list_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "¡No se encontraron empleados!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)



if __name__ == "__main__":
    root = Tk()
    system = Empleado(root)
    root.mainloop()
