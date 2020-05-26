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
import sys
import controller 
import csv
from ADT import list as lt
from ADT import stack as stk
from ADT import orderedmap as map
from DataStructures import listiterator as it
from DataStructures import orderedmapstructure as tree
import sys


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido al Laboratorio 9")
    print("1- Cargar información")
    print("2- Req 1 ")
    print("3- Req 2")
    print("4- Req 3")
    print("5- Req 4")
    print("6- Nada")
    print("0- Salir")


def initCatalog ():
    """
    Inicializa el catalogo
    """
    return controller.initCatalog()


def loadData (catalog):
    """
    Carga las bibliotecas en la estructura de datos
    """
    controller.loadData(catalog)


"""
Menu principal 
""" 
def main():
    while True: 
        printMenu()
        inputs =input("Seleccione una opción para continuar\n")
        if int(inputs[0])==1:
            print("Cargando información de los archivos ....")
            catalog = initCatalog ()
            loadData (catalog)
            t = tree.size(catalog['date_city_trips'])
            print('Arbol',t)
            g = controller.countNodesEdgesGraph(catalog)
            print('Vertices grafo: ',g[0],' Ejes grafo: ',g[1])
        elif int(inputs[0])==2:
            city = input('Ingrese nombre de la ciudad: ')
            controller.stationsByDockCount(catalog, city)
            
        elif int(inputs[0])==3:
            dates = input('Ingrese las fechas del intervalo (ej: 8/29/2013 1/1/2014) \n')
            dat1 = dates.split(" ")[0]
            dat2 = dates.split(" ")[1]
            r = controller.trips_per_dates(catalog,dat1,dat2)
            for city  in r:
                print (city, r[city])

        elif int(inputs[0])==4:
            r = catalog['list_temperature']
            print(r)
            
        elif int(inputs[0])==5:
            vertices =input("Ingrese el vertice origen y destino. (Ejemplo: '48-2014-2-27 66-2014-2-27')\n")
            path = controller.getShortestPath(catalog,vertices)
            if path == 'No hay camino' or path == 'No existen los vértices':
                print (path)
            else:
                print("El camino de menor costo entre los vertices es:")
                totalDist = 0
                while not stk.isEmpty (path): 
                    step = stk.pop(path)
                    totalDist += step['weight']
                    print (step['vertexA'] + "-->" + step['vertexB'] + " costo: " + str(step['weight']))
                print ("Total: " + str (totalDist))
            
        
        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    main()