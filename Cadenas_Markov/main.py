from MarkovGenerator import Markov_Generator

def create_markov_chain(generator):
    generator.train_markov_chain()
    generator.save_markov_chain_to_json("./trained_chains/", "markov_chain_1")

def load_markov_chain(generator):
    generator.load_markov_chain_from_json("./trained_chains/markov_chain_1.json")

def generate_melodies(generator):
    generator.run_markov_chain()

def main():
    generator = Markov_Generator()

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
            generate_melodies(generator)
        else:
            exit = True


if __name__ == '__main__':
    main()