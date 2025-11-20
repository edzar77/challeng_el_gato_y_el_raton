import random
from collections import deque
import math
import os
import sys
import time
from copy import deepcopy

# ---------- Parámetros ----------
ROWS = 15
COLS = 15

MAX_DEPTH = 4        # profundidad del Minimax (ajustar para más/menos "pensamiento")
WALL_DENSITY = 0.30  # probabilidad aproximada de paredes (se usará generación de laberinto)
SEED = None          # para reproducibilidad, o None

# Posiciones por defecto
MOUSE_START = (0, 0)
CHEESE_POS = (ROWS - 1, COLS - 1)
CAT_START = (ROWS - 1, 0)

# Símbolos para dibujar
WALL = '#'
EMPTY = ' '
MOUSE = 'M'
CAT = 'C'
CHEESE = 'Q'

# Movimientos (dy, dx) y teclas
MOVES = {
    'w': (-1, 0),
    's': (1, 0),
    'a': (0, -1),
    'd': (0, 1),
}

# ---------- Utilidades laberinto ----------
def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def neighbors(r, c):
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if in_bounds(nr, nc):
            yield nr, nc

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

# Genera un laberinto simple usando DFS aleatorio sobre celdas (genera paredes con densidad)
def generate_maze(seed=None):
    if seed is not None:
        random.seed(seed)
    # Start with all walls, carve passages using randomized DFS over cell grid
    grid = [[WALL for _ in range(COLS)] for __ in range(ROWS)]
    start = (0,0)
    stack = [start]
    grid[start[0]][start[1]] = EMPTY
    visited = {start}
    while stack:
        r,c = stack[-1]
        nbrs = [(nr,nc) for nr,nc in neighbors(r,c) if (nr,nc) not in visited]
        if not nbrs:
            stack.pop()
            continue
        nxt = random.choice(nbrs)
        nr,nc = nxt
        # carve straight path (we'll carve the neighbor cell)
        grid[nr][nc] = EMPTY
        visited.add((nr,nc))
        stack.append((nr,nc))
    # Add some random walls to increase complexity but ensure start-cheese connectivity
    attempts = int(ROWS*COLS*WALL_DENSITY)
    for _ in range(attempts):
        r = random.randrange(ROWS)
        c = random.randrange(COLS)
        if (r,c) in (MOUSE_START, CAT_START, CHEESE_POS):
            continue
        # don't add a wall if it disconnects mouse-cheese (we'll test)
        old = grid[r][c]
        grid[r][c] = WALL
        if not path_exists(grid, MOUSE_START, CHEESE_POS):
            grid[r][c] = old  # revert
    return grid

def path_exists(grid, a, b):
    # simple BFS
    if grid[a[0]][a[1]] == WALL or grid[b[0]][b[1]] == WALL:
        return False
    q = deque([a])
    seen = {a}
    while q:
        r,c = q.popleft()
        if (r,c) == b:
            return True
        for nr,nc in neighbors(r,c):
            if (nr,nc) not in seen and grid[nr][nc] != WALL:
                seen.add((nr,nc))
                q.append((nr,nc))
    return False

# ---------- Juego: representación del estado ----------
class GameState:
    def __init__(self, grid, mouse_pos, cat_pos):
        self.grid = grid
        self.mouse = mouse_pos
        self.cat = cat_pos

    def copy(self):
        return GameState([row[:] for row in self.grid], self.mouse, self.cat)

    def is_terminal(self):
        if self.mouse == CHEESE_POS:
            return True
        if self.cat == self.mouse:
            return True
        return False

    def winner(self):
        if self.mouse == CHEESE_POS:
            return 'mouse'
        if self.cat == self.mouse:
            return 'cat'
        return None

    def legal_moves(self, who):
        # who: 'mouse' or 'cat'
        r,c = self.mouse if who=='mouse' else self.cat
        res = []
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if in_bounds(nr,nc) and self.grid[nr][nc] != WALL:
                res.append((nr,nc))
        # allow "stay" as a move? Usually no — we disallow staying to force action
        return res

# ---------- Heurística (desde la perspectiva del GATO) ----------
def evaluate_state(state):
    # terminal checks
    if state.cat == state.mouse:
        return 1_000_000  # cat wins: very grande
    if state.mouse == CHEESE_POS:
        return -1_000_000 # mouse wins: muy negativo para el gato

    # distances
    d_mouse_cheese = manhattan(state.mouse, CHEESE_POS)
    d_cat_mouse = manhattan(state.cat, state.mouse)

    # combine in a way that larger is better for cat:
    max_dist = ROWS + COLS
    # cat prefers: mouse far from cheese (bigger d_mouse_cheese), and cat close to mouse (smaller d_cat_mouse)
    score = (d_mouse_cheese * 10) + ((max_dist - d_cat_mouse) * 8)
    # small tie-breaker: prefer states where cat is closer to cheese too (so cat can block)
    d_cat_cheese = manhattan(state.cat, CHEESE_POS)
    score += (max_dist - d_cat_cheese) * 1
    return score

# ---------- Minimax con poda alfa-beta ----------
def minimax(state, depth, alpha, beta, maximizing_player):
    # maximizing_player = True --> the cat to move (since evaluation is from cat perspective)
    if depth == 0 or state.is_terminal():
        return evaluate_state(state), None

    if maximizing_player:
        best_val = -math.inf
        best_move = None
        moves = state.legal_moves('cat')
        if not moves:
            # no moves for cat => evaluate
            return evaluate_state(state), None
        for mv in moves:
            child = state.copy()
            child.cat = mv
            val, _ = minimax(child, depth-1, alpha, beta, False)
            if val > best_val:
                best_val = val
                best_move = mv
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        return best_val, best_move
    else:
        # minimizing player: the mouse (from cat's perspective mouse wants to minimize this evaluation)
        best_val = math.inf
        best_move = None
        moves = state.legal_moves('mouse')
        if not moves:
            return evaluate_state(state), None
        for mv in moves:
            child = state.copy()
            child.mouse = mv
            val, _ = minimax(child, depth-1, alpha, beta, True)
            if val < best_val:
                best_val = val
                best_move = mv
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_val, best_move

def cat_choose_move_minimax(state):
    # run minimax from current state with cat to move
    _, move = minimax(state, MAX_DEPTH, -math.inf, math.inf, True)
    # if minimax had no move (shouldn't happen) fallback greedy
    if move is None:
        moves = state.legal_moves('cat')
        if not moves:
            return state.cat
        # greedy: minimize distance to mouse
        moves.sort(key=lambda p: manhattan(p, state.mouse))
        return moves[0]
    return move

# ---------- Dibujar tablero ----------
def draw(state):
    os.system('cls' if os.name=='nt' else 'clear')
    grid = [row[:] for row in state.grid]
    mr, mc = state.mouse
    cr, cc = state.cat
    qr, qc = CHEESE_POS
    grid[qr][qc] = CHEESE
    grid[mr][mc] = MOUSE
    grid[cr][cc] = CAT
    # print with coordinates optionally
    print("El laberinto del gato y el ratón (M = ratón, C = gato, Q = queso)")
    print("-" * (COLS + 2))
    for r in range(ROWS):
        print('|' + ''.join(grid[r]) + '|')
    print("-" * (COLS + 2))
    print("Controles: W=arriba, S=abajo, A=izquierda, D=derecha. Escribí 'q' para salir.")

# ---------- Bucle principal ----------
def main():
    # setup
    if SEED is not None:
        seed = SEED
    else:
        seed = int(time.time())
    random.seed(seed)

    # generate maze ensuring path from mouse to cheese
    attempts = 0
    while True:
        grid = generate_maze(seed=random.randrange(10**9))
        if path_exists(grid, MOUSE_START, CHEESE_POS) and path_exists(grid, CAT_START, CHEESE_POS):
            break
        attempts += 1
        if attempts > 200:
            # fallback: empty grid (shouldn't usually happen)
            grid = [[EMPTY for _ in range(COLS)] for __ in range(ROWS)]
            break

    state = GameState(grid, MOUSE_START, CAT_START)

    # game loop
    while True:
        draw(state)
        if state.is_terminal():
            w = state.winner()
            if w == 'mouse':
                print("¡El ratón alcanzó el queso! 🎉 Ganaste (ratón).")
            elif w == 'cat':
                print("El gato atrapó al ratón. 😿 Ganó el gato.")
            else:
                print("Fin de juego.")
            break

        # Turn: player (mouse) then cat (AI)
        # -- Player move
        move = None
        while True:
            key = input("Movimiento (W/A/S/D): ").strip().lower()
            if key == 'q':
                print("Saliendo...")
                sys.exit(0)
            if key not in MOVES:
                print("Tecla inválida. Usa W A S D o q para salir.")
                continue
            dr, dc = MOVES[key]
            nr = state.mouse[0] + dr
            nc = state.mouse[1] + dc
            if not in_bounds(nr,nc):
                print("Movimiento fuera de límites.")
                continue
            if state.grid[nr][nc] == WALL:
                print("Hay una pared ahí.")
                continue
            move = (nr,nc)
            break
        state.mouse = move

        # check terminal after mouse move
        if state.is_terminal():
            draw(state)
            continue

        # -- Cat (AI) move
        print("El gato está pensando...")
        cat_move = cat_choose_move_minimax(state)
        # small pause para experiencia
        time.sleep(0.4)
        state.cat = cat_move

    print("Juego terminado.")

if __name__ == "__main__":
    main()
