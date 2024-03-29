from tkinter import *
from tkinter import messagebox
import sqlite3
import os



class LoginManager:
    def __init__(self, root_win):
        self.root = root_win
        self.root.geometry("600x600+300+50")
        self.root.title("Gestion de Stock")
        self.root.config(bg="#2EB086")

        # variables
        self.user_id_var = StringVar()
        self.password_var = StringVar()

        # login frame

        login_frame = Frame(self.root, bd=0, relief=RIDGE, bg="white")
        login_frame.place(x=100, y=100, width=400, height=400)

        # screen Title
        title = Label(login_frame, text="Conectarse", font=("Lato", 18, "bold"), bg="white", fg="#343A40", anchor="w") # may add anchor here to center left
        title.place(x=50, y=40, relwidth=1)
        title_2 = Label(login_frame, text="Bienvenido al sistema de gestión de stock", font=("Lato", 12, "normal"), bg="white", fg="#D0C9C0", anchor="w")  # may add anchor here to center left
        title_2.place(x=50, y=70, relwidth=1)

        # username
        username_label = Label(login_frame, text="Identificación de usuario", font=("Lato", 13, "normal"), bg="white", fg="#7F8487")
        username_label.place(x=50, y=120)
        username_text = Entry(login_frame, textvariable=self.user_id_var, font=("Lato", 18, "normal"), bg="#EFEAD8", bd=0)
        username_text.place(x=50, y=150, width=300, height=40)
        # password
        password_label = Label(login_frame, text="Contraseña", font=("Lato", 13, "normal"), bg="white", fg="#7F8487")
        password_label.place(x=50, y=200)
        password_text = Entry(login_frame, textvariable=self.password_var, font=("Lato", 18, "normal"), bg="#EFEAD8", show="*", bd=0)
        password_text.place(x=50, y=230, width=300, height=40)

        # button
        login_button = Button(login_frame, text="Conectarse", command=self.login, font=("Lato", 14, "normal"), bg="#2EB086", fg="white", bd=0)
        login_button.place(x=50, y=300, width=300, height=40)

    # methods

    def login(self):
        con = sqlite3.connect(r'DB-gestion.sql')
        cur = con.cursor()
        try:
            if self.user_id_var.get() == "" or self.password_var.get() == "":
                messagebox.showerror("Error", "Por favor ingrese nombre de usuario y contraseña", parent=self.root)
            else:
                cur.execute("SELECT type FROM employee WHERE id=? AND password=?", (self.user_id_var.get(), self.password_var.get()))
                user_type = cur.fetchone()[0]
                print(user_type)
                if user_type is None:
                    messagebox.showerror("Error", "ID de usuario o contraseña no válidos", parent=self.root)
                else:
                    if user_type == "Admin":
                        self.root.destroy()
                        os.system("python admin_dashboard.py")
                    elif user_type == "Empleado":
                        self.root.destroy()
                        os.system("python pos.py")
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    system = LoginManager(root)
    root.mainloop()
