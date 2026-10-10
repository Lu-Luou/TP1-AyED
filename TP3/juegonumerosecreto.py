import os
import pickle
import random

class Categorias:
    def __init__(self):
        self.Nrocategoria = 0
        self.Nombrecategoria = " " * 30
        self.Pregunta = " " * 200
        self.Estado = "A"

class Opciones:
    def __init__(self):
        self.Nrocategoria = 0
        self.Nroopcion = 0
        self.Objeto = " " * 100
        self.Valor = 0

class Jugadores:
    def __init__(self):
        self.Nombrejug = " " * 30
        self.Creditos = 10000.0
        self.Juegos = [[0] * 4 for i in range(2)]

def pedir_nombre():
    nombre_ingresado = input("Ingrese su nombre: ").strip()
    while nombre_ingresado == "" or nombre_ingresado.isdigit() or len(nombre_ingresado) > 30:
        if nombre_ingresado == "":
            print("Error: el nombre no puede estar vacio.")
        elif nombre_ingresado.isdigit():
            print("Error: el nombre no puede ser solo un numero.")
        else:
            print("Error: el nombre no puede superar los 30 caracteres.")
        nombre_ingresado = input("Ingrese su nombre: ").strip()
    return nombre_ingresado

def abrir_archivo(ruta_archivo):
    if os.path.exists(ruta_archivo):
        archivo_abierto = open(ruta_archivo, "r+b")
    else:
        archivo_abierto = open(ruta_archivo, "w+b")
    return archivo_abierto

def apertura():
    global arLoJug
    arLoJug = abrir_archivo(arFiJug)

def cierre():
    arLoJug.close()

def busquedajug(nombre_buscado):
    arLoJug.flush()
    tam_jug = os.path.getsize(arFiJug)
    pos_encontrada = -1
    arLoJug.seek(0)
    while arLoJug.tell() < tam_jug and pos_encontrada == -1:
        pos_inicio_jug = arLoJug.tell()
        reg_jug_leido = pickle.load(arLoJug)
        if reg_jug_leido.Nombrejug.strip().lower() == nombre_buscado.strip().lower():
            pos_encontrada = pos_inicio_jug
    return pos_encontrada


def altajug(nombre_nuevo):
    reg_jug_nuevo = Jugadores()
    reg_jug_nuevo.Nombrejug = nombre_nuevo.ljust(30)
    arLoJug.seek(0, 2)
    pos_alta = arLoJug.tell()
    pickle.dump(reg_jug_nuevo, arLoJug)
    arLoJug.flush()
    return pos_alta

def leer_jugador(pos_jug_leer):
    arLoJug.seek(pos_jug_leer, 0)
    reg_jug_devuelto = pickle.load(arLoJug)
    return reg_jug_devuelto

MAX_INTENTOS = 5
arFiJug = "c:\\tp3\\jugadores.dat"
apertura()
os.system("cls")
print("\033[4m\033[91mNÚMERO SECRETO\033[0m")
nom = pedir_nombre()
pos = busquedajug(nom)
if pos == -1:
    pos = altajug(nom)
numero_secreto=random.randint(1,100)
intentos=MAX_INTENTOS
ganador= False
while(intentos > 0 and ganador==False):
    print("Usted tiene",intentos,"intentos")
    numero = input("Ingrese un número entre 1 y 100: ")
    while not numero.isdigit() or int(numero) < 1 or int(numero) > 100:
        numero=input("Por favor, ingrese un número válido entre 1 y 100: ")
    numero=int(numero)
    intentos=intentos-1
    if numero==numero_secreto:
        ganador=True
    else:
        if numero > numero_secreto:
            print("El número secreto es menor")
        else:
            print("El número secreto es mayor")
    if ganador==True:
        print("¡¡Enhorabuena " + nom + "! Ganaste en " + str(MAX_INTENTOS - intentos) + " intentos. El número secreto era", numero_secreto)
        arLoJug.seek(pos,0)
        reg=pickle.load(arLoJug)
        reg.Juegos[0][1]=reg.Juegos[0][1]+1
        arLoJug.seek(pos,0)
        pickle.dump(reg,arLoJug)
        arLoJug.flush()
    else:
        if intentos==0:
            print("Oh no, perdiste el juego")
            print("El número secreto era", numero_secreto)
            arLoJug.seek(pos,0)
            reg=pickle.load(arLoJug)
            reg.Juegos[1][1]=reg.Juegos[1][1]+1
            arLoJug.seek(pos,0)
            pickle.dump(reg,arLoJug)
            arLoJug.flush()
input("Presione Enter para continuar...")
cierre()