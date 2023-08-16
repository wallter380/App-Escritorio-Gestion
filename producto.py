from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class Producto:
    def __init__(self, root_win):
        self.prod_ID_var = None
        self.root = root_win
        self.root.geometry("1100x500+220+130")
        self.root.title("Gestion de Productos")
        self.root.config(bg="white")
        self.root.focus_force()

        # system variables
        self.buscarOption_var = StringVar()
        self.buscarText_var = StringVar()

        self.prod_id_var = StringVar()
        self.categ_var = StringVar()
        self.proveedor_var = StringVar()
        self.categ_list = []
        self.proveedor_list = []
        self.get_categ_proveedor()
        self.producto_list = []
        self.nombre_var = StringVar()
        self.precio_var = StringVar()
        self.cantidad_var = StringVar()
        self.estado_var = StringVar()

        producto_frame = Frame(self.root, bd=1, bg="white")
        producto_frame.place(x=10, y=10, width=500, height=480)

        title = Label(producto_frame, text="Informacion de Producto", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        title.pack(side=TOP, fill=X)

        # labels
        categ_label = Label(producto_frame, text="Categoria", font=("Lato", 14, "normal"), bg="white")
        categ_label.place(x=30, y=60)
        proveedor_label = Label(producto_frame, text="Proveedor", font=("Lato", 14, "normal"), bg="white")
        proveedor_label.place(x=30, y=110)
        nombre_label = Label(producto_frame, text="Nombre", font=("Lato", 14, "normal"), bg="white")
        nombre_label.place(x=30, y=160)
        precio_label = Label(producto_frame, text="Precio", font=("Lato", 14, "normal"), bg="white")
        precio_label.place(x=30, y=210)
        cantidad_label = Label(producto_frame, text="Cantidad", font=("Lato", 14, "normal"), bg="white")
        cantidad_label.place(x=30, y=260)
        estado_label = Label(producto_frame, text="Estado", font=("Lato", 14, "normal"), bg="white")
        estado_label.place(x=30, y=310)

        # inputs

        # category select
        categ_select = ttk.Combobox(self.root, textvariable=self.categ_var, values=self.categ_list, state="readonly", justify=CENTER, font=("Lato", 14, "normal"))
        categ_select.place(x=190, y=70, width=200)
        categ_select.current(0)
        # supplier select
        proveedor_select = ttk.Combobox(self.root, textvariable=self.proveedor_var, values=self.proveedor_list, state="readonly", justify=CENTER, font=("Lato", 14, "normal"))
        proveedor_select.place(x=190, y=120, width=200)
        proveedor_select.current(0)

        nombre_txt = Entry(producto_frame, textvariable=self.nombre_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        nombre_txt.place(x=180, y=160, width=200)
        precio_txt = Entry(producto_frame, textvariable=self.precio_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        precio_txt.place(x=180, y=210, width=200)
        cantidad_txt = Entry(producto_frame, textvariable=self.cantidad_var, font=("Lato", 14, "normal"), bg="#EEE6CE", bd=1)
        cantidad_txt.place(x=180, y=260, width=200)

        status_select = ttk.Combobox(self.root, textvariable=self.estado_var, values=("activo", "inactivo"), state="readonly", justify=CENTER, font=("Lato", 14, "normal"))
        status_select.place(x=190, y=320, width=200)
        status_select.current(0)

        # buttons
        add_btn = Button(producto_frame, text="Agregar", command=self.add_producto, font=("Lato", 11, "bold"), bg="#2EB086", fg="white", bd=3, cursor="hand2")
        add_btn.place(x=10, y=400, width=110, height=25)
        update_btn = Button(producto_frame, text="Modificar", command=self.update_producto, font=("Lato", 11, "bold"), bg="#0AA1DD", fg="white", bd=3, cursor="hand2")
        update_btn.place(x=130, y=400, width=110, height=25)
        delete_btn = Button(producto_frame, text="Borrar", command=self.delete_producto, font=("Lato", 11, "bold"), bg="#B8405E", fg="white", bd=3, cursor="hand2")
        delete_btn.place(x=250, y=400, width=110, height=25)
        clear_btn = Button(producto_frame, text="Borrar", command=self.clear, font=("Lato", 11, "bold"), bg="#313552", fg="white", bd=3, cursor="hand2")
        clear_btn.place(x=370, y=400, width=110, height=25)

        # search employee
        buscar_frame = LabelFrame(self.root, text="Buscar un producto", font=("Lato", 11, "normal"), bg="white", bd=2)
        buscar_frame.place(x=520, y=10, width=465, height=70)

        # search options
        options_box = ttk.Combobox(buscar_frame, textvariable=self.buscarOption_var, values=("Seleccionar", "Categoria", "Proveedor", "Nombre"), state="readonly", justify=CENTER, font=("Lato", 11, "normal"))
        options_box.place(x=10, y=10, width=150)
        options_box.current(0)

        buscar_box = Entry(buscar_frame, textvariable=self.buscarText_var, font=("Lato", 11, "normal"), bg="#EEE6CE")
        buscar_box.place(x=170, y=10, width=170, height=25)
        buscar_btn = Button(buscar_frame, text="Buscar", command=self.buscar_producto, font=("Lato", 11, "bold"), bg="#2EB086", fg="white", bd=3, cursor="hand2")
        buscar_btn.place(x=350, y=10, width=100, height=25)

        # Products list
        producto_list_frame = Frame(self.root, bd=3, relief=RIDGE)
        producto_list_frame.place(x=520, y=90, width=560, height=390)

        scroll_y = Scrollbar(producto_list_frame, orient=VERTICAL)
        scroll_x = Scrollbar(producto_list_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        list_columns = ("id", "Categoria", "Proveedor", "Nombre", "Precio", "Cantidad", "Estado")
        self.producto_list_table = ttk.Treeview(producto_list_frame, columns=list_columns, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.producto_list_table.pack(fill=BOTH, expand=1)
        scroll_x.config(command=self.producto_list_table.xview)
        scroll_y.config(command=self.producto_list_table.yview)

        self.producto_list_table.heading("id", text="ID")
        self.producto_list_table.heading("Categoria", text="Categoria")
        self.producto_list_table.heading("Proveedor", text="Proveedor")
        self.producto_list_table.heading("Nombre", text="Nombre")
        self.producto_list_table.heading("Precio", text="Precio")
        self.producto_list_table.heading("Cantidad", text="Cantidad")
        self.producto_list_table.heading("Estado", text="Estado")
        self.producto_list_table["show"] = "headings"

        self.producto_list_table.column("id", width=90)
        self.producto_list_table.column("Categoria", width=100)
        self.producto_list_table.column("Proveedor", width=100)
        self.producto_list_table.column("Nombre", width=100)
        self.producto_list_table.column("Precio", width=100)
        self.producto_list_table.column("Cantidad", width=100)
        self.producto_list_table.column("Estado", width=100)

        self.producto_list_table.bind("<ButtonRelease-1>", self.get_data)

        self.show_producto()

        # product methods
    def get_categ_proveedor(self):
        self.categ_list.append("Vacio")
        self.proveedor_list.append("Vacio")
        con = sqlite3.connect("DB-gestion.sql")
        cur = con.cursor()
        try:
            cur.execute("SELECT nombre FROM categoria")
            categs = cur.fetchall()

            if len(categs) > 0:
                del self.categ_list[:]
                self.categ_list.append("Select")
                for item in categs:
                    self.categ_list.append(item[0])

            cur.execute("SELECT nombre FROM proveedor")
            suppls = cur.fetchall()

            if len(suppls) > 0:
                del self.proveedor_list[:]
                self.proveedor_list.append("Select")
                for item in suppls:
                    self.proveedor_list.append(item[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def add_producto(self):
        con = sqlite3.connect("DB-gestion.sql")
        cur = con.cursor()
        try:
            if self.categ_var.get() == "Vacío" or self.proveedor_var.get() == "Vacío" :
                messagebox.showerror("Error", "Debes rellenar categorías y proveedores primero", parent=self.root)
            elif self.categ_var.get() == "Select" or self.proveedor_var.get() == "Select" or self.nombre_var.get() == "":
                messagebox.showerror("Error", "Los campos Categoría, Proveedor y Nombre son obligatorios", parent=self.root)
            else:
                cur.execute("SELECT * FROM producto WHERE nombre=?", (self.nombre_var.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "El producto ya existe", parent=self.root)
                else:
                    values_to_insert = (self.categ_var.get(),
                                        self.proveedor_var.get(),
                                        self.nombre_var.get(),
                                        self.precio_var.get(),
                                        self.cantidad_var.get(),
                                        self.estado_var.get(),
                                        )
                    cur.execute("INSERT INTO producto (categoria, proveedor, nombre, precio, cantidad, estado) VALUES (?,?,?,?,?,?)", values_to_insert)
                    con.commit()
                    messagebox.showinfo("Éxito", "Producto agregado con éxito", parent=self.root)
                    self.show_producto()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def update_producto(self):
        con = sqlite3.connect("DB-gestion.sql")
        cur = con.cursor()
        try:
            if self.prod_ID_var.get() == "":
                messagebox.showerror("Error", "Debe seleccionar un producto de la lista", parent=self.root)
            else:
                cur.execute("SELECT * FROM producto WHERE ID=?", (self.prod_ID_var.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "ID de producto no válido", parent=self.root)
                else:
                    values_to_insert = (
                                        self.categ_var.get(),
                                        self.proveedor_var.get(),
                                        self.nombre_var.get(),
                                        self.precio_var.get(),
                                        self.cantidad_var.get(),
                                        self.estado_var.get(),
                                        self.prod_ID_var.get()
                                        )
                    cur.execute("UPDATE producto set categoria=?, proveedor=?, nombre=?, precio=?, cantidad=?, estado=? WHERE ID=?", values_to_insert)
                    con.commit()
                    messagebox.showinfo("Éxito", "Producto modificado con éxito", parent=self.root)
                    self.show_producto()
                    con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def delete_producto(self):
        con = sqlite3.connect('DB-gestion.sql')
        cur = con.cursor()
        try:
            if self.prod_id_var.get() == "":
                messagebox.showerror("Error", "Debe seleccionar un producto de la lista", parent=self.root)
            else:
                cur.execute("SELECT * FROM producto WHERE ID=?", (self.prod_ID_var.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "ID de producto no válido", parent=self.root)
                else:
                    user_confirm = messagebox.askyesno("Confirmación", "¿Confirmar eliminación?", parent=self.root)
                    if user_confirm:
                        cur.execute("DELETE FROM producto WHERE ID=?", (self.prod_ID_var.get(),))
                        con.commit()
                        messagebox.showinfo("Éxito", "Producto eliminado con éxito", parent=self.root)
                        self.show_producto()
                        # self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def show_producto(self):
        con = sqlite3.connect("DB-gestion.sql")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM producto")
            rows = cur.fetchall()
            self.producto_list_table.delete(*self.producto_list_table.get_children())
            for row in rows:
                self.producto_list_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def buscar_producto(self):
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
                elif self.buscarOption_var.get() == "Categoria":
                    self.buscarOption_var.set("categoria")
                elif self.buscarOption_var.get() == "Proveedor":
                    self.buscarOption_var.set("proveedor")
                cur.execute("SELECT * FROM producto WHERE " + self.buscarOption_var.get() + " LIKE '%" + self.buscarText_var.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0 :
                    self.producto_list_table.delete(*self.producto_list_table.get_children())
                    for row in rows:
                        self.producto_list_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "¡No se encontró ningún producto!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)


    def get_data(self, ev):
        table_focus = self.producto_list_table.focus()
        table_content = (self.producto_list_table.item(table_focus))
        row = table_content["values"]
        print(row)

        self.prod_ID_var.set(row[0])
        self.categ_var.set(row[1])
        self.proveedor_var.set(row[2])
        self.nombre_var.set(row[3])
        self.precio_var.set(row[4])
        self.cantidad_var.set(row[5])
        self.estado_var.set(row[6])

    def clear(self):
        self.prod_ID_var.set("")
        self.categ_var.set("Select")
        self.proveedor_var.set("Select")
        self.nombre_var.set("")
        self.precio_var.set("")
        self.cantidad_var.set("")
        self.estado_var.set("")
        self.show_producto()


if __name__ == "__main__":
    root = Tk()
    system = Producto(root)
    root.mainloop()
