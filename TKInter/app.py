from tkinter import *
from tkinter import ttk

def setStyle(frm):
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#ccc")

    l1 = ttk.Label(frm, text="Generador Musical", font=30)
    l1.grid(column = 0, row = 0)
    l1.anchor(N)


def setButtons(frm, root):
    ttk.Button(frm, text = "Generar melodías", command = root.destroy).grid(column=0, row = 1)
    ttk.Button(frm, text = "Salir", command = root.destroy).grid(column=0, row = 10)
    


def main():
    #Creación de la aplicación raíz
    root = Tk()
    frm = ttk.Frame(root, padding = 10, width=200, height=200)
    frm.grid()

    #Setting de texto y botones
    setStyle(frm)
    setButtons(frm, root)
    

    #Llama al bucle de la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()
