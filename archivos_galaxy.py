import json
import re
def crear_json(ruta):
    data = {}
    data["puntajes"] = []
    data["puntajes"].append({
        "nombre": "luis",
        "puntos": 100
    })
    data["puntajes"].append({
        "nombre": "jose",
        "puntos": 200
    })
    with open(ruta, 'a') as archivo:
        json.dump(data, archivo, indent = 4)

ruta = "galaxy.json"
#crear_json(ruta)        

def parse_puntaje(ruta:str)->list:
    i = 0
    with open(ruta,'r') as archivo:
        lista_puntos = []
        todo = archivo.read()
        nombre = re.findall(r'"nombre": "([a-zA-Z0_9]+)', todo)
        puntos = re.findall(r'"puntos": ([0-9]+)', todo)

        for i in range(len(nombre)):
            dic_puntajes = {}
            dic_puntajes["nombre"] = nombre[i]
            dic_puntajes["puntos"] = int(puntos[i])
            lista_puntos.append(dic_puntajes)
            i += 1
    return lista_puntos   

def guardar_json(ruta:str, lista:list)->None:
    with open(ruta, 'w') as archivo:
        json.dump(lista, archivo, indent=4) 

def agregar_jugador(lista,nombre,puntos):
    dic = {}
    dic["nombre"]= nombre
    dic["puntos"]= puntos
    lista.append(dic)
    return lista

def ordenar_lista(lista: list, key: str) -> list:
    bandera_swap = True
    while bandera_swap == True:
        bandera_swap = False
        for i in range(len(lista)-1):
            if lista[i][key] > lista[i+1][key]:
                auxiliar = lista[i]
                lista[i] = lista[i+1]
                lista[i+1] = auxiliar
                bandera_swap = True
    for element in lista:
        print(element['nombre'], element[key])
    return lista    

def mostrar_top5(lista:list)->list:
    lista_top5 = []
    i = 0
    
    for elemento in lista:
        if i < 5:
            lista_top5.append(elemento)
            i += 1
    return lista_top5       

# lista = [1,2,3,4,5,6,7]            
# lista_top = mostrar_top5(lista)
# print(lista_top)