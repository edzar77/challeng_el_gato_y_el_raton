import os
import time

class   TableroLaberinto:
    def __init__(self,fila,columna):
        self.fila = fila
        self.columna = columna 
        self.tablero = [['.' for c in range(columna)]for f in range(fila)]

    def valor_de_tablero(self,fila,columna):
        return self.tablero[fila][columna]
    
    def agregar_paredes(self,fila,columna):
        self.tablero[fila][columna] = '#'
    
    def sin_paredes(self,fila,columna):
        return self.tablero[fila][columna] in ('.','Q')

    #Inicializar posiciones: G=(gf,gc), R=(rf,rc), Q=(qf,qc).
    def inicio_gato(self,fila,columna):
        self.tablero[fila][columna] = 'G'

    def inicio_raton(self,fila,columna):
        self.tablero[fila][columna] = 'R'

    def queso_pos(self,fila,columna):
        self.tablero[fila][columna] = 'Q'
    
    def __str__(self):
        presentacion = ''
        for fila in range(self.fila):
            for columna in range(self.columna):
                presentacion += self.tablero[fila][columna]
            presentacion += '\n'
        return presentacion

mi_tablero = TableroLaberinto(16,16)
mi_tablero.inicio_gato(1,1)
mi_tablero.inicio_raton(13,6)
mi_tablero.queso_pos(8,5,)


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

print(mi_tablero)

raton_fila = 13
raton_columna = 6
gato_fila = 1
gato_columna = 1
queso_pos = (8,5)
historial_movimientos = []

contador=0

while True:
    
    if (raton_fila,raton_columna) != queso_pos:
        mi_tablero.tablero[raton_fila][raton_columna] = '.'
    
    mi_tablero.tablero[gato_fila][gato_columna] = '.'
    
    
    print(f'turno: {contador}')
    
    if raton_fila > queso_pos [0] and mi_tablero.sin_paredes(raton_fila -1,raton_columna):
        raton_fila -= 1
    elif raton_fila < queso_pos [0] and mi_tablero.sin_paredes(raton_fila +1,raton_columna):
        raton_fila += 1
        
    if raton_columna > queso_pos [1] and mi_tablero.sin_paredes(raton_fila,raton_columna -1):
        raton_columna -= 1
    elif raton_columna < queso_pos [1] and mi_tablero.sin_paredes(raton_fila,raton_columna +1):
        raton_columna += 1
        
    if gato_fila > raton_fila and mi_tablero.sin_paredes(gato_fila -1,gato_columna):
        gato_fila -= 1
    elif gato_fila < raton_fila and mi_tablero.sin_paredes(gato_fila +1,gato_columna):
        gato_fila += 1
    
    if gato_columna > raton_columna and mi_tablero.sin_paredes(gato_fila,gato_columna -1):
        gato_columna -= 1
    elif gato_columna < raton_columna and mi_tablero.sin_paredes(gato_fila,gato_columna +1):
        gato_columna += 1
    
    mi_tablero.queso_pos(*queso_pos)
    mi_tablero.tablero[raton_fila][raton_columna] = 'R'
    mi_tablero.tablero[gato_fila][gato_columna] = 'G'    

    historial_movimientos.append({
        "raton": (raton_fila,raton_columna),
        "gato": (gato_fila,gato_columna)
    })
    
    os.system('cls'if os.name == 'nt' else 'clear')
    contador += 1
    print(f'turno: {contador}')
    print(mi_tablero)
        
    if (raton_fila,raton_columna) == queso_pos:
        print('ganaste el juego')
        break
    
    if (gato_fila,gato_columna) == (raton_fila,raton_columna):
        print('perdiste el juego')
        break
    
    time.sleep(3.5)


    
