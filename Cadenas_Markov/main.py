from markovGenerator import Markov_Generator

def create_markov_chain(generator):
    generator.train_markov_chain()
    generator.save_markov_chain_to_json("./trained_chains/", "markov_chain_1")

def load_markov_chain(generator):
    generator.load_markov_chain_from_json("./trained_chains/markov_chain_1")

def generate_melodies(generator, n_notes, n_sims):
    generator.run_markov_chain(num_notes = n_notes, num_simulations = n_sims)

def main():
    generator = Markov_Generator(use_silences=False, smooth_ocurrences=False)

    exit = False

    while not exit:
        option = ""
        while option != "1" and option != "2" and option != "3" and option != "q":
            option = input(
                "[1]: Crear cadena de markov \n[2]: Cargar cadena creada previamente \n[3]: Generar melodias \n[q]: Salir \n")

        if (option == "1"):
            create_markov_chain(generator)
        elif (option == "2"):
            load_markov_chain(generator)
        elif (option == "3"):
            print("Introduce el numero de notas que deseas generar en cada melodia")
            notes = get_input_number(4, 4*40)

            print("Introduce el numero de melodias que deseas generar en total")
            sims = get_input_number(1, 20)

            generate_melodies(generator, notes, sims)
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