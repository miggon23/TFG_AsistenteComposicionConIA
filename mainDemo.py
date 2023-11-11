import sys
sys.path.append('./Harmonizer/')
sys.path.append('./Drums/')

from Cadenas_Markov import markovGenerator

from Drums import drumGenerator
from Drums import enums

from Harmonizer import harmonyGenerator

def load_markov_chain(generator):
    generator.load_markov_chain_from_json("./trained_chains/markov_chain_1")

def generate_melodies(generator, n_notes, n_sims):
    return generator.run_markov_chain(num_notes = n_notes, num_simulations = n_sims)

def main():
    generator = markovGenerator.Markov_Generator(use_silences=False)
    load_markov_chain(generator)

    exit = False

    while not exit:
        #markov generator
        option = ""
        while option != "g" and option != "q":
            option = input(
                "[g]: Generar melodias \n[q]: Salir \n")

        if (option == "g"):
            print("Introduce el numero de notas que deseas generar en cada melodia")
            notes = get_input_number(4, 4*40)

            outputs = generate_melodies(generator, notes, 1)
        else:
            exit = True

        #armonizer
        option = ""
        while option != "a" and option != "q":
            option = input(
                "[a]: Armonizar \n[q]: Salir \n")
            
        if (option == "a"):
            harmonyGenerator.HarmonyGenerator.generate(outputs[0])
        else:
            exit = True

        #drums
        option = ""
        while option != "t" and option != "q":
            option = input(
                "[t]: Tamborizar \n[q]: Salir \n")
            
        if (option == "t"):
            style = enums.Style.BASIC
            drumGenerator.DrumGenerator.generate(style)
        else:
            exit = True

def get_input_number(a, b):

    valid_number_entered = False

    while not valid_number_entered:
        try:
            user_input = int(input(f"Introduce un numero entre {a} y {b}: "))
            if a <= user_input <= b:
                valid_number_entered = True 
            else:
                print(f"El numero debe de estar entre {a} y {b}")
        except ValueError:
            print("Por favor introduce un numero valido")

    return user_input


if __name__ == '__main__':
    main()