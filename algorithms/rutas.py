from grafos import TablaMapeo

rutas = TablaMapeo('./Ciudades_Aeroibero.csv')
grafo = rutas.grafo

matrix = grafo.getMatrix()
crit = grafo.getCryteria()

print(grafo)

rutas_totales = []

for c in crit:
    ruta = []

    for el in matrix[c]:
        rutas.dijkstra(c, el)

        for em in matrix[c]:
            r = rutas.findPath(em)

            if len(r) > 1:
                ruta.append(r)
    
    rutas_totales.append(ruta)
    
    print(c)
    for el in ruta:
        print(el)
    print()