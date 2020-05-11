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
        elif int(inputs[0])==2:
            city = input('Ingrese nombre de la ciudad: ')
            controller.stationsByDockCount(catalog, city)
            
        elif int(inputs[0])==3:
            com_con=controller.countConnectedComponents(catalog)
            print('El grafo tiene: ',com_con,"componentes conectados")
        elif int(inputs[0])==4:
            vertices =input("Ingrese el vertice origen y destino (EJEMPLO: HNL-1-25 ICT-1-25 ) \n")
            lst = controller.getPath(catalog,vertices,'dfs')
            print("El camino entre los vertices es:")
            if lst is not None:
                lst_it = it.newIterator(lst)
                route=''
                while it.hasNext(lst_it):
                    city = it.next(lst_it)
                    route += city + " "
                print (route)
            else:
                print('\nNo hay camino para los vértices ingresados\n')
            
        elif int(inputs[0])==5:
            vertices =input("Ingrese el vertice origen y destino (EJEMPLO: HNL-1-25 ICT-1-25 ) \n")
            lst = controller.getPath(catalog,vertices,'bfs')
            print("El camino entre los vertices es:")
            if lst is not None:
                lst_it = it.newIterator(lst)
                route=''
                while it.hasNext(lst_it):
                    city = it.next(lst_it)
                    route += city + " "
                print (route)
            else:
                print('\nNo hay camino para los vértices ingresados\n')
        elif int(inputs[0])==6:
            vertices =input("Ingrese el vertice origen y destino. (Ejemplo: 'ALB-5-12 LAX-5-12')\n")
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