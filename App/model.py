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
    #stationNameId = map.newMap(capacity=70, prime=37, maptype='CHAINING',comparefunction=compareByKey)
    #Creamos un RBT indexado por fechas, el value es un map con ciudades y cantidad de viajes
    date_city_trips = tree.newMap('RBT')
    #Creamos una lista para que contiene dia, temperatura y cantidad de viajes en ese dia 
    list_temperature = lt.newList('ARRAY_LIST')
    #Creamos un grafo de viajes por fecha
    trips_digraph = g.newGraph(44679,compareByKey,directed=True,datastructure="ADJ_LIST")
    #Se crea el catálogo
    catalog = {'cities':cityStationsMap, 'stationIds': stationIdName, 'date_city_trips':date_city_trips, 'list_temperature':list_temperature, 'tripsGraph': trips_digraph }    
    return catalog

def addDate_temperature (catalog,row):
    '''
    Función que crea una lista de diccionarios de fechas con la temperatura y la cantidad de viajes asociada a partir del árbol de fechas
    '''
    dicc_date = {}
    value = 0
    a = (row['date']).split(sep="-")
    temperature = float(row['mean_temperature_f'])
    date_string = str(a[1]) + '/'+str(a[2])+'/'+str(a[0])
    date = strToDate(date_string, "%m/%d/%Y")
    w = tree.get(catalog['date_city_trips'],date,greater)
    keys = map.keySet(w)
    keysIterator = it.newIterator(keys)
    while it.hasNext(keysIterator):
        city = it.next(keysIterator)
        count = int(map.get(w,city)['value'])
        value += count
    dicc_date = {'Date':date_string,'Temperature':temperature,'Cantidad_viajes': value}
    lt.addLast(catalog['list_temperature'],dicc_date)

def sortDate_temperature(catalog):
    '''
    Función que ordena la lista de diccionarios con fecha, temperatura y cantidad de viajes, usando fecha como criterio de ordenamiento. 
    '''
    list_temp = catalog['list_temperature']
    mergesort.mergesort(list_temp,compareTemperatureGreater)

def consulta_temperature(catalog, n):
    '''
    Función que devuelve los N días con la mayor y menor temperatura
    '''
    N = int(n)
    list_temperatures = catalog['list_temperature']
    response_max = lt.newList('ARRAY_LIST')
    response_min = lt.newList('ARRAY_LIST')
    for i in range(1,N+1) :
        g = lt.getElement(list_temperatures,i)
        lt.addLast(response_max,g)
    s = int(lt.size(list_temperatures))
    for i in range(s-N,s):
        f = lt.getElement(list_temperatures,i)
        lt.addFirst(response_min,f)
    return (response_max,response_min)

def addCityStations (catalog, row):
    '''
    Función que va construyendo un mapa de ciudades, añadiendo a cada ciudad una lista con sus estaciones respectivas. 
    Cada estación contiene un diccionario con su ID, Nombre, y Dock Count.
    '''
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

    #stationsNameId = catalog['stationNames']
    #map.put(stationNameId,row['name'],row['id'])

def stationsByDockCount(catalog, city):
    '''
    Función que retorna las 3 estaciones con más Dock Count para una ciudad que entra como input
    '''
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
    '''
    Función que ordena la lista de estaciones para cada ciudad por dock cont de mayor a menor
    '''
    #Iteramos sobre toda las ciudades para ir ordenando las listas de estaciones por dock_count
    cityStationsMap = catalog['cities']
    citiesList = map.keySet(cityStationsMap)
    citiesIterator = it.newIterator(citiesList)
    while it.hasNext(citiesIterator):
        city = it.next(citiesIterator)
        stationsList = map.get(cityStationsMap,city)['value']
        mergesort.mergesort(stationsList,compareDockCountGreater)

def station_id_city (catalog,station_id) :
    '''
    Función que devuelve la ciudad en la que está ubicada una estación, recibiendo como input el id de la estación
    '''
    # Funcion auxiliar a addDate_city_trips que me devuelve la ciudad a partir del id de una estacion 
    stations_ids = catalog['stationIds']
    y = map.get(stations_ids,station_id)
    city = y['value']['City']
    return city 


def addDate_city_trips(catalog,row):
    '''
    Función que construye el árbol RBT de fechas. Cada nodo del árbol es a su vez un mapa de hash con cantidad de viajes indexados por ciudad
    '''
    # Añadimos las fechas al RBT con un value igual a un map con ciudad y values =  cantidad de viajes

    d = row['start_date'] # row del archivo trip.csv 
    t = d.split(" ")[0]
    date = strToDate(t,'%m/%d/%Y')
    #print(date)
    id_station = row['start_station_id']
    city_trip = tree.get(catalog['date_city_trips'],date,greater)
    #print(city_trip)
    city = station_id_city(catalog,id_station)
    if city_trip :
        if map.contains(city_trip,city):
            u = map.get(city_trip,city)['value']  
            u += 1
            map.put(city_trip,city,u)
            catalog['date_city_trips'] = tree.put(catalog['date_city_trips'],date,city_trip,greater)

        else :
            map.put(city_trip,city,1)
            catalog['date_city_trips'] = tree.put(catalog['date_city_trips'],date,city_trip,greater)
    else :
        city_trip = map.newMap(capacity= 5, prime=3,maptype='CHAINING', comparefunction = compareByKey)
        map.put(city_trip,city,1)
        catalog['date_city_trips'] = tree.put(catalog['date_city_trips'],date,city_trip,greater)

def addTripDay_Edges(catalog, row):
    '''
    Función que va creando un grafo dirigido de viajes añadiendo cada vértice y eje 
    '''
    addVertex(catalog,row)
    addEdge(catalog,row)

def addVertex(catalog, row):
    '''
    Función que añade los vértices al grafo de viajes si no existen
    '''
    if not g.containsVertex(catalog['tripsGraph'], row['src']):
        g.insertVertex(catalog['tripsGraph'], row['src'])
    if not g.containsVertex(catalog['tripsGraph'], row['dst']):
        g.insertVertex(catalog['tripsGraph'],row['dst'])

def addEdge(catalog, row):
    '''
    Función que añade los ejes al grafo de viajes
    '''
    if row['duration'] != "":
        g.addEdge (catalog['tripsGraph'], row['src'], row['dst'], float(row['duration']))

def countNodesEdgesGraph(catalog):
    """
    Retorna la cantidad de nodos y enlaces del grafo de viajes
    """
    tripsGraph=catalog['tripsGraph']
    nodes = g.numVertex(tripsGraph)
    edges = g.numEdges(tripsGraph)

    return nodes,edges

def getShortestPath (catalog, source, dst):
    """
    Retorna el camino de menor costo entre vertice origen y destino, si existe 
    """
    graph = catalog['tripsGraph']
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

def trips_per_dates (catalog, init_date, last_date):
    '''
    Función que responde el requerimiento 2; para un rango de fechas devuelve la cantidad de viajes totales por ciudad
    '''
    # Esta es la que usamos para responder el req 2 , se devulve un dict con llaves = ciudades y value = suma de todas las cantidades

    response = {}
    date_1 = strToDate(init_date, '%m/%d/%Y')
    date_2 = strToDate(last_date, '%m/%d/%Y')
    range_list = tree.valueRange(catalog['date_city_trips'],date_1,date_2,greater)
    #print(range_list)
    #print(type(range_list))
    iterator_range = it.newIterator(range_list)
    while it.hasNext(iterator_range):
        Element = it.next(iterator_range)
        elkeys=map.keySet(Element)
        iterator_keys = it.newIterator(elkeys)
        while it.hasNext(iterator_keys):
            city = it.next(iterator_keys) 
            count = map.get(Element,city)['value']
            if city in response :
                r = response[city]
                w = r + count
                response[city] = w
            else :
                response[city] = count
                
    return response

    
# Funciones de comparacion
def compareDockCountGreater( element1, element2):
        if int(element1['dock_count']) >  int(element2['dock_count']):
            return True
        return False
def compareTemperatureGreater (element1, element2):
    if float(element1['Temperature']) > float(element2['Temperature']):
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
