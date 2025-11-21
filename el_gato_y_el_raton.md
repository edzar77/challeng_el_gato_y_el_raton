# El laberinto del gato y el raton

Este proyecto implementa un laberinto donde un gato persigue a un ratón y el raton persigue alcanzar el queso utilizando codigos basicos y algoritmo minimax donde el gato es el max y el raton el mini

##  Características
- Tablero bidimencional de 16x16 basado en clases 
- El gato utiliza movimiento automático basado en el algoritmo minimax y el raton un monvimiento aleatorio dirigido al queso
- se ejecuta de forma automatica sin intervencion de jugadores 

## Qué funcionó, qué fue un desastre, y tu mejor "¡ajá!" durante el proceso.
- En este punto al momento de decidir por el tipo de matriz, me fue mas facil el tablero por clases. Con esta secuencia de codigos me fue mas practico poder ordenar, tanto el tablero como las pocisiones iniciales del gato, raton y queso.
- Al momento de realizar los movimientos tanto del gato como del raton utilice un while true que en un primer momento todos los movimientos fueron automaticos y aleatorios conforme a la codificacion.
- tambien hay que tener en cuenta que algunos codigos fueron proporcionados por los compañeros para la mejora de la presentacion, como ser el codigo que hace que no se esté duplicando el tablero con cada movimiento y el contador de turnos. 
- Por ultimo integre el algoritmo minimax, este si fue un desastre y tube que ser guiado por una AI para poder integrar y la integracion no salió como esperaba ya que al momento de ejecutar el gato en momentos no reconoce los obstaculos y tampoco la posicion del queso y va con todo contra el raton y el raton con la logica actual no se aleja del gato
- lo otro es que la poscion del gato, el raton y el queso su posicion son fijas y para que las posiciones sean aleatorias o sean ingresadas habría que agregar mas codigos
##  Cómo ejecutar
python minimax_lab.py
