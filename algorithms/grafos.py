from math import inf
from os import system

# Clase para guardar matrices de adhyacencia
class Grafo:
    # Recibe una lista de nodos y la matriz en sí
    def __init__(self, elementos:list, matrix:list):
        self.elementos = elementos
        self.matrix = matrix

        # Si alguna dimension de la matriz no coincide con la cantidad de nodos, imprime error
        if len(self.matrix) != len(self.elementos):
            print("Matrix doesn't contain the same amount of rows as elements declared...")

        for el in self.matrix:
            if len(el) != len(self.elementos):
                print("A row doesn't have the same declared amount of elements...")

    # Método para convertir a cadena la matriz
    def __str__(self):
        string = '\t\t'
        
        for el in self.elementos:
            string += f'{el}{" "*(14-len(f"{el}"))}'
        
        for i in range(len(self.elementos)):
            string += f'\n{self.elementos[i]}{" "*(16-len(f"{self.elementos[i]}"))}'

            for j in range(len(self.matrix[i])):
                string += f'{self.matrix[i][j]}{" "*(14-len(f"{self.matrix[i][j]}"))}'
    
        return string

    # Obtiene la fila de adhyacencia de un nodo específico
    def getElementRow(self, element):
        for i in range(len(self.elementos)):
            if self.elementos[i] == element:
                return self.matrix[i]
        
        return None

# Como se guarda un nodo en la tabla de mapeo
class NodoMapeo:
    # Contiene un nombre, el costo para llegar desde el origen, la ruta por la que se llega
    def __init__(self, nombre, costo=inf, origen=None):
        self.nombre = nombre
        self.costo = costo
        self.origen = origen
    
    # Metodo para convertir a cadena
    def __str__(self):
        return f'{self.nombre}{" "*(16-len(f"{self.nombre}"))}{self.costo if self.costo != inf else '--'}\t{self.origen if self.origen != None else '--'}'

# Tabla de mapeo con el algoritmo de dijkstra
class TablaMapeo:
    # Recibe una matriz de adhyacencia
    def __init__(self, nodos:Grafo):
        self.nodos = []         # Lista de NodoMapeo que contendrá la tabla final
        self.priorityList = []  # Lista de NodoMapeo, es la lista de nodos que faltan por evaluar

        # Forzosamente se debe recibir una matriz de adhyacencia
        if type(nodos) == type(Grafo([1], [[1]])):
            self.grafo = nodos  # Guarda la matriz

            # Guarda cada nodo de la matriz en la lista de nodos
            for el in nodos.elementos:
                self.nodos.append(NodoMapeo(el))

    # Metodo para imprimir en forma de cadena
    def __str__(self):
        string = 'Nodo\t\tCosto\tOrigen'

        for el in self.nodos:
            string += f'\n{el}'

        return string
    
    # Regresa una lista con la ruta que se debe recorrer para llegar a un destino
    def findPath(self, dest):
        # Extrae el nodo
        nodo = self.findNodo(dest)
        steps = []

        # Recorre todos los nodos de regreso al origen
        while nodo.origen != None and nodo.costo != 0:
            steps.append(nodo.nombre)
            nodo = self.findNodo(nodo.origen)

        steps.append(nodo.nombre)

        # Invierte el listado para iniciar desde el origen
        steps.reverse()

        return steps
    
    # Busca un nodo por valor en la tabla final
    def findNodo(self, valor):
        for el in self.nodos:
            if el.nombre == valor:
                return el
        
        return None
    
    # Busca un nodo por valor en la lista de prioridad aka nodos no evaluados
    def findNodoInPL(self, valor):
        for el in self.priorityList:
            if el.nombre == valor:
                return el
        
        return None
    
    # Reinicia los valores de las listas para poder iniciar el algoritmo de dijkstra
    def resetNodos(self):
        self.priorityList = []

        for el in self.nodos:
            el.costo = inf
            el.origen = None
    
    # Criterio por el que se acomodan los nodos en la lista de prioridad: costo
    def sortCrit(self, nodo):
        return nodo.costo

    # Ejecuta el alrgoritmo para encontrar el camino más corto
    def dijkstra(self, origen):
        self.resetNodos()

        # Busca el punto de origen y le establece un costo de 0
        o = self.findNodo(origen)

        if o == None:
            print("Nodo de origen inexistente...")
            return

        o.costo = 0

        # Copia la lista de nodos en la lista de prioridad
        self.priorityList = self.nodos.copy()

        # Mientras la lista de prioridad tenga elementos
        while len(self.priorityList):
            self.priorityList.sort(key=self.sortCrit) # Acomoda la lista según los costos
            nodo = self.priorityList.pop(0) # Extrae el primer elemento

            row = self.grafo.getElementRow(nodo.nombre).copy() # Obtiene las conexiones del elemento extraido

            # Para cada elemento de las conexiones del elemento extraido
            for i in range(len(row)):
                # Hace infinitos los puntos a los que no puede llegar
                if row[i] == 0:
                    row[i] = inf
                
                # Determina el costo que tomaría del punto de origen al nodo seleccionado
                costo = row[i] + nodo.costo

                # Revisa si el elemento sigue en la lista de prioridad
                n = self.findNodoInPL(self.nodos[i].nombre)

                # Si el elemento no se ha evaluado y obtiene un costo menor
                if n != None and costo < self.nodos[i].costo:
                    # Establece un nuevo costo y origen para el nodo
                    self.nodos[i].costo = costo
                    self.nodos[i].origen = nodo.nombre
                    
                    n.costo = costo
                    n.origen = nodo.nombre


# Trata un grafo para buscar un camino de inicio a fin
def evalGrafo(tabla:TablaMapeo):
    entry1 = None
    start = None

    entry2 = None
    end = None

    # Recibe el nodo inicial
    while start == None:
        print(tabla.grafo)
        entry1 = input("Introduce un nodo de inicio: ")

        if type(tabla.nodos[0].nombre) == type(1):
            entry1 = eval(entry1)

        start = tabla.findNodo(entry1)

        system("clear")

        if start == None:
            print("No se encontró el nodo...")

    # Busca las rutas partiendod del nodo elegido
    tabla.dijkstra(entry1)

    # Obtiene el nodo destino
    while end == None:
        print(tabla)
        entry2 = input("Introduce el nodo final: ")

        if type(tabla.nodos[0].nombre) == type(1):
            entry2 = eval(entry2)

        end = tabla.findNodo(entry2)

        system("clear")

        # En caso de elegir el mismo nodo o uno inexistente
        if end == None:
            print("No se encontró el nodo...")
        elif entry2 == entry1:
            print("Ya estás en ese nodo...")
            end = None
    
    
    print(tabla)
    print()

    # Si no se puede llegar al nodo
    if end.costo == inf and end.origen == None:
        print("No se puede acceder a ese nodo...")
    else:
        print(f"Total de pasos: {end.costo}")
        path = tabla.findPath(entry2)
        
        for i in range(len(path)):
            if i:
                print(' -> ', end='')
            
            print(path[i], end='')
    
    input("\n\nPresiona <enter> para continuar.")
    system("clear")

if __name__ == '__main__':
    # Grafo de pruebas
    gEJ = Grafo(['Nashville', 'Memphis', 'Atlanta', 'New Orleans', 'Movile', 'Savannah'], 
        [[0,15,2,0,0,0], 
        [15,0,10,3,7,0], 
        [2,10,0,0,2,1], 
        [0,3,0,0,3,0], 
        [0,7,2,3,0,6], 
        [0,0,1,0,6,0]])
    tEJ = TablaMapeo(gEJ)

    # Grafo IV
    gIV = Grafo([1,2,3,4,5,6,7], [[0,0,3,0,0,0,0], [3,0,0,0,0,0,0], [0,0,0,0,3,2,0], [0,0,0,0,0,0,2], [0,0,0,0,0,0,0], [0,0,0,0,0,0,1], [0,0,2,0,0,0,0]])
    tIV = TablaMapeo(gIV)

    # Grafo V
    gV = Grafo([1,2,3,4,5,6], [[0,1,3,0,0,0],[0,0,0,0,0,0],[0,2,0,0,0,7],[0,0,0,0,0,0],[4,0,0,5,0,0],[0,0,0,6,0,0]])
    tV = TablaMapeo(gV)

    # Grafo VII
    gVII = Grafo(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'], 
        [[0,7,2,6,0,0,0,9,0], 
        [7,0,6,0,0,0,0,0,0], 
        [2,6,0,1,3,0,0,0,0], 
        [6,0,1,0,0,0,0,5,0], 
        [0,0,3,0,0,2,8,0,1], 
        [0,0,0,0,2,0,3,0,0], 
        [0,0,0,0,8,3,0,0,0], 
        [9,0,0,5,0,0,0,0,0], 
        [0,0,0,0,1,0,0,0,0]])
    tVII = TablaMapeo(gVII)

    evalGrafo(tEJ)
    evalGrafo(tIV)
    evalGrafo(tV)
    evalGrafo(tVII)