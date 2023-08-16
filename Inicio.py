from tkinter import *
from tkinter import ttk, messagebox
from empleado import Empleado
from proveedor import Proveedor
from categoria import Categoria
from producto import Producto
from ventas import Venta
import sqlite3
import os
import threading


class StockManager:
    # Inicialización de la ventana raíz
    # Configuración de la interfaz gráfica de usuario (GUI)
    # Creación de widgets, como etiquetas, botones y marcos
    # Vinculación de funciones a los botones
    # Actualización de contenido y manejo de la aplicación
    def __init__(self, root_win):
        self.root = root_win
        self.root.geometry("1400x700+0+0")
        self.root.title("Gestion de Stock")
        self.root.config(bg="white")

        # screen Title
        title = Label(self.root, text="Gestion Empresarial", font=("Lato", 26, "bold"), bg="white", fg="#343A40", anchor="w", padx=20) # may add anchor here to center left
        title.place(x=200, y=0, relwidth=1, height=70)

        # logout button
        logout_btn = Button(self.root, text="Desconectar", command=self.logout, font=("Lato", 11, "bold"), bd=0, bg="#F66B0E", fg="white")
        logout_btn.place(x=1180, y=10, height=40, width=120)

        # Menu
        menu_frame = Frame(self.root, bd=0, bg="#23282c", relief=RIDGE)
        menu_frame.place(x=0, y=0, width=200, height=400, relheight=1)

        menu_label = Label(menu_frame, text="Menu", font=("Lato", 15, "bold"), fg="#313552", bg="#23ba9b")
        menu_label.pack(side=TOP, fill=X)

        empleado_btn = Button(menu_frame, text="Empleados", command=self.empleado, font=("Lato", 14, "normal"), bg="#23282c", fg="#a7acb2", bd=0, cursor="hand2")
        empleado_btn.pack(side=TOP, fill=X)
        proveedor_btn = Button(menu_frame, text="Proveedores", command=self.proveedor, bg="#23282c", font=("Lato", 14, "normal"), fg="#a7acb2", bd=0, cursor="hand2")
        proveedor_btn.pack(side=TOP, fill=X)
        producto_btn = Button(menu_frame, text="Productos", command=self.producto, font=("Lato", 14, "normal"), bg="#23282c", fg="#a7acb2", bd=0, cursor="hand2")
        producto_btn.pack(side=TOP, fill=X)
        categoria_btn = Button(menu_frame, text="Categorias", command=self.categoria, font=("Lato", 14, "normal"), bg="#23282c", fg="#a7acb2", bd=0, cursor="hand2")
        categoria_btn.pack(side=TOP, fill=X)
        venta_btn = Button(menu_frame, text="Ventas", command=self.venta, font=("Lato", 14, "normal"), bg="#23282c", fg="#a7acb2", bd=0, cursor="hand2")
        venta_btn.pack(side=TOP, fill=X)
        salir_btn = Button(menu_frame, text="Salir", font=("Lato", 14, "normal"), bg="#23282c", fg="#a7acb2", bd=0, cursor="hand2")
        salir_btn.pack(side=TOP, fill=X)

        # dashboard content
        self.empleado_label = Label(self.root, text="Total de Empleados\n0", font=("Lato", 15, "bold"), fg="white", bg="#f27b53", bd=5)
        self.empleado_label.place(x=300, y=80, width=300, height=100)
        self.proveedor_label = Label(self.root, text="Total Proveedores\n0", font=("Lato", 15, "bold"), fg="white", bg="#dc587d", bd=5)
        self.proveedor_label.place(x=650, y=80, width=300, height=100)
        self.producto_label = Label(self.root, text="Total Productos\n0", font=("Lato", 15, "bold"), fg="white", bg="#847cc5", bd=5)
        self.producto_label.place(x=1000, y=80, width=300, height=100)
        self.categoria_label = Label(self.root, text="Total Categorias\n0", font=("Lato", 15, "bold"), fg="white", bg="#fbb168", bd=5)
        self.categoria_label.place(x=300, y=200, width=300, height=100)
        self.venta_label = Label(self.root, text="Total Ventas\n0", font=("Lato", 15, "bold"), fg="white", bg="#23ba9b", bd=5)
        self.venta_label.place(x=650, y=200, width=300, height=100)

        # sales list
        venta_list_frame = Frame(self.root, bd=3, relief=RIDGE)
        venta_list_frame.place(x=220, y=350, width=420, height=250)

        scroll_y = Scrollbar(venta_list_frame, orient=VERTICAL)
        scroll_x = Scrollbar(venta_list_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        venta_list_columns = ("factura_no", "nombre_cliente", "contacto_cliente", "fecha")
        self.venta_list_table = ttk.Treeview(venta_list_frame, columns=venta_list_columns, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.venta_list_table.pack(fill=BOTH, expand=1)
        scroll_x.config(command=self.venta_list_table.xview)
        scroll_y.config(command=self.venta_list_table.yview)

        self.venta_list_table.heading("factura_no", text="Factura No.")
        self.venta_list_table.heading("nombre_cliente", text="Nombre Cliente")
        self.venta_list_table.heading("contacto_cliente", text="Contacto Cliente")
        self.venta_list_table.heading("fecha", text="Fecha")
        self.venta_list_table["show"] = "headings"

        self.venta_list_table.column("factura_no", width=100)
        self.venta_list_table.column("nombre_cliente", width=100)
        self.venta_list_table.column("contacto_cliente", width=100)
        self.venta_list_table.column("fecha", width=100)

        # line_sale list
        line_venta_list_columns = Frame(self.root, bd=3, relief=RIDGE)
        line_venta_list_columns.place(x=660, y=350, width=650, height=250)

        scroll_y = Scrollbar(line_venta_list_columns, orient=VERTICAL)
        scroll_x = Scrollbar(line_venta_list_columns, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        venta_list_columns = ("factura_no", "nombre_producto", "precio", "cantidad")
        self.line_venta_list_table = ttk.Treeview(line_venta_list_columns, columns=venta_list_columns, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.line_venta_list_table.pack(fill=BOTH, expand=1)
        scroll_x.config(command=self.line_venta_list_table.xview)
        scroll_y.config(command=self.line_venta_list_table.yview)

        self.line_venta_list_table.heading("factura_no", text="Factura No.")
        self.line_venta_list_table.heading("nombre_producto", text="Nombre Producto")
        self.line_venta_list_table.heading("precio", text="Precio")
        self.line_venta_list_table.heading("cantidad", text="Cantidad")
        self.line_venta_list_table["show"] = "headings"

        self.line_venta_list_table.column("factura_no", width=100)
        self.line_venta_list_table.column("nombre_producto", width=100)
        self.line_venta_list_table.column("precio", width=100)
        self.line_venta_list_table.column("cantidad", width=100)


        # footer
        footer = Label(self.root, text="Escribir pie de pagina", font=("Lato", 15, "normal"), bg="#2EB086", fg="#313552") # may add anchor here to center left
        footer.place(x=0, y=670, relwidth=1, height=30)

        self.update_content()
        self.show_venta()
        self.show_line_venta()
        # ========================================================
        # Creación de una ventana secundaria para gestionar empleados
        # Utilización de la clase Employee para administrar empleados
    def empleado(self):
        self.new_window = Toplevel(self.root)
        self.emp_manager = Empleado(self.new_window)

    # Creación de una ventana secundaria para gestionar proveedores
    # Utilización de la clase Supplier para administrar proveedores
    def proveedor(self):
        self.new_window = Toplevel(self.root)
        self.proveedor_manager = Proveedor(self.new_window)

    # Creación de una ventana secundaria para gestionar categorías
    # Utilización de la clase Category para administrar categorías
    def categoria(self):
        self.new_window = Toplevel(self.root)
        self.categoria_manager = Categoria(self.new_window)

    # Creación de una ventana secundaria para gestionar productos
    # Utilización de la clase Product para administrar productos
    def producto(self):
        self.new_window = Toplevel(self.root)
        self.producto_manager = Producto(self.new_window)

    # Creación de una ventana secundaria para gestionar ventas
    # Utilización de la clase Sales para administrar ventas
    def venta(self):
        self.new_window = Toplevel(self.root)
        self.venta_manager = Venta(self.new_window)

    # Actualización de las etiquetas que muestran estadísticas
    # Utilización de hilos para actualización periódica de contenido
    def update_content(self):
        con = sqlite3.connect("DB-gestion.sql")
        cur = con.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM empleado")
            p = cur.fetchone()[0]
            self.empleado_label.config(text=f"Total de Empleados\n{p}")

            cur.execute("SELECT COUNT(*) FROM proveedor")
            proveedor = cur.fetchone()[0]
            self.proveedor_label.config(text=f"Total de Proveedores\n{proveedor}")

            cur.execute("SELECT COUNT(*) FROM producto")
            prd = cur.fetchone()[0]
            self.producto_label.config(text=f"Total de Productos\n{prd}")

            cur.execute("SELECT COUNT(*) FROM categoria")
            cat = cur.fetchone()[0]
            self.categoria_label.config(text=f"Total de Categorias\n{cat}")

            self.venta_label.config(text=f"Total de Ventas\n{str(len(os.listdir('bills')))}")

            threading.Timer(2.0, self.update_content).start()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

     # Cierre de la ventana principal y vuelta a la ventana de inicio de sesión
    def logout(self):
        self.root.destroy()
        os.system("python login.py")

    # Mostrar detalles de ventas en una tabla
    # Utilización de consultas SQL para obtener los datos
    def show_venta(self):
        con = sqlite3.connect("DB-gestion.sql")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM venta")
            rows = cur.fetchall()
            self.venta_list_table.delete(*self.venta_list_table.get_children())
            for row in rows:
                self.venta_list_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    # Mostrar detalles de las líneas de venta en una tabla
    # Utilización de consultas SQL para obtener los datos
    def show_line_venta(self):
        con = sqlite3.connect("DB-gestion.sql")
        cur = con.cursor()
        try:
            cur.execute("SELECT p.nombre, lv.precio, lv.cantidad FROM line_venta lv JOIN producto p ON lv.ID =p.ID")
            rows = cur.fetchall()
            self.line_venta_list_table.delete(*self.line_venta_list_table.get_children())
            for row in rows:
                self.line_venta_list_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    # Crear la ventana principal y la instancia de la clase StockManager
    # Iniciar el ciclo de eventos de la interfaz gráfica
if __name__ == "__main__":
    root = Tk()
    system = StockManager(root)
    root.mainloop()
