import pandas as pd
from math import inf
from os import system

class Grafo:
    def __init__(self, ruta:str=None):
        if not ruta:
            return
        
        # Leer el archivo
        self.__dataset = pd.read_csv(ruta)

        # Obtener todos loas puntos de origen y de destino
        origenes = self.__dataset['Origen'].unique()
        destinos = self.__dataset['Destino'].unique()

        self.__missing_origenes = []
        self.__missing_destinos = []

        # Obtener los puntos que son mencionados en una columna pero no en la otra para agregarlos
        for origen in origenes:
            if origen not in destinos:
                self.__missing_destinos.append(origen)
                self.__dataset.loc[len(self.__dataset)] = [origen, origen, None, inf, inf, inf]

        for destino in destinos:
            if destino not in origenes:
                self.__missing_origenes.append(destino)
                self.__dataset.loc[len(self.__dataset)] = [destino, destino, None, inf, inf, inf]
        
        # Mensaje de advertencia
        # if len(self.__missing_origenes):
        #     print("Warning: some destinations are not listed in the origins row, they were aded to the adjacency matrix.")
        # if len(self.__missing_destinos):
        #     print("Warning: some origins are not listed in the destination row, they were aded to the adjacency matrix.")

        # Crea 3 matrices de origenes y destinos considerando la distancia, el tiempo y el costo
        # Las acomoda para tener la forma de una matriz de adyacencia
        # Esto genera 3 matrices de adyacencia en una, con 3 diferentes costos: distancia, tiempo y precio listas para operarse con Djikstra
        self.__matrix = self.__dataset.pivot(index='Origen', columns='Destino', values=['Distancia (Km)', 'Tiempo total (Hrs)', 'Costo total']).sort_index()
        self.__matrix.fillna(inf, inplace=True)

    # Impresión como cadena
    def __str__(self):
        string = ''
        
        crit = self.getCryteria()

        # Imprime por separado cada tabla por criterio
        for el in crit:
            string += f'{el}:\n{self.__matrix[el]}\n\n'

        return string

    # Obtiene todos los criterios por los que se evalua
    def getCryteria(self):
        crit = []
        for el in self.__matrix.columns.values:
            if el[0] not in crit:
                crit.append(el[0])
        
        return crit
    
    # Obtiene el elemento 'element' en la matriz del criterio 'field'
    def getElementRow(self, field, element):
        return self.__matrix.loc[element][field].values
    
    # Obtiene la matriz de adyacencia
    def getMatrix(self):
        return self.__matrix
    
    # Obtiene el dataset original
    def getDataSet(self):
        return self.__dataset

# Como se guarda un nodo en la tabla de mapeo
class NodoMapeo:
    # Contiene un nombre, el costo para llegar desde el origen, la ruta por la que se llega
    def __init__(self, nombre, costo=inf, origen=None):
        self.nombre = nombre
        self.costo = costo
        self.origen = origen
    
    # Metodo para convertir a cadena
    def __str__(self):
        origen = self.origen if self.origen != None else '--'
        costo = self.costo if self.costo != inf else '--'

        return f'{self.nombre}{" "*(20-len(f"{self.nombre}"))}{costo}{" "*(20-len(f'{costo}'))}{origen}'

class NodoRuta:
    def __init__(self, origen, destino, costos:dict):
        self.origen = origen
        self.destino = destino
        self.costos = costos
    
    def __str__(self):
        string = f'{self.origen} -> {self.destino}:\n'

        for k, v in self.costos.items():
            string += f'\t{k}: {v}\n'
        
        return string
    
    # Método para comparar    
    def __eq__(self, other):
        if not isinstance(other, NodoRuta):
            return False
        
        return self.origen == other.origen and self.destino == other.destino

# Tabla de mapeo con el algoritmo de dijkstra
class TablaMapeo:
    # Recibe una matriz de adhyacencia o la ruta al archivo csv
    def __init__(self, nodos:Grafo|str):
        self.nodos = []         # Lista de NodoMapeo que contendrá la tabla final
        self.priorityList = []  # Lista de NodoMapeo, es la lista de nodos que faltan por evaluar

        # guarda el grafo según el argumento de entrada
        if type(nodos) == type(Grafo()):
            self.grafo = nodos
        elif type(nodos) == type('a'):
            self.grafo = Grafo(nodos)

        matrix = self.grafo.getMatrix()

        # Guarda cada nodo de la matriz en la lista de nodos
        for i in range(len(matrix)):
            self.nodos.append(NodoMapeo(matrix.iloc[i].name))

    # Metodo para imprimir en forma de cadena
    def __str__(self):
        string = 'Nodo' + ' '*16 + 'Costo' + ' '*15 + 'Origen'

        for el in self.nodos:
            string += f'\n{el}'

        return string

    # Busca un nodo por valor en la tabla final
    def findNodo(self, valor):
        for el in self.nodos:
            if el.nombre == valor:
                return el
        
        return None
    
    # Regresa una lista con la ruta que se debe recorrer para llegar a un destino
    def findPath(self, dest):
        # Extrae el nodo
        matrix = self.grafo.getMatrix()
        crit = self.grafo.getCryteria()

        c = False

        for el in self.nodos:
            if not (el.origen == None and el.costo == inf):
                c = True

        if c:
            nodo = self.findNodo(dest)
            steps = []
            resumen = []

            # Recorre todos los nodos de regreso al origen
            while nodo.origen != None and nodo.costo != 0:
                steps.append(nodo)
                nodo = self.findNodo(nodo.origen)

            steps.append(nodo)

            for i in range(len(steps) - 1):
                costos = {}

                for el in crit:
                    costos[el] = matrix[el].loc[steps[i].origen].loc[steps[i].nombre]
                
                resumen.append(NodoRuta(steps[i].origen, steps[i].nombre, costos))

            # Invierte el listado para iniciar desde el origen
            steps.reverse()
            resumen.reverse()

            return steps, resumen
        else:
            print('Warning: Routes are not generated yet...')
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
    def dijkstra(self, field, origen):
        self.resetNodos()

        # Busca el punto de origen y le establece un costo de 0
        o = self.findNodo(origen)

        if o == None:
            print("Warning: Couldn't find origin node...")
            return

        o.costo = 0

        # Copia la lista de nodos en la lista de prioridad
        self.priorityList = self.nodos.copy()

        # Mientras la lista de prioridad tenga elementos
        while len(self.priorityList):
            self.priorityList.sort(key=self.sortCrit) # Acomoda la lista según los costos
            nodo = self.priorityList.pop(0) # Extrae el primer elemento

            row = self.grafo.getElementRow(field, nodo.nombre).copy() # Obtiene las conexiones del elemento extraido

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
    def evalGrafo(tabla):
        entry0 = None
        
        entry1 = None
        start = None

        entry2 = None
        end = None

        # Listado de criterios para considerar costos
        crit = tabla.grafo.getCryteria()

        # Recibe el criterio a considerar
        while entry0 == None:
            for el in crit:
                print(el)

            entry0 = input('Introduce un criterio de costo: ')

            system('clear')

            if entry0 not in crit:
                print("El criterio mencionado no existe...")
                entry0 = None

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
        tabla.dijkstra(entry0, entry1)

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
            print(f"{entry0}: {end.costo}")
            path = tabla.findPath(entry2)
            
            for i in range(len(path)):
                if i:
                    print(' -> ', end='')
                
                print(path[i], end='')
        
        input("\n\nPresiona <enter> para continuar.")
        system("clear")
