import sqlite3


def create_db():
    con = sqlite3.connect(r'DB-gestion.sql')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS empleado("
                "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                "nombre text,"
                "email text,"
                "genero text,"
                "contacto text,"
                "fn text,"
                "fi text,"
                "contraseña text,"
                "direccion text,"
                "salario float)"
                )
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS cliente("
                "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                "nombre text,"
                "email text,"
                "genero text,"
                "fn text,"
                "direccion text)"
                )
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS proveedor("
                "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                "nombre text,"
                "email text,"
                "detalle text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS categoria("
                "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                "nombre text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS producto("
                "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                "categoria text,"
                "proveedor text,"
                "nombre text,"
                "proveedor_ID text,"
                "precio float)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS venta("
                "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                "cl_ID integer,"
                "prod_ID,"
                "cl_contacto text ,"
                "fecha text,"
                "FOREIGN KEY (cl_ID) REFERENCES cliente(ID),"
                "FOREIGN KEY (prod_ID) REFERENCES producto(ID))")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS line_venta(ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                "factura_no INTEGER,"
                "nombre_prod text,"
                "precio float,"
                "cantidad interger,"
                "FOREIGN KEY (factura_no) REFERENCES venta(factura_no),"
                "FOREIGN KEY (nombre_prod) REFERENCES producto(nombre))")

    con.commit()



create_db()