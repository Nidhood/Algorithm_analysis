## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================

import random
import sys


def generate_activities(num_activities, num_slots):
    """Genera un número específico de actividades aleatorias."""
    activities = []
    s = 0
    while s < num_activities:
        start = random.randint(0, num_slots - 1)
        end = random.randint(start + 1, num_slots)
        if start < end:
            activities.append(f"act_{s} {start} {end}")
            s = s + 1
    return activities


def main():
    # Verificar argumentos
    if len(sys.argv) < 4:
        print("Usage: python3", sys.argv[0], "number_of_files number_of_activities number_of_slots")
        sys.exit(1)

    # Leer argumentos
    num_files = int(sys.argv[1])
    num_activities = int(sys.argv[2])
    num_slots = int(sys.argv[3])

    # Generar y guardar en archivos
    for i in range(1, num_files + 1):
        filename = f"activities_{i}"
        activities = generate_activities(num_activities, num_slots)

        # Guardar en archivo
        with open(filename, 'w') as file:
            for activity in activities:
                file.write(activity + '\n')

        print(f"Archivo {filename} creado con {num_activities} actividades.")


if __name__ == "__main__":
    main()