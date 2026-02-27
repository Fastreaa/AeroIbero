from grafos import TablaMapeo
from os import system

##########################################
# Generación de todas las rutas posibles #
##########################################

# Carga la información del csv
rutas = TablaMapeo('../Ciudades_Aeroibero.csv')
grafo = rutas.grafo

# Obtiene la matriz de adyacencia y los criterios de búsqueda
matrix = grafo.getMatrix()
crit = grafo.getCryteria()

# Diccionario de rutas por criterio
# Cada criterio tendrá una lista con todas las rutas posibles
# Las rutas constan de una tupla con los pasos a recorrer con un desglose de costos y
# un resumen de los puntos a visitar
rutas_totales = {}

# Para cada criterio de búsqueda
for c in crit:
    ruta = [] # Lista de rutas del criterio

    # Para cada elemento en la matriz de adyacencia con el criterio
    for el in matrix[c]:
        rutas.dijkstra(c, el) # Genera la tabla de mapeo del elemento

        for em in matrix[c]: # Busca el camino más corto para los demás elementos
            s, r = rutas.findPath(em) # Obtiene el desglose y el resumen

            # Si se puede llear de {el} a {em}, agrega la tupla a la lista
            if len(s) > 1:
                ruta.append((s, r))

    # Guarda las rutas del criterio en el diccionario
    rutas_totales[c] = ruta


##################################
# Evaluación de rutas y destinos #
##################################

v = False # Origen y destino válidos
origen = None # Punto de origen
destino = None # Punto destino
criterio = None # Criterio de búsqueda

i = 0 # Contador
optima = True # Si todas las rutas siguen los mismos puntos

# Mientras no haya un origen y un destino válidos
while not v:
    v = True

    # Obtiene y valida el origen
    while origen == None:
        origen = input("Introduce la ciudad de origen: ")
        system('clear')

        if origen not in matrix[crit[0]]:
            print("El origen no existe...")    
            origen = None

    # Obtiene y valida el destino
    while destino == None:
        destino = input("Introduce la ciudad de destino: ")
        system('clear')

        if destino not in matrix[crit[0]]:
            print("El destino no existe...")
            destino = None

    # Diccionario de las rutas del origen al destino por criterio
    rutas_criterio = {}

    # Revisa que se pueda llegar del origen al destino
    for c in crit:
        i = 0

        while i < len(rutas_totales[c]) and not (rutas_totales[c][i][0][0].nombre == origen and rutas_totales[c][i][0][-1].nombre == destino):
            i += 1

        if i < len(rutas_totales[c]):
            rutas_criterio[c] = rutas_totales[c][i]
    
    # Si no se puede llegar al destino, marcar error
    if not len(rutas_criterio):
        print("No se encpntró una ruta del origen al destino...")
        v = False
    else:
        # Revisa si las rutas de los diferentes criterios pasan por los mismos puntos
        for s1, r1 in rutas_criterio.items():
            for s2, r2 in rutas_criterio.items():
                if s1 != s2:
                    for j in range(len(r1[1])):
                        if j >= len(r2[1]) or r1[1][j] != r2[1][j]:
                            optima = False

# Si todos los criterios pasan por los mismos puntos, ruta óptima
if optima:
    print("El sistema encontró la ruta óptima!")
    
    for el in rutas_criterio[crit[0]][1]:
        print(el)
else:
    # De lo contrario, valida el criterio deseado
    while criterio == None:
        criterio = input("Introduce el criterio de búsqueda: ")
        system('clear')

        if criterio not in crit:
            print("El criterio no existe...")
            criterio = None

    # Imprime el desglose de la ruta según el criterio
    for el in rutas_criterio[criterio][1]:
        print(el)
