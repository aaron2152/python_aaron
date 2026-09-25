import tkinter as tk
import os

def abrir_calculadora():
    os.system("calc")

ventana = tk.Tk()
ventana.title("Abrir Calculadora")

boton = tk.Button(ventana, text= "Abrir Calculadora", command=abrir_calculadora)
boton.pack(pady=20)

ventana.mainloop()