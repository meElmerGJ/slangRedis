import redis
from tabulate import tabulate

r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=0)


# Class to create slang objects
class Slang:
    words_generated = False

    def __init__(self, word, meaning):
        self.word = word
        self.meaning = meaning


# Function to print a done task correctly message with a specified format
def sys_msg(types, msg):
    print(f"\n-----> {types}: {msg} <------")


# Function verify if a word required exists.
def exists(value):
    if r.exists(value) != 1:
        return False
    else:
        return True


# Functino to input values
def input_word():
    return input("Ingrese la palabra >> ")


# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////

# -------------------------------PROGRAM FUNCTIONS ----------------------------------------

# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////

# Function create a slang object
def add_word():
    word = input_word()
    if not exists(f'{word}'):
        meaning = input("Ingrese el significado >> ")
        new_slang = Slang(word, meaning)
        r.set(f'{new_slang.word}', f'{new_slang.meaning}')
        sys_msg("INFO", "Palabra agregada")
    else:
        sys_msg("ERROR", "La palabra ya existe")


# Function to update a word
def edit_word():
    word = input_word()
    if not exists(f'{word}'):
        sys_msg("ERROR", "La palabra no existe")
    else:
        meaning = input("Ingrese el nuevo significado >> ")
        r.set(word, f'{meaning}')
        sys_msg("INFO", "Palabra editada")


# Function to delete a word
def del_word():
    word = input("Ingrese la palabra >> ")
    if not exists(f'{word}'):
        sys_msg("ERROR", "La palabra no existe")
    else:
        r.delete(word)
        sys_msg("INFO", "La palabra ha sido eliminada")


# Function get all records
def get_words():
    values = r.keys("*")
    table = []
    for i in values:
        table.append([i, r.get(i)])
    print(tabulate(table, headers=["Palabra", "Significado"], tablefmt="psql"))


# Function to get a specific word meaning
def get_meaning():
    word = input_word()
    if not exists(word):
        sys_msg("ERROR", "La palabra no existe")
    else:
        print(f"\n{word}, significa: {r.get(word)}")


# Function to generate 10 records to test functions. (TEST USAGE ONLY)
def generate_data():
    if Slang.words_generated:
        sys_msg("ERROR", "Los registros ya han sido creados")
    else:
        slang_objects = [
            Slang("Chombo", "Amigo cercano o compañero"),
            Slang("Jato", "Casa o hogar"),
            Slang("Pana", "Amigo o camarada"),
            Slang("Que xopa!", "El clasico saludo de nosotros"),
            Slang("Taquilla", "Alguna historia o relato que puede ser falsa"),
            Slang("Quilla", "Dinero"),
            Slang("Tirar la posta", "Contar una historia o chisme"),
            Slang("Taquear", "Comer en exceso"),
            Slang("Chiri", "Frío"),
            Slang("Pelea de gallos", "Competencia o disputa acalorada")
        ]
        for i in slang_objects:
            r.set(i.word, i.meaning)
        sys_msg("INFO", "Se han creado 10 registros")
        Slang.words_generated = True


# Function to delete all records (TEST USAGE ONLY)
def delete_all_data():
    r.flushdb()
    sys_msg("INFO", "Todos los registros han sido eliminados")


# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////

# ---------------------------------------PROGRAM ------------------------------------------

# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////


if __name__ == '__main__':
    try:
        # Flujos de programa
        print("\nBIENVENIDO AL DICCIONARIO DE SLANG PANAMEÑO\n")

        # Program menu
        menu = """
                1) Agregar nueva palabra
                2) Editar palabra
                3) Eliminar palabra 
                4) Ver palabras
                5) Buscar significado de palabra
                6) Insertar 10 registros(only test usage)
                7) Eliminar todos los registros(only test usage)
                8) Salir
                """

        # Program main loop // Warning! -> Need to use version above Python 3.10 for ***match - case*** Statements.
        end = False

        while not end:
            try:
                print(menu)
                option = int(input(f"Ingresa una opcion: "))
                if int(option) in range(1, 9):
                    match option:
                        case 1:
                            add_word()
                        case 2:
                            edit_word()
                        case 3:
                            del_word()
                        case 4:
                            get_words()
                        case 5:
                            get_meaning()
                        case 6:
                            generate_data()
                        case 7:
                            delete_all_data()
                        case 8:
                            sys_msg("INFO", "El programa ha finalizado")
                            exit()
                else:
                    sys_msg("ERROR", "Ingrese una opcion correcta")
            except ValueError:
                sys_msg("ERROR", "Ingrese una opcion correcta")
    except (KeyboardInterrupt, EOFError):
        sys_msg("INFO", "El programa ha finalizado")
