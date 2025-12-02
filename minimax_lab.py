import os
import time

# Clase que representa el tablero del laberinto
class TableroLaberinto:
    def __init__(self,fila,columna):
        # Dimensiones del tablero
        self.fila = fila
        self.columna = columnagit push
        # Crea una matriz de puntos (.) vacíos
        self.tablero = [['.' for c in range(columna)]for f in range(fila)]

    # Retorna el valor de una celda
    def valor_de_tablero(self,fila,columna):
        return self.tablero[fila][columna]
    
    # Coloca una pared en la posición indicada
    def agregar_paredes(self,fila,columna):
        self.tablero[fila][columna] = '#'
    
    # Verifica si la celda NO es pared
    def sin_paredes(self,fila,columna):
        return self.tablero[fila][columna] != '#'
    
    # Retorna movimientos posibles desde una posición (arriba, abajo, izq, der)
    def posibilidades(self,pos):
        fila, columna = pos
        movimientos = []
        direcciones = [(-1,0),(1,0),(0,-1),(0,1)]  # 4 direcciones básicas
        
        for direcciones_fila, direcciones_columna in direcciones:
            nueva_fila, nueva_columna = fila + direcciones_fila, columna + direcciones_columna
            
            # Verifica límites del tablero
            if 0 <=nueva_fila < self.fila and 0 <= nueva_columna < self.columna:
                movimientos.append((nueva_fila,nueva_columna))
        
        return movimientos

    # Coloca al gato
    def inicio_gato(self,fila,columna):
        self.tablero[fila][columna] = 'G'
    
    # Coloca al ratón
    def inicio_raton(self,fila,columna):
        self.tablero[fila][columna] = 'R'

    # Coloca el queso
    def queso_pos(self,fila,columna):
        self.tablero[fila][columna] = 'Q'
    
    # Representación en texto del tablero
    def __str__(self):
        presentacion = ''
        for fila in range(self.fila):
            for columna in range(self.columna):
                presentacion += self.tablero[fila][columna]
            presentacion += '\n'
        return presentacion
    
    # Verifica si una posición está dentro del tablero
    def dentro_tablero(self,pos):
        return 0 <= pos[0] < self.fila and 0 <= pos[1] < self.columna

    # Distancia Manhattan entre ratón y gato
    def distancia_manhattan(self,raton_pos,gato_pos):
        return abs(raton_pos[0]- gato_pos[0]) + abs(raton_pos[1]-gato_pos[1])
    
    # Evalúa una situación del tablero para el minimax
    def evaluar(self,gato_pos,raton_pos,queso_pos):
        # Si el gato atrapa al ratón → mejor para el gato
        if gato_pos == raton_pos:
            return 1000
        # Si el ratón llega al queso → mejor para el ratón
        if raton_pos == queso_pos:
            return -1000
        
        # Calcula distancias
        distancia_raton_queso = self.distancia_manhattan(raton_pos,queso_pos)
        distancia_gato_raton = self.distancia_manhattan(gato_pos,raton_pos)
        
        # Mientras más cerca esté el ratón del queso, menor puntaje
        puntaje_queso = 500 - distancia_raton_queso*10
        # Mientras más cerca esté el gato del ratón, mayor puntaje
        puntaje_gato = 500 - distancia_gato_raton*10
            
        return puntaje_queso + puntaje_gato        
        
    # No se usa activamente, pero calcula un valor para movimientos del gato
    def ver_movimientos_gato(self,posicion_actual_gato,posicion_actual_raton,profundidad,gato_pos,raton_pos):
        if posicion_actual_gato == gato_pos:
            return 1000
        if posicion_actual_raton == raton_pos:
            return 1000
        distancia = self.distancia_manhattan(posicion_actual_gato,posicion_actual_raton)
        return distancia
    
    # Algoritmo Minimax para elegir la jugada del gato o del ratón
    def minimax(self,gato_pos,raton_pos,profundidad,es_turno_gato,queso_pos):
        # Condiciones terminales
        if profundidad == 0 or gato_pos == raton_pos or raton_pos == queso_pos:
            return self.evaluar(gato_pos,raton_pos,queso_pos)
        
        if es_turno_gato:
            # El gato intenta maximizar la puntuación
            max_eval = -float('inf')
            for cada_movimiento_gato in self.posibilidades(gato_pos):
                score = self.minimax(cada_movimiento_gato,raton_pos,profundidad-1,False,queso_pos)
                max_eval = max(max_eval,score)
            return max_eval
        else:
            # El ratón intenta minimizar la puntuación
            min_eval = float('inf')
            for cada_movimiento_raton in self.posibilidades(raton_pos):
                score = self.minimax(gato_pos,cada_movimiento_raton,profundidad-1,True,queso_pos)
                min_eval = min(min_eval,score)
            return min_eval


# ---------------------------
# CONFIGURACIÓN INICIAL
# ---------------------------

mi_tablero = TableroLaberinto(16,16)
mi_tablero.inicio_gato(0,0)
mi_tablero.inicio_raton(15,15)
mi_tablero.queso_pos(3,5)

# Agrega paredes
mi_tablero.agregar_paredes(4,4)
mi_tablero.agregar_paredes(3,2)
mi_tablero.agregar_paredes(6,7)
mi_tablero.agregar_paredes(5,2)
mi_tablero.agregar_paredes(10,4)
mi_tablero.agregar_paredes(2,4)
mi_tablero.agregar_paredes(11,3)
mi_tablero.agregar_paredes(14,7)
mi_tablero.agregar_paredes(13,2)
mi_tablero.agregar_paredes(10,8)
mi_tablero.agregar_paredes(0,1)
mi_tablero.agregar_paredes(1,3)
mi_tablero.agregar_paredes(2,10)
mi_tablero.agregar_paredes(3,7)
mi_tablero.agregar_paredes(4,12)
mi_tablero.agregar_paredes(5,9)
mi_tablero.agregar_paredes(6,14)
mi_tablero.agregar_paredes(7,5)
mi_tablero.agregar_paredes(8,11)
mi_tablero.agregar_paredes(9,6)
mi_tablero.agregar_paredes(10,13)
mi_tablero.agregar_paredes(11,9)
mi_tablero.agregar_paredes(12,4)
mi_tablero.agregar_paredes(13,10)
mi_tablero.agregar_paredes(14,3)
mi_tablero.agregar_paredes(15,2)
mi_tablero.agregar_paredes(8,2)
mi_tablero.agregar_paredes(12,12)
mi_tablero.agregar_paredes(7,14)
mi_tablero.agregar_paredes(1,11)

print(mi_tablero)

# Estado inicial de personajes
raton_fila = 15
raton_columna = 15
gato_fila = 0
gato_columna = 0
queso_pos = (3,5)

historial_movimientos = []

turno_gato = False   # Empieza moviendo el ratón
contador=0

# ---------------------------
# BUCLE PRINCIPAL DEL JUEGO
# ---------------------------

while True:
    
    # Limpia posición previa del ratón (si no está en el queso)
    if (raton_fila,raton_columna) != queso_pos:
        mi_tablero.tablero[raton_fila][raton_columna] = '.'
    
    # Limpia posición previa del gato
    mi_tablero.tablero[gato_fila][gato_columna] = '.'
    
    # -------------------- TURNO DEL GATO --------------------
    if turno_gato:  
        mejor_movimiento = None
        mejor_valor = -float('inf')
        
        # Recorre todas las posibilidades del gato y usa minimax
        for mov in mi_tablero.posibilidades((gato_fila,gato_columna)):
            val = mi_tablero.minimax(mov,(raton_fila,raton_columna), 2,False,queso_pos)
            if val > mejor_valor:
                mejor_valor = val
                mejor_movimiento = mov
        
        # Actualiza posición del gato
        if mejor_movimiento is not None:
            gato_fila,gato_columna = mejor_movimiento
    
    # -------------------- TURNO DEL RATÓN --------------------
    else:
        # Movimiento "directo" : se acerca al queso
        if raton_fila > queso_pos[0] and mi_tablero.sin_paredes(raton_fila -1,raton_columna):
            raton_fila -= 1
        elif raton_fila < queso_pos[0] and mi_tablero.sin_paredes(raton_fila +1,raton_columna):
            raton_fila += 1
        
        elif raton_columna > queso_pos[1] and mi_tablero.sin_paredes(raton_fila,raton_columna -1):
            raton_columna -= 1
        elif raton_columna < queso_pos[1] and mi_tablero.sin_paredes(raton_fila,raton_columna +1):
            raton_columna += 1
    
    # Cambia el turno
    turno_gato = not turno_gato
    
    # Vuelve a colocar a los personajes
    mi_tablero.queso_pos(*queso_pos)
    mi_tablero.tablero[raton_fila][raton_columna] = 'R'
    mi_tablero.tablero[gato_fila][gato_columna] = 'G'    

    historial_movimientos.append({
        "raton": (raton_fila,raton_columna),
        "gato": (gato_fila,gato_columna)
    })
    
    # Limpia pantalla y muestra tablero
    os.system('cls' if os.name == 'nt' else 'clear')
    contador += 1
    print(f'turno: {contador}')
    print(mi_tablero)
        
    # Condiciones de victoria
    if (raton_fila,raton_columna) == queso_pos:
        print('ganaste el juego')
        break
    
    if (gato_fila,gato_columna) == (raton_fila,raton_columna):
        print('perdiste el juego')
        break
    
    time.sleep(2.5)

