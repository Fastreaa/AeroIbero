from grafos import TablaMapeo
from os import system

# Carga la información del csv
rutas = TablaMapeo('../Ciudades_Aeroibero.csv')
grafo = rutas.grafo

# Obtiene la matriz de adyacencia y los criterios de búsqueda
matrix = grafo.getMatrix()
crit = grafo.getCryteria()


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

        # Busca el mismo origen/destino en las 3 categorias
        while i < len(rutas.rutas_totales[c]) and not (rutas.rutas_totales[c][i][0][0].nombre == origen and rutas.rutas_totales[c][i][0][-1].nombre == destino):
            i += 1

        # Si encontró el elemenento, lo guarda
        if i < len(rutas.rutas_totales[c]):
            rutas_criterio[c] = rutas.rutas_totales[c][i]
    
    # Si no se puede llegar al destino, marcar error
    if not len(rutas_criterio):
        print("No se encontró una ruta del origen al destino...")
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
