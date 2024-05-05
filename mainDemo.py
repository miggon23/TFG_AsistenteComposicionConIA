import sys
sys.path.append('./Cadenas_Markov/')
sys.path.append('./MagentaGenerator/')
sys.path.append('./RNN/')
sys.path.append('./Harmonizer/')
sys.path.append('./Drums/')
sys.path.append('./Basslines/')

from Cadenas_Markov import markovGenerator
from MagentaGenerator import magentaPython
from RNN import rnnGenerator

from Drums import drumGenerator
from Drums import enums

from Harmonizer import harmonyGenerator

from Basslines import basslineGenerator

FILE = "./Media/midi/output_song.mid"

def load_markov_chain(generator):
    generator.load_markov_chain_from_json("./trained_chains/markov_chain_1")

def generate_markov(generator, n_bar, n_sims):
    return generator.run_markov_chain(num_bar = n_bar * 2, num_simulations = n_sims)

def generate_magenta(n_bar, n_sims, temperature):
    return magentaPython.generate_melodies(n_melodies=n_sims, n_steps=n_bar * 8, temperature=temperature)

def generate_rnn(n_bar, temperature):
    return rnnGenerator.generate(n_bar*8, temperature)

def continue_magenta(path_to_midi, n_bar, temperature):
    return magentaPython.continue_melody_midi(path_to_midi, temperature = temperature)

def load_file(path_to_midi="./Media/midi/output_song.mid"):
    return [path_to_midi]

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

            outputs = generate_magenta(bar * 2, 1)

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

                outputs = generate_markov(generator, bar * 2, 1)
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
            drumGenerator.DrumGenerator.generateAllStyles()
        else:
            exit = True
            break

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