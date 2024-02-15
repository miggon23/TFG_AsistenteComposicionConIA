import sys
sys.path.append('./Cadenas_Markov/')
sys.path.append('./Harmonizer/')
sys.path.append('./Drums/')
sys.path.append('./Basslines/')

from Cadenas_Markov import markovGenerator

from Drums import drumGenerator
from Drums import enums

from Harmonizer import harmonyGenerator

from Basslines import basslineGenerator

FILE = "./midi/markov_melody_8.mid"

def load_markov_chain(generator):
    generator.load_markov_chain_from_json("./trained_chains/markov_chain_1")

def generate_melodies(generator, n_bar, n_sims):
    return generator.run_markov_chain(num_bar = n_bar, num_simulations = n_sims)

def main():
    generator = markovGenerator.Markov_Generator(use_silences=False)
    load_markov_chain(generator)

    exit = False

    while not exit:
        #markov generator
        option = ""
        while option != "g" and option != "c" and option != "q":
            option = input(
                "[g]: Generar melodias \n[c]: Cargar melodia de archivo \n[q]: Salir \n")

        if (option == "g"):
            print("Introduce el numero de compases que deseas generar en cada melodia")
            bar = get_input_number(2, 4*40)

            outputs = generate_melodies(generator, bar * 2, 1)

        elif (option == "c"):
            outputs = [FILE]
        
        else:
            exit = True
            break

        #armonizer
        option = ""
        while option != "q" and option != "a":
            option = input(
                "[g]: Generar de nuevo \n[a]: Armonizar \n[q]: Salir \n")

            if (option == "g"):
                print("Introduce el numero de compases que deseas generar en cada melodia")
                bar = get_input_number(2, 4*40)

                outputs = generate_melodies(generator, bar * 2, 1)
            elif (option == "a"):
                bassline = basslineGenerator.BasslineGenerator.generate()
                harmonyGenerator.HarmonyGenerator.generate(bassline, outputs[0])
            elif (option == "q"):
                exit = True
                break

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
            break

def armonice(inputMelody):
    bassline = basslineGenerator.BasslineGenerator.generate()
    harmonyGenerator.HarmonyGenerator.generate(bassline, inputMelody)
    return bassline

def tamborice():
    style = enums.Style.BASIC
    drumGenerator.DrumGenerator.generate(style)

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