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
from DataStructures import orderedmapstructure as tree
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
    #Creamos un RBT indexado por fechas, el value es un map con ciudades y cantidad de viajes
    date_city_trips = tree.newMap('RBT')
    #Se crea el catálogo
    catalog = {'cities':cityStationsMap, 'stationIds': stationIdName, 'date_city_trips':date_city_trips }    
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

    #Añadimos la estación al mapa de ids con value de  nombres de las estaciones y su ciudad 
    stationsIdName = catalog['stationIds']
    dicct = {'Name' : row['name'], 'City': row['city']}
    map.put(stationsIdName,row['id'],dicct)

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

def station_id_city (catalog,station_id) :
    # Funcion auxiliar a addDate_city_trips que me devuelve la ciudad a partir del id de una estacion 
    stations_ids = catalog['stationIds']
    y = map.get(stations_ids,station_id)
    city = y['value']['City']
    return city 


def addDate_city_trips(catalog,row):
    # Añadimos las fechas al RBT con un value igual a un map con ciudad y values =  cantidad de viajes

    d = row['start_date'] # row del archivo trip.csv 
    date = strToDate(d,'%m-%d-%Y')
    id_station = row['start_station_id']
    city_trip = tree.get(catalog['date_city_trips'],date,greater)
    print(city_trip)
    city = station_id_city(catalog,id_station)
    if city_trip :
        u = map.get(city_trip,city)['value']  
        u += 1
        map.put(city_trip,city,u)
    else :
        city_trip = map.newMap(capacity= 5, prime=3,maptype='CHAINING', comparefunction = compareByKey)
        map.put(city_trip,city,1)
        tree.put(catalog['date_city_trips'],date,city_trip,greater)

def trips_per_dates (catalog, init_date, last_date):
    # Esta es la que usamos para responder el req 2 , se devulve un dict con llaves = ciudades y value = suma de todas las cantidades

    response = {}
    date_1 = strToDate(init_date, '%m-%d-%Y')
    date_2 = strToDate(last_date, '%m-%d-%Y')
    range_list = tree.valueRange(catalog['date_city_trips'],date_1,date_2,greater)
    iterator_range = it.newIterator(range_list)
    while it.hasNext(range_list):
        Element = it.next(iterator_range)
        key = tree.get(catalog['date_city_trips'],Element,greater)['value']
        k_lst = map.keySet(key)
        iterator_key = it.newIterator(k_lst)
        while it.hasNext(iterator_key):
            f_key = it.next(iterator_key) 
            city = map.get(Element,f_key)
            v = city['value']
            f = city['key']
            if f in response :
                r = response[f]
                w = r + v
                response[f] = w
            else :
                response[f] = v 
    return response


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

def greater (key1, key2):
    if ( key1 == key2):
        return 0
    elif (key1 < key2):
        return -1
    else:
        return 1

# Funciones auxiliares 
def strToDate(date_string, format):
    try:
        # date_string = '2016/05/18 13:55:26' -> format = '%Y/%m/%d %H:%M:%S')
        return datetime.strptime(date_string,format)
    except:
        return datetime.strptime('1900', '%Y')
