"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 *
 * Adaptado del desarrollo para el curso ISIS1225 - Estructuras de Datos y Algoritmos
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
import model
import csv
from ADT import list as lt
from ADT import map as map


from DataStructures import listiterator as it
from Sorting import mergesort as sort
from time import process_time


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Funcionaes utilitarias

def printList (lst):
    iterator = it.newIterator(lst)
    while  it.hasNext(iterator):
        element = it.next(iterator)
        result = "".join(str(key) + ": " + str(value) + ". " for key, value in element.items())
        print (result)


# Funciones para la carga de datos 

def loadStationsFile (catalog):
    """
    Carga las estaciones del archivo.
    Se almacena un mapa de estaciones indexado por el id de estación. Se almacena un mapa de ciudades con sus respectivas estaciones.
    """
    t1_start = process_time() #tiempo inicial
    stationsFile = cf.data_dir + 'bikes_data/station.csv'
    dialect = csv.excel()
    dialect.delimiter=','
    with open(stationsFile, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        for row in spamreader:
            #print(row)
            model.addCityStations(catalog, row)        
    model.sortCityStations(catalog)

    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución carga archivo estaciones:",t1_stop-t1_start," segundos")  
 
def load_tripFile (catalog):
    t1_start = process_time() #tiempo inicial
    stationsFile = cf.data_dir + 'bikes_data/trip.csv'
    dialect = csv.excel()
    dialect.delimiter=','
    with open(stationsFile, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        for row in spamreader:
            model.addDate_city_trips(catalog, row)        
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución carga archivo viajes :",t1_stop-t1_start," segundos") 

def stationsByDockCount(catalog, city):
    t1_start = process_time()
    try:
        stations=model.stationsByDockCount(catalog, city)
        printList(stations)
    except: print('Verifique el nombre de la ciudad')
    t1_stop = process_time()
    print("Tiempo de ejecución estaciones con más parqueos por ciudad:",t1_stop-t1_start," segundos")  

def trips_per_dates(catalog,init,last):
    t1_start = process_time()
    s = model.trips_per_dates(catalog,init,last)
    t1_stop = process_time()
    print("Tiempo de ejecución cantidad de viajes por ciudad entre fechas :",t1_stop-t1_start," segundos")
    return s 

def loadEdgesFile(catalog):
    t1_start=process_time()
    edgesFile = cf.data_dir+'tripxday_edges/tripday_edges.csv'
    dialect = csv.excel()
    dialect.delimiter=';'
    with open(edgesFile,encoding="utf-8-sig") as csvfile:
        spamreader=csv.DictReader(csvfile, dialect=dialect)
        for row in spamreader:
            model.addTripDay_Edges(catalog, row)
    t1_stop=process_time()
    print('Tiempo de ejecución carga grafo de viajes por fechas: ',t1_stop-t1_start,' segundos')

def loadTemperatureFile (catalog):
    """
    Carga las temperaturas del archivo.
    Se almacena una lista con la info necesaria para el req 3 
    """
    t1_start = process_time() #tiempo inicial
    stationsFile = cf.data_dir + 'bikes_data/weather.csv'
    dialect = csv.excel()
    dialect.delimiter=','
    with open(stationsFile, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        for row in spamreader:
            model.addDate_temperature(catalog,row)
    model.sortDate_temperature(catalog)      
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución carga archivo de temperaturas:",t1_stop-t1_start," segundos")  

def initCatalog ():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog



def loadData (catalog):
    """
    Carga los datos de los archivos en la estructura de datos
    """
    loadStationsFile(catalog)  
    load_tripFile(catalog)
    loadTemperatureFile(catalog)
    loadEdgesFile(catalog)
    

# Funciones llamadas desde la vista y enviadas al modelo


def countNodesEdges_non_directed(catalog):
    
    nodes, edges = model.countNodesEdges_non_directed(catalog)
   
    
    return nodes, edges

def countNodesEdgesGraph(catalog):
    
    nodes, edges = model.countNodesEdgesGraph(catalog)
    
    return nodes, edges

def countConnectedComponents(catalog):
    t1_start = process_time() #tiempo inicial
    ccs = model.componentes_conectados(catalog) 
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución de conteo de componentes conectados:",t1_stop-t1_start," segundos")
    return ccs

def getPath(catalog, vertices, strct):
    t1_start = process_time() #tiempo inicial
    source=vertices.split(" ")[0]
    dst=vertices.split(" ")[1]
    path = model.getPath(catalog, source, dst,strct)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución de ",strct," ",t1_stop-t1_start," segundos")
    return path

def getShortestPath(catalog, vertices):
    t1_start = process_time() #tiempo inicial
    source=vertices.split(" ")[0]
    dst=vertices.split(" ")[1]
    path = model.getShortestPath(catalog, source, dst)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución de dijkstra: ",t1_stop-t1_start," segundos")
    return path

