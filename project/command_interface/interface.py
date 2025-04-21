from project.free_flow.board.read_board import read_board
from project.free_flow.free_flow import free_flow


class Interface:
    def __init__(self):
        self.command = ""
        self.input_board = None
        self.graph = None  # Placeholder for a possible 'Graph' object

    def get_command(self):
        return self.command

    def set_command(self, command):
        self.command = command.strip()

    def set_input_board(self, input_board):
        self.input_board = input_board

    def play(self):
        if self.input_board is None:
            print("Debe cargar un tablero primero con el comando 'cargar nombre_archivo'.")
            return

        free_flow(self.input_board)
        print("Resultado exitoso. Ha ganado el juego")

    def print_general_help(self):
        commands = [
            "cargar nombre_archivo",
            "jugar",
            "salir"
        ]

        print("Comandos:")
        for idx, command in enumerate(commands, start=1):
            print(f"{idx}. {command}")
        print("Para obtener más información sobre un comando específico, digite 'ayuda' seguido del comando deseado")

    def print_specific_help(self, words, word_count):
        if word_count == 3 and words[1] == "cargar" and words[2] == "nombre_archivo":
            print("Modo de uso: 'cargar' nombre_archivo")
        elif word_count == 2 and words[1] == "jugar":
            print("Modo de uso: 'jugar'")
        elif word_count == 2 and words[1] == "salir":
            print("Modo de uso: 'salir'")
            print("Termina la ejecución de la aplicación")
        else:
            print("Comando no reconocido. Intente nuevamente.")

    def process_command(self):
        words = self.command.split()

        if not words:
            print("Comando vacío. Intente nuevamente.")
            return

        action = words[0]
        word_count = len(words)

        try:
            if action == "ayuda" and word_count == 1:
                self.print_general_help()
            elif action == "ayuda":
                self.print_specific_help(words, word_count)
            elif action == "cargar" and word_count == 2:
                self.input_board = f'inputs/{words[1]}'
                read_board(f'inputs/{words[1]}')
                print(f"Resultado exitoso. El tablero ha sido cargado exitosamente desde el archivo {self.input_board}")
            elif action == "jugar" and word_count == 1:
                self.play()
            elif action == "salir" and word_count == 1:
                print("Gracias por jugar")
                print("------------------------------------------------------------------------------------------------------------------------")
            else:
                print("Comando no reconocido. Intente nuevamente.")
        except Exception as e:
            print(f"Error: {e}")
