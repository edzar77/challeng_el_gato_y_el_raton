import math
import time

# Tamaño del tablero
SIZE = 15

# Posiciones iniciales
mouse_pos = [0, 0]
cat_pos = [SIZE - 1, 0]
cheese_pos = [SIZE - 1, SIZE - 1]

# Movimientos posibles
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izq, der


def in_bounds(pos):
    """Verifica que una posición esté dentro del tablero"""
    return 0 <= pos[0] < SIZE and 0 <= pos[1] < SIZE


def manhattan(a, b):
    """Distancia Manhattan (para medir cercanía)"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def draw_board(mouse, cat, cheese):
    """Dibuja el tablero en consola"""
    for i in range(SIZE):
        for j in range(SIZE):
            if [i, j] == mouse:
                print("M", end=" ")
            elif [i, j] == cat:
                print("C", end=" ")
            elif [i, j] == cheese:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()
    print()


def is_terminal(mouse, cat):
    """Verifica si el juego terminó"""
    if mouse == cheese_pos:
        return True
    if mouse == cat:
        return True
    return False


def evaluate(mouse, cat):
    """Evalúa el estado desde el punto de vista del gato (mayor = mejor para el gato)"""
    if mouse == cat:
        return 1000  # Gato gana
    if mouse == cheese_pos:
        return -1000  # Ratón gana
    # Cuanto más cerca el gato del ratón, mejor; cuanto más lejos el ratón del queso, mejor para el gato
    return -(manhattan(mouse, cheese_pos)) + (15 - manhattan(cat, mouse))


def minimax(mouse, cat, depth, is_cat_turn):
    """Algoritmo minimax básico sin poda"""
    if depth == 0 or is_terminal(mouse, cat):
        return evaluate(mouse, cat), None

    if is_cat_turn:
        best_value = -math.inf
        best_move = None
        for move in moves:
            new_cat = [cat[0] + move[0], cat[1] + move[1]]
            if not in_bounds(new_cat):
                continue
            val, _ = minimax(mouse, new_cat, depth - 1, False)
            if val > best_value:
                best_value = val
                best_move = new_cat
        return best_value, best_move
    else:
        best_value = math.inf
        best_move = None
        for move in moves:
            new_mouse = [mouse[0] + move[0], mouse[1] + move[1]]
            if not in_bounds(new_mouse):
                continue
            val, _ = minimax(new_mouse, cat, depth - 1, True)
            if val < best_value:
                best_value = val
                best_move = new_mouse
        return best_value, best_move


# ------------------- Juego principal -------------------

print("🐭 El laberinto del gato y el ratón (versión simple)")
print("Usa W/A/S/D para mover el ratón hacia el queso (Q)")
print("El gato (C) usará el algoritmo Minimax para atraparte.\n")

while True:
    draw_board(mouse_pos, cat_pos, cheese_pos)

    # Condiciones de fin
    if mouse_pos == cheese_pos:
        print("¡El ratón llegó al queso! 🧀 ¡Ganaste!")
        break
    if mouse_pos == cat_pos:
        print("😿 El gato atrapó al ratón. ¡Perdiste!")
        break

    # Movimiento del jugador (ratón)
    move = input("Movimiento (W/A/S/D): ").lower()
    if move not in ["w", "a", "s", "d"]:
        print("Movimiento inválido.")
        continue

    if move == "w":
        new_pos = [mouse_pos[0] - 1, mouse_pos[1]]
    elif move == "s":
        new_pos = [mouse_pos[0] + 1, mouse_pos[1]]
    elif move == "a":
        new_pos = [mouse_pos[0], mouse_pos[1] - 1]
    else:  # "d"
        new_pos = [mouse_pos[0], mouse_pos[1] + 1]

    if in_bounds(new_pos):
        mouse_pos = new_pos
    else:
        print("Movimiento fuera del tablero.")
        continue

    # Turno del gato (IA con Minimax)
    print("El gato está pensando...")
    _, new_cat = minimax(mouse_pos, cat_pos, 3, True)  # profundidad = 3
    if new_cat:
        cat_pos = new_cat
    time.sleep(0.5)
