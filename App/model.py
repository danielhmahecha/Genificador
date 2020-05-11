"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
from ADT import list as lt
from ADT import graph as g
from ADT import map as map
from ADT import list as lt
from Sorting import mergesort 
from DataStructures import listiterator as it
from datetime import datetime
from DataStructures import dijkstra as dk
from DataStructures import dfs as dfs 
from DataStructures import bfs as bfs 

"""
Se define la estructura de un catálogo de libros.
El catálogo tendrá tres listas, una para libros, otra para autores 
y otra para géneros
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo y retorna el catalogo inicializado.
    """
    #Creamos un mapa de ciudades
    cityStationsMap = map.newMap(capacity=5, prime=3,maptype='CHAINING',comparefunction=compareByKey)
    #Creamos un mapa de nombres de estaciones indexadas por Id de estación, para facilitar la carga de los datos de los otros archivos
    stationIdName = map.newMap(capacity=70, prime=37, maptype='CHAINING',comparefunction=compareByKey)
    
    #Se crea el catálogo
    catalog = {'cities':cityStationsMap, 'stationIds': stationIdName}    
    return catalog
    
def addCityStations (catalog, row):
    #Vamos actualizando el mapa de ciudades, añadiendo la estación a la ciudad respectiva
    cityStationsMap = catalog['cities']
    station = {'id': row['id'], 'name': row['name'], 'dock_count': row['dock_count']}
    if  map.contains(cityStationsMap,row['city']) == False:
        stationsList = lt.newList(datastructure='ARRAY_LIST')
        lt.addLast(stationsList,station) 
        map.put(cityStationsMap,row['city'],stationsList)
    if map.contains(cityStationsMap,row['city']) == True:
        stationsList = map.get(cityStationsMap,row['city']) ['value']
        lt.addLast(stationsList,station) 
        map.put(cityStationsMap,row['city'],stationsList)  

    #Añadimos la estación al mapa de ids y nombres de las estaciones
    stationsIdName = catalog['stationIds']
    map.put(stationsIdName,row['id'],row['name'])

def stationsByDockCount(catalog, city):
    try:
        ans = lt.newList()
        cityStationsMap = catalog['cities']
        stationsList = map.get(cityStationsMap,city)['value']
        c=1
        while c<=3:
            station=lt.getElement(stationsList,c)
            element={'Nombre': station['name'], 'Dock Count': station['dock_count']}
            lt.addLast(ans,element)
            c+=1
        return ans
    except: print('Ciudad no encontrada')
def sortCityStations(catalog):
    #Iteramos sobre toda las ciudades para ir ordenando las listas de estaciones por dock_count
    cityStationsMap = catalog['cities']
    citiesList = map.keySet(cityStationsMap)
    citiesIterator = it.newIterator(citiesList)
    while it.hasNext(citiesIterator):
        city = it.next(citiesIterator)
        stationsList = map.get(cityStationsMap,city)['value']
        mergesort.mergesort(stationsList,compareDockCountGreater)

def addReviewNode_non_directed (catalog, row):
    """
    Adiciona un nodo para almacenar un libro o usuario 
    """
    if not g.containsVertex(catalog['non_directed_Graph'], row['SOURCE']):
        g.insertVertex (catalog['non_directed_Graph'], row['SOURCE'])
    if not g.containsVertex(catalog['non_directed_Graph'], row['DEST']):
        g.insertVertex (catalog['non_directed_Graph'], row['DEST'])

def addReviewEdge_non_directed (catalog, row):
    """
    Adiciona un enlace para almacenar una revisión
    """
    if row['AIR_TIME'] != "":
        g.addEdge (catalog['non_directed_Graph'], row['SOURCE'], row['DEST'], float(row['AIR_TIME']))


def addReviewNode_directed (catalog, row):
    """
    Adiciona un nodo para almacenar un libro o usuario 
    """
    if not g.containsVertex(catalog['directed_Graph'], row['SOURCE']):
        g.insertVertex (catalog['directed_Graph'], row['SOURCE'])
    if not g.containsVertex(catalog['directed_Graph'], row['DEST']):
        g.insertVertex (catalog['directed_Graph'], row['DEST'])

def addReviewEdge_directed (catalog, row):
    """
    Adiciona un enlace para almacenar una revisión
    """
    if row['AIR_TIME'] != "":
        g.addEdge (catalog['directed_Graph'], row['SOURCE'], row['DEST'], float(row['AIR_TIME']))


def countNodesEdges_non_directed (catalog):
    """
    Retorna la cantidad de nodos y enlaces del grafo de bibliotecas
    """
    nodes = g.numVertex(catalog['non_directed_Graph'])
    edges = g.numEdges(catalog['non_directed_Graph'])

    return nodes,edges
def countNodesEdges_directed (catalog):
    """
    Retorna la cantidad de nodos y enlaces del grafo de bibliotecas
    """
    nodes = g.numVertex(catalog['directed_Graph'])
    edges = g.numEdges(catalog['directed_Graph'])

    return nodes,edges

def componentes_conectados(catalog):
    counter = 0
    grafo = catalog['non_directed_Graph']
    vertices = g.vertices(grafo)
    graph_iter = it.newIterator (vertices)
    m = map.newMap(capacity= 55681,maptype='CHAINING',comparefunction=grafo['comparefunction']) 
    while (it.hasNext (graph_iter)):
        n = it.next (graph_iter)
        visited_w = map.get(m, n)
        if visited_w == None :
            dfs.newDFS_2(grafo,n,m)
            counter += 1
    return counter

def getPath (catalog, source, dest, strct):
    """
    Retorna el camino, si existe, entre vertice origen y destino
    """
    path = None
    if g.containsVertex(catalog['non_directed_Graph'],source) and g.containsVertex(catalog['non_directed_Graph'],dest):
        #print("vertices: ",source,", ", dest)
        if strct == 'dfs':
            search = dfs.newDFS(catalog['non_directed_Graph'],source)
            path = dfs.pathTo(search,dest)
        if strct == 'bfs':
            search = bfs.newBFS(catalog['non_directed_Graph'],source)
            path = bfs.pathTo(search, dest)
    # ejecutar dfs desde source
    # obtener el camino hasta dst
    # retornar el camino

    return path



def getShortestPath (catalog, source, dst):
    """
    Retorna el camino de menor costo entre vertice origen y destino, si existe 
    """
    graph = catalog['directed_Graph']
    print("vertices: ",source,", ",dst)
    if g.containsVertex(graph, source) and g.containsVertex(graph, dst):
        dijks = dk.newDijkstra(graph,source)
        if dk.hasPathTo(dijks, dst):
            path = dk.pathTo(dijks,dst)
        else:
            path = 'No hay camino'
    else:
        path = 'No existen los vértices'

    return path
    # ejecutar Dijkstra desde source
    # obtener el camino hasta dst
    # retornar el camino
    
   # return None
    
# Funciones de comparacion
def compareDockCountGreater( element1, element2):
        if int(element1['dock_count']) >  int(element2['dock_count']):
            return True
        return False

def compareByKey (key, element):
    return  (key == element['key'] )  

