import sys
sys.path.append('./Cadenas_Markov/')
sys.path.append('./Harmonizer/')
sys.path.append('./Drums/')
sys.path.append('./Basslines/')

from tkinter import *
from tkinter import ttk
import random # TO DELETE
import mainDemo as demo
from Cadenas_Markov import markovGenerator
from Harmonizer import harmonyGenerator

from Basslines import basslineGenerator

melody = None

def generateMelodies(generator):
    melody = demo.generate_melodies(generator, 2 * random.randint(5, 15), 1)[0]

def armonice():
    if(melody == None):
        return
    bassline = basslineGenerator.BasslineGenerator.generate()
    harmonyGenerator.HarmonyGenerator.generate(bassline, melody)

def tamborice():
    demo.tamborice()

def setStyle(frm):
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#ccc")

    l1 = ttk.Label(frm, text="Generador Musical", font=30,)
    l1.grid(column = 0, row = 0)
    l1.anchor(N)


def setButtons(frm, root, generator):
    ttk.Button(frm, text = "Generar melodías", command = generateMelodies(generator)).grid(column=0, row = 1)
    ttk.Button(frm, text = "Armonizar", command = generateMelodies(generator)).grid(column=0, row = 2)
    ttk.Button(frm, text = "Tamborizar", command = generateMelodies(generator)).grid(column=0, row = 3)
    ttk.Button(frm, text = "Salir", command = root.destroy).grid(column=0, row = 10)
    


def main():
    #Creación de la aplicación raíz
    root = Tk()
    root.geometry("400x300")
    frame = ttk.Frame(root, padding = 20)
    frame.grid()

    generator = markovGenerator.Markov_Generator(use_silences=False)
    demo.load_markov_chain(generator)
    #Setting de texto y botones
    setStyle(frame)
    setButtons(frame, root, generator)
    

    #Llama al bucle de la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()


