import random
import itertools


# Obtenemos los vecinos
def get_neighbors(i, j, rows, cols):
    neighbors = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols:
                neighbors.append((ni, nj))
            # end if
        # end for
    # end for
    return neighbors


# Obtenemos las casillas frontera para detectar minas y movimientos seguros
def get_frontier(matrix, rows, cols):
    frontier = set()
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] != '?':
                neighbors = get_neighbors(i, j, rows, cols)
                if any(matrix[ni][nj] == '?' for (ni, nj) in neighbors):
                    frontier.add((i, j))
                # end if
            # end if
        # end for
    # end for
    return frontier


# Aplicamos reglas simples para deducir movimientos seguros y minas
def simple_solver(matrix, rows, cols, known_mines):
    safe_moves = set()
    new_mines = set()

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == '?' or (i, j) in known_mines:
                continue
            # end if

            num = matrix[i][j]
            neighbors = get_neighbors(i, j, rows, cols)
            hidden_neighbors = [n for n in neighbors if matrix[n[0]][n[1]] == '?']
            known_count = sum(1 for n in neighbors if n in known_mines)

            # Regla 1: Si todas las minas están marcadas, los vecinos son seguros
            if known_count == num:
                for h in hidden_neighbors:
                    if h not in known_mines and h not in safe_moves:
                        safe_moves.add(h)
                    # end if
                # end for
            #end if

            # Regla 2: Vecinos ocultos = minas faltantes, puee todos son minas
            elif known_count + len(hidden_neighbors) == num:
                for h in hidden_neighbors:
                    if h not in known_mines and h not in new_mines:
                        new_mines.add(h)
                    # end if
                # end for
            # end if
        # end for
    return safe_moves, new_mines


# Genera combinaciones válidas de minas para las restricciones dadas
def generate_valid_assignments(constraints):
    if not constraints:
        return []

    # Recopilar todas las casillas ocultas unicas
    all_hidden = set()
    for (hidden, _) in constraints:
        all_hidden.update(hidden)
    all_hidden = list(all_hidden)

    # Si no hay casillas ocultas, retornar vacío
    if not all_hidden:
        return []

    # Generar todas las posibles combinaciones de minas
    valid_assignments = []
    n = len(all_hidden)

    # Para cada posible numero de minas
    for r in range(0, n + 1):

        # Para cada combinación de tamano r
        for combo in itertools.combinations(all_hidden, r):
            mines_combo = set(combo)
            valid = True

            # Verificar contra cada restriccion

            for (hidden_list, required) in constraints:

                # Contar minas en esta restriccion
                count = len(mines_combo & set(hidden_list))

                # Si no cumple, descartar
                if count != required:
                    valid = False
                    break

            if valid:
                valid_assignments.append(mines_combo)

    return valid_assignments


# Inferir casillas seguras y minas ciertas a partir de las asignaciones validas
def infer_from_assignments(valid_assignments, all_hidden):
    safe_moves = set(all_hidden)
    certain_mines = set()

    if not valid_assignments:
        return set(), set()

    # Encontrar casillas que siempre son minas
    for cell in all_hidden:
        if all(cell in assignment for assignment in valid_assignments):
            certain_mines.add(cell)

    # Encontrar casillas que nunca son minas
    for cell in all_hidden:
        if all(cell not in assignment for assignment in valid_assignments):
            safe_moves.add(cell)

    return safe_moves, certain_mines


# Realiza busqueda avanzada en la frontera usando Vertex Cover
def frontier_search(matrix, rows, cols, known_mines, frontier):
    constraints = []
    all_hidden = set()

    for (i, j) in frontier:
        num = matrix[i][j]
        neighbors = get_neighbors(i, j, rows, cols)
        hidden = [
            (ni, nj) for (ni, nj) in neighbors
            if matrix[ni][nj] == '?' and (ni, nj) not in known_mines
        ]
        known_count = sum(1 for (ni, nj) in neighbors if (ni, nj) in known_mines)
        required_mines = num - known_count

        # Solo considerar restricciones válidas
        if required_mines < 0 or required_mines > len(hidden):
            continue

        if hidden:  # Solo agregar si hay casillas ocultas
            constraints.append((hidden, required_mines))
            all_hidden.update(hidden)

    # Si no hay restricciones, retornar vacío
    if not constraints:
        return set(), set()

    # Generar y validar asignaciones
    valid_assignments = generate_valid_assignments(constraints)

    # Inferir de las asignaciones válidas
    safe_moves, certain_mines = infer_from_assignments(valid_assignments, list(all_hidden))
    return safe_moves, certain_mines


# Selecciona un movimiento seguro aleatorio de las casillas ocultas
def random_safe_move(matrix, rows, cols, known_mines):
    options = [
        (i, j) for i in range(rows) for j in range(cols)
        if matrix[i][j] == '?' and (i, j) not in known_mines
    ]
    return random.choice(options) if options else None

# Heuristic solver que orquesta las 3 fases de resolución
def heuristic_solver(matrix, rows, cols, known_mines):

    # Fase 1: Reglas simples iterativas
    changed = True
    while changed:
        safe_moves, new_mines = simple_solver(matrix, rows, cols, known_mines)
        if safe_moves:
            return next(iter(safe_moves))
        if new_mines:
            known_mines.update(new_mines)
            changed = True
        else:
            changed = False

    # Fase 2: Búsqueda en la frontera
    frontier = get_frontier(matrix, rows, cols)
    if len(frontier) <= 15:  # Límite para evitar explosión combinatoria
        safe_frontier, mines_frontier = frontier_search(
            matrix, rows, cols, known_mines, frontier
        )
        if safe_frontier:
            return next(iter(safe_frontier))
        if mines_frontier:
            known_mines.update(mines_frontier)
            # Intentar nuevamente con nueva información
            return heuristic_solver(matrix, rows, cols, known_mines)

    # Fase 3: Selección aleatoria segura
    return random_safe_move(matrix, rows, cols, known_mines)