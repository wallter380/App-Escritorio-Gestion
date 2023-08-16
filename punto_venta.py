from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import time
import os

class POS:
    def __init__(self, root_win):
        self.root = root_win
        self.root.geometry("1350x700+0+0")
        self.root.title("Sistema de gestión de Stock")
        self.root.config(bg="white")

        # screen Title
        title = Label(self.root, text="Punto de venta", font=("Lato", 26, "bold"), bg="white", fg="#343A40", anchor="w", padx=20) # may add anchor here to center left
        title.place(x=10, y=0, relwidth=1, height=70)

        # logout button
        logout_btn = Button(self.root, text="desconectar", command=self.logout, font=("Lato", 11, "bold"), bd=0, bg="#F66B0E", fg="white")
        logout_btn.place(x=1180, y=10, height=40, width=120)

        # product Frame ----------------------------------

        # produt search variable
        self.buscar_var = StringVar()

        producto_frame = Frame(self.root, bd=1, relief=RIDGE, bg="white")
        producto_frame.place(x=10, y=110, width=410, height=550)

        producto_title = Label(producto_frame, text="Sección de productos", font=("Lato", 14, "normal"),  bg="#2EB086", fg="white")
        producto_title.pack(side=TOP, fill=X)

        producto_buscar_frame = Frame(producto_frame, bd=1, relief=RIDGE, bg="white")
        producto_buscar_frame.place(x=2, y=36, width=399, height=90)

        buscar_label = Label(producto_buscar_frame, text="Búsqueda de Producto", font=("Lato", 14, "normal"), bg="white", fg="#2EB086")
        buscar_label.place(x=2, y=5)
        pd_nombre_label = Label(producto_buscar_frame, text="Nombre del producto", font=("Lato", 13, "normal"), bg="white")
        pd_nombre_label.place(x=2, y=40)
        pd_nombre_txt = Entry(producto_buscar_frame, textvariable=self.buscar_var, font=("Lato", 13, "normal"), bg="#EEE6CE")
        pd_nombre_txt.place(x=125, y=40, width=150, height=22)
        buscar_btn = Button(producto_buscar_frame, text="Buscar", command=self.buscar_producto, font=("Lato", 13, "normal"), bg="#2EB086", fg="white")
        buscar_btn.place(x=280, y=40, width=110, height=22)
        show_all_btn = Button(producto_buscar_frame, text="Mostrar todo", command=self.show_producto, font=("Lato", 13, "normal"), bg="#313552",fg="white")
        show_all_btn.place(x=280, y=65, width=110, height=22)

        # product list
        producto_list_frame = Frame(producto_frame, bd=3, relief=RIDGE)
        producto_list_frame.place(x=2, y=130, width=399, height=385)

        scroll_y = Scrollbar(producto_list_frame, orient=VERTICAL)
        scroll_x = Scrollbar(producto_list_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        list_columns = ("id", "nombre", "precio", "cantidad", "estado")
        self.producto_list_table = ttk.Treeview(producto_list_frame, columns=list_columns, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.producto_list_table.pack(fill=BOTH, expand=1)
        scroll_x.config(command=self.producto_list_table.xview)
        scroll_y.config(command=self.producto_list_table.yview)

        self.producto_list_table.heading("id", text="ID")
        self.producto_list_table.heading("nombre", text="Nombre")
        self.producto_list_table.heading("precio", text="Precio")
        self.producto_list_table.heading("cantidad", text="Cantidad")
        self.producto_list_table.heading("estado", text="Estado")

        self.producto_list_table["show"] = "headings"

        self.producto_list_table.column("id", width=40)
        self.producto_list_table.column("nombre", width=100)
        self.producto_list_table.column("precio", width=80)
        self.producto_list_table.column("cantidad", width=100)
        self.producto_list_table.column("estado", width=50)
        self.producto_list_table.bind("<ButtonRelease-1>", self.get_data)

        note_label = Label(producto_frame, text="Nota: Introduzca 0 para eliminar el producto de la cesta", font=("Lato", 12, "normal"), fg="#B22727", bg="white")
        note_label.pack(side=BOTTOM, fill=X)

        # customer frame

        # variables customer
        self.cust_nombre_var = StringVar()
        self.cust_contacto_var = StringVar()
        customer_frame = Frame(self.root, bd=3, relief=RIDGE, background="white")
        customer_frame.place(x=420, y=110, width=530, height=70)

        cust_title = Label(customer_frame, text="Informacion del cliente", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        cust_title.pack(side=TOP, fill=X)

        cust_nombre_label = Label(customer_frame, text="Nombre", font=("Lato", 14, "normal"), bg="white")
        cust_nombre_label.place(x=5, y=35)
        cust_nombre_txt = Entry(customer_frame, textvariable=self.cust_nombre_var, font=("Lato", 14, "normal"), bg="#EEE6CE")
        cust_nombre_txt.place(x=80, y=35, width=180)

        cust_contacto_label = Label(customer_frame, text="Contacto No.", font=("Lato", 14, "normal"), bg="white")
        cust_contacto_label.place(x=270, y=35)
        cust_contacto_txt = Entry(customer_frame, textvariable=self.cust_contacto_var, font=("Lato", 14, "normal"), bg="#EEE6CE")
        cust_contacto_txt.place(x=380, y=35, width=140)

        # cart frame ---------------------------------------
        self.cart_list = []

        cal_cart_frame = Frame(self.root, bd=2, relief=RIDGE)
        cal_cart_frame.place(x=420, y=190, width=530, height=360)

        cart_frame = Frame(cal_cart_frame, bd=2, relief=RIDGE)
        cart_frame.place(x=2, y=3, relwidth=1, height=340)
        self.cart_title = Label(cart_frame, text="Carrito   | \tTotal de Productos:  0 ", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        self.cart_title.pack(side=TOP, fill=X)

        scroll_y = Scrollbar(cart_frame, orient=VERTICAL)
        scroll_x = Scrollbar(cart_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        list_columns_cart = ("id", "nombre", "precio", "cantidad", "stock")
        self.cart_list_table = ttk.Treeview(cart_frame, columns=list_columns_cart, yscrollcommand=scroll_y.set,
                                            xscrollcommand=scroll_x.set)
        self.cart_list_table.pack(fill=BOTH, expand=1)
        scroll_x.config(command=self.cart_list_table.xview)
        scroll_y.config(command=self.cart_list_table.yview)

        self.cart_list_table.heading("id", text="ID")
        self.cart_list_table.heading("nombre", text="Nombre")
        self.cart_list_table.heading("precio", text="Precio")
        self.cart_list_table.heading("cantidad", text="Cantidad")
        self.cart_list_table.heading("stock", text="Stock")
        self.cart_list_table["show"] = "headings"

        self.cart_list_table.column("ID", width=90)
        self.cart_list_table.column("nombre", width=100)
        self.cart_list_table.column("precio", width=100)
        self.cart_list_table.column("cantidad", width=100)
        self.cart_list_table.column("stock", width=100)
        self.cart_list_table.bind("<ButtonRelease-1>", self.get_cart_data)

        # cart widgets
        self.p_id_var = StringVar()
        self.p_nombre_var = StringVar()
        self.p_precio_var = StringVar()
        self.p_cantidad_var = StringVar()
        self.p_stock_var = StringVar()
        cart_widgets_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        cart_widgets_frame.place(x=420, y=550, width=530, height=110)

        p_nombre_label = Label(cart_widgets_frame, text="Nombre del producto", font=("Lato", 13, "normal"), bg="white")
        p_nombre_label.place(x=5, y=5)
        p_nombre_text = Entry(cart_widgets_frame, textvariable=self.p_nombre_var, font=("Lato", 13, "normal"), state="readonly", bg="#EEE6CE")
        p_nombre_text.place(x=5, y=35, width=190, height=22)

        p_precio_label = Label(cart_widgets_frame, text="Precio por cantidad", font=("Lato", 13, "normal"), bg="white")
        p_precio_label.place(x=230, y=5)
        p_precio_text = Entry(cart_widgets_frame, textvariable=self.p_precio_var, font=("Lato", 13, "normal"), state="readonly", bg="#EEE6CE")
        p_precio_text.place(x=230, y=35, width=150, height=22)

        p_cantidad_label = Label(cart_widgets_frame, text="Cantidad", font=("Lato", 13, "normal"), bg="white")
        p_cantidad_label.place(x=400, y=5)
        p_cantidad_text = Entry(cart_widgets_frame, textvariable=self.p_cantidad_var, font=("Lato", 13, "normal"), bg="#EEE6CE")
        p_cantidad_text.place(x=400, y=35, width=120, height=22)

        self.p_stock_label = Label(cart_widgets_frame, text="En Stock", font=("Lato", 13, "normal"), bg="white")
        self.p_stock_label.place(x=5, y=70)

        add_cart_btn = Button(cart_widgets_frame, text="Añadir a la csrrito", command=self.add_cart, font=("Lato", 12, "normal"), bg="#0AA1DD", fg="white")
        add_cart_btn.place(x=180, y=70, width=150, height=30)
        clear_cart_btn = Button(cart_widgets_frame, text="Borrar", command=self.clear_cart, font=("Lato", 12, "normal"), bg="#313552", fg="white")
        clear_cart_btn.place(x=340, y=70, width=150, height=30)

        # billing frame -----------------------------------------------------
        bill_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        bill_frame.place(x=953, y=110, width=390, height=410)

        bill_title = Label(bill_frame, text="Factura del cliente", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        bill_title.pack(side=TOP, fill=X)
        bill_scroll_y = Scrollbar(bill_frame, orient=VERTICAL)
        bill_scroll_y.pack(side=RIGHT, fill=Y)
        self.bill_area_text = Text(bill_frame, yscrollcommand=bill_scroll_y.set)
        self.bill_area_text.pack(fill=BOTH, expand=1)
        bill_scroll_y.config(command=self.bill_area_text.yview)

        # billing buttons ----------------------------------------------------------
        bill_menu_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        bill_menu_frame.place(x=953, y=520, width=390, height=140)

        self.amount_label = Label(bill_menu_frame, text="Cantidad\n0", font=("Lato", 14, "normal"), bg="#f27b53", fg="white")
        self.amount_label.place(x=5, y=5, width=120, height=70)

        self.discount_label = Label(bill_menu_frame, text="Descuento\n5%", font=("Lato", 14, "normal"), bg="#dc587d", fg="white")
        self.discount_label.place(x=130, y=5, width=120, height=70)

        self.net_label = Label(bill_menu_frame, text="Neto a pagar\n0", font=("Lato", 14, "normal"), bg="#847cc5", fg="white")
        self.net_label.place(x=255, y=5, width=125, height=70)

        print_bnt = Button(bill_menu_frame, text="Imprimir", font=("Lato", 14, "normal"), bg="#2EB086", fg="white")
        print_bnt.place(x=5, y=80, width=120, height=50)

        generate_btn = Button(bill_menu_frame, text="Generar\nfactura", command=self.generate_bill, font=("Lato", 14, "normal"), bg="#0AA1DD", fg="white")
        generate_btn.place(x=130, y=80, width=120, height=50)

        clear_all_btn = Button(bill_menu_frame, text="Eliminar\nTodo", command=self.clear_all, font=("Lato", 14, "normal"),bg="#313552", fg="white")
        clear_all_btn.place(x=255, y=80, width=125, height=50)

        self.show_product()

    # methods ----------------------
    def show_producto(self):
        con = sqlite3.connect("DB-gestion.sql")
        cur = con.cursor()
        try:
            cur.execute("SELECT ID, nombre, precio, estado FROM producto Where status='activo'")
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
            if self.buscar_var.get() == "":
                messagebox.showerror("Error", "Campo de búsqueda vacío", parent=self.root)
            else:
                cur.execute("SELECT ID, nombre, precio, cantidad, estado FROM producto WHERE nombre LIKE '%" + self.buscar_var.get() + "%' and estado='activo'")
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

        self.p_id_var.set(row[0])
        self.p_nombre_var.set(row[1])
        self.p_precio_var.set(row[2])
        self.p_stock_var.set(row[3])
        self.p_cantidad_var.set("1")
        self.p_stock_label.config(text=f"En Stock: {row[3]}")

    def get_cart_data(self, ev):
        table_focus = self.cart_list_table.focus()
        table_content = (self.cart_list_table.item(table_focus))
        row = table_content["values"]

        self.p_id_var.set(row[0])
        self.p_nombre_var.set(row[1])
        self.p_precio_var.set(row[2])
        self.p_cantidad_var.set(row[3])

    def add_cart(self):
        if self.p_id_var.get() == "":
            messagebox.showerror("Erreur", "Veuillez Selectionner Un Produit", parent=self.root)
        elif self.p_cantidad_var.get() == "":
            messagebox.showerror("Erreur", "Veuillez Saisir Quantité", parent=self.root)
        elif int(self.p_cantidad_var.get()) > int(self.p_stock_var.get()):
            messagebox.showerror("Error", "Stock insuficiente", parent=self.root)
        else:
            calculated_price = float(int(self.p_cantidad_var.get()) * float(self.p_precio_var.get()))
            print(calculated_price)
            cart_data = [self.p_id_var.get(), self.p_nombre_var.get(), calculated_precio, self.p_cantidad_var.get(), self.p_stock_var.get()]

            # to update cart
            producto_exists = False
            index = 0
            for row in self.cart_list:
                if self.p_id_var.get() == row[0]:
                    producto_exists = True
                    break
                index += 1

            if producto_exists:
                op = messagebox.askyesno("Confirmación", "El producto ya existe. ¿Desea actualizar?")
                if op:
                    if self.p_cantidad_var.get() == "0":
                        self.cart_list.pop(index)
                    else:
                        self.cart_list[index][2] = calculated_price
                        self.cart_list[index][3] = self.p_cantidad_var.get()
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_update()

    def show_cart(self):
        try:
            self.cart_list_table.delete(*self.cart_list_table.get_children())
            for row in self.cart_list:
                self.cart_list_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def bill_update(self):
        self.amount = 0
        self.net_pay = 0
        self.discount = 0
        for row in self.cart_list:
            self.amount = self.amount + float(row[2])
        self.discount = (self.amount * 5)/100
        self.net_pay = self.amount - self.discount

        self.amount_label.config(text=f"Cantidad\n{self.amount}DH")
        self.net_label.config(text=f"Neto a pagar\n{self.net_pay}DH")
        self.cart_title.config(text=f"Carrito | \tProductos totales: {len(self.cart_list)} ")


    def generate_bill(self):
        if self.cust_nombre_var.get() == "" or self.cust_contacto_var.get() == "":
            messagebox.showerror("Error", f"Por favor, introduzca los datos del cliente", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", f"Agregue productos al carrito", parent=self.root)
        else:
            # bill Top
            self.bill_top()
            # bill middle
            self.bill_middle()
            # bill bottom
            self.bill_bottom()

            with open(f"bills/{str(self.invoice_n)}.txt", "w") as f:
                f.write(self.bill_area_text.get("1.0", END))
            messagebox.showinfo("Éxito", "Factura guardada", parent=self.root)


    def bill_top(self):
        self.invoice_n = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        print(self.invoice_n)
        bill_top_temp = f'''
\tRapimarket-Inventario
\tNúmero de teléfono 8899773344 , Marrakech
{str("="*45)}
Nombre del cliente: {self.cust_nombre_var.get()}
Tel cliente : {self.cust_contacto_var.get()}
Factura No. {str(self.invoice_n)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*45)}
nombre del producto\t\t\tQTE\tPrecio
{str("="*45)}
        '''
        self.bill_area_text.delete('1.0', END)
        self.bill_area_text.insert('1.0', bill_top_temp)

        con = sqlite3.connect("DB-gestion.sql")
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO venta VALUES (?,?,?,?)", (self.invoice_n, self.cust_nombre_var.get(), self.cust_contacto_var.get(),str(time.strftime("%d/%m/%Y"))))
            con.commit()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def bill_middle(self):
        con = sqlite3.connect("DB-gestion.sql")
        cur = con.cursor()
        try:
            for row in self.cart_list:
                ID = row[0]
                nombre = row[1]
                cantidad = row[3]
                precio = row[2]
                print(row[4])
                self.bill_area_text.insert(END, "\n " + str(nombre) + "\t\t\t" + str(cantidad) + "\tDH " + str(precio))
                producto_stock = row[4]
                updated_cantidad = int(producto_stock) - int(cantidad)
                if int(updated_cantidad) == 0:
                    status = "inactivo"
                else:
                    status = "activo"
                cur.execute("UPDATE producto set cantidad=?, estado=? where ID=?", (updated_cantidad, estado, ID))
                cur.execute("INSERT INTO line_venta VALUES (?,?,?,?)", (self.invoice_n, ID, precio, cantidad))
            con.commit()
            self.show_producto()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def bill_bottom(self):
        bill_bottom_temp = f'''
{str("="*45)}
Monto Total\t\t\t\tDH {self.amount}
Descuento\t\t\t\tDH {self.discount}
Neto a pagar\t\t\t\tDH {self.net_pay}
{str("="*45)}\n
        '''
        self.bill_area_text.insert(END, bill_bottom_temp)

    def clear_cart(self):
        self.p_id_var.set("")
        self.p_nombre_var.set("")
        self.p_precio_var.set("")
        self.p_cantidad_var.set("")
        self.p_stock_label.config(text=f"En Stock")
        self.p_stock_var.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.cust_nombre_var.set("")
        self.cust_contacto_var.set("")
        self.bill_area_text.delete('1.0', END)
        self.cart_title.config(text=f"Carrito  | \tTotal de Productos:  0")
        self.clear_cart()
        self.show_producto()
        self.show_cart()

    def logout(self):
        self.root.destroy()
        os.system("python login.py")


if __name__ == "__main__":
    root = Tk()
    system = POS(root)
    root.mainloop()
