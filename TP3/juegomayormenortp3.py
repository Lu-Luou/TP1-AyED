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

def abrir_archivo(ruta_archivo):
    if os.path.exists(ruta_archivo):
        archivo_abierto = open(ruta_archivo, "r+b")
    else:
        archivo_abierto = open(ruta_archivo, "w+b")
    return archivo_abierto

def apertura():
    global arLoCate, arLoOpc, arLoJug
    arLoCate = abrir_archivo(arFiCa)
    arLoOpc = abrir_archivo(arFiOpc)
    arLoJug = abrir_archivo(arFiJug)

def cierre():
    arLoCate.close()
    arLoOpc.close()
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

def registrar_resultado(pos_jug_grabar, monto_resultado, gano_partida):
    arLoJug.seek(pos_jug_grabar, 0)
    reg_jug_actualizado = pickle.load(arLoJug)
    reg_jug_actualizado.Creditos = reg_jug_actualizado.Creditos + monto_resultado
    if gano_partida:
        reg_jug_actualizado.Juegos[0][0] = reg_jug_actualizado.Juegos[0][0] + 1
    else:
        reg_jug_actualizado.Juegos[1][0] = reg_jug_actualizado.Juegos[1][0] + 1
    arLoJug.seek(pos_jug_grabar, 0)
    pickle.dump(reg_jug_actualizado, arLoJug)
    arLoJug.flush()


def contar_activas():
    arLoCate.flush()
    tam_cate_cont = os.path.getsize(arFiCa)
    cant_activas = 0
    arLoCate.seek(0, 0)
    while arLoCate.tell() < tam_cate_cont:
        reg_cate_cont = pickle.load(arLoCate)
        if reg_cate_cont.Estado == "A":
            cant_activas = cant_activas + 1
    return cant_activas

def muestracategorias():
    arLoCate.flush()
    tam_cate_muestra = os.path.getsize(arFiCa)
    arLoCate.seek(0, 0)
    while arLoCate.tell() < tam_cate_muestra:
        reg_cate_muestra = pickle.load(arLoCate)
        if reg_cate_muestra.Estado == "A":
            print(reg_cate_muestra.Nrocategoria, "-", reg_cate_muestra.Nombrecategoria.strip())

def busqueda_categoria(nro_cate_buscada, solo_activas):
    arLoCate.flush()
    tam_cate_busq = os.path.getsize(arFiCa)
    pos_cate_encontrada = -1
    arLoCate.seek(0, 0)
    while arLoCate.tell() < tam_cate_busq and pos_cate_encontrada == -1:
        pos_inicio_cate = arLoCate.tell()
        reg_cate_busq = pickle.load(arLoCate)
        if reg_cate_busq.Nrocategoria == nro_cate_buscada:
            if not solo_activas or reg_cate_busq.Estado == "A":
                pos_cate_encontrada = pos_inicio_cate
    return pos_cate_encontrada

def contar_opciones(nro_cate_contar):
    arLoOpc.flush()
    tam_opc_cont = os.path.getsize(arFiOpc)
    cant_opciones = 0
    arLoOpc.seek(0, 0)
    while arLoOpc.tell() < tam_opc_cont:
        reg_opc_cont = pickle.load(arLoOpc)
        if reg_opc_cont.Nrocategoria == nro_cate_contar:
            cant_opciones = cant_opciones + 1
    return cant_opciones


def determinaropciones(nro_cate_sorteo, es_primera):
    global Posiciones_opciones, cantidad_opc
    if es_primera == True:
        arLoOpc.flush()
        tam_opc_sorteo = os.path.getsize(arFiOpc)
        indice_carga = 0
        arLoOpc.seek(0, 0)
        while arLoOpc.tell() < tam_opc_sorteo:
            pos_inicio_opc = arLoOpc.tell()
            reg_opc_sorteo = pickle.load(arLoOpc)
            if reg_opc_sorteo.Nrocategoria == nro_cate_sorteo:
                Posiciones_opciones[indice_carga] = pos_inicio_opc
                indice_carga = indice_carga + 1
        cantidad_opc = indice_carga
    casillero = random.randint(0, cantidad_opc - 1)
    while Posiciones_opciones[casillero] == -1:
        casillero = random.randint(0, cantidad_opc - 1)
    arLoOpc.seek(Posiciones_opciones[casillero], 0)
    opcion_sorteada = pickle.load(arLoOpc)
    Posiciones_opciones[casillero] = -1
    return opcion_sorteada

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

def pedir_apuesta(saldo_disponible):
    texto_apuesta = input("¿Cuantos creditos desea apostar? ").strip()
    apuesta_valida = False
    while not apuesta_valida:
        if not texto_apuesta.isdigit():
            print("Error: ingrese un numero entero positivo.")
            texto_apuesta = input("¿Cuantos creditos desea apostar? ").strip()
        elif int(texto_apuesta) == 0 or int(texto_apuesta) > saldo_disponible:
            print("Error: la apuesta debe ser mayor a 0 y no superar su saldo de", saldo_disponible)
            texto_apuesta = input("¿Cuantos creditos desea apostar? ").strip()
        else:
            apuesta_valida = True
    apuesta_entera = int(texto_apuesta)
    return apuesta_entera

def pedir_categoria():
    print("Categorias")
    muestracategorias()
    texto_cate = input("Selecciona una categoria para iniciar el juego: ").strip()
    while not texto_cate.isdigit() or busqueda_categoria(int(texto_cate), True) == -1:
        texto_cate = input("Categoria invalida, elegi una de la lista: ").strip()
    nro_cate_valida = int(texto_cate)
    return nro_cate_valida

def pedir_eleccion(opcion_izq, opcion_der):
    texto_eleccion = input("1- " + opcion_izq.Objeto.strip() + "  /  2- " + opcion_der.Objeto.strip() + ": ").strip()
    while texto_eleccion != "1" and texto_eleccion != "2":
        print("Error: debe ingresar 1 o 2.")
        texto_eleccion = input("1- " + opcion_izq.Objeto.strip() + "  /  2- " + opcion_der.Objeto.strip() + ": ").strip()
    eleccion_numero = int(texto_eleccion)
    return eleccion_numero

def preguntar_continuar():
    texto_continuar = input("¿Desea volver a jugar? (S/N): ").strip().upper()
    while texto_continuar != "S" and texto_continuar != "N":
        print("Error: ingrese S o N.")
        texto_continuar = input("¿Desea volver a jugar? (S/N): ").strip().upper()
    return texto_continuar

arFiCa = "c:\\tp3\\categorias.dat"
arFiOpc = "c:\\tp3\\opciones.dat"
arFiJug = "c:\\tp3\\jugadores.dat"
Posiciones_opciones = [-1] * 100
cantidad_opc = 0
apertura()
nom = pedir_nombre()
pos = busquedajug(nom)
if pos == -1:
    pos = altajug(nom)
reg = leer_jugador(pos)
continuar = "S"
while reg.Creditos > 0 and continuar == "S":
    print()
    print("Saldo actual:", reg.Creditos)
    if contar_activas() == 0:
        print("No hay categorias activas. Un administrador debe dar de alta alguna.")
        continuar = "N"
    else:
        apuesta = pedir_apuesta(reg.Creditos)
        cat_elegida = pedir_categoria()
        if contar_opciones(cat_elegida) < 7:
            print("Esa categoria tiene menos de 7 opciones y no se puede jugar.")
            print("Un administrador debe agregar mas opciones.")
            continuar = "N"
        else:
            poscate = busqueda_categoria(cat_elegida, True)
            arLoCate.seek(poscate, 0)
            regcate = pickle.load(arLoCate)
            nombrecate = regcate.Nombrecategoria.strip()
            preguntacate = regcate.Pregunta.strip()
            op1 = determinaropciones(cat_elegida, True)
            op2 = determinaropciones(cat_elegida, False)
            correctas = 0
            rondas = 0
            while rondas != 6:
                print()
                print("Ronda", rondas + 1, "de 6 -", nombrecate)
                print(preguntacate)
                eleccion = pedir_eleccion(op1, op2)
                rondas = rondas + 1
                print("1-", op1.Objeto.strip(), op1.Valor, "/ 2-", op2.Objeto.strip(), op2.Valor)
                if (eleccion == 1 and op1.Valor >= op2.Valor) or (eleccion == 2 and op2.Valor >= op1.Valor):
                    print("La respuesta es correcta!!!")
                    correctas = correctas + 1
                else:
                    print("Ups... la respuesta es incorrecta...")
                if rondas != 6:
                    input("Presione Enter para continuar...")
                    if op1.Valor >= op2.Valor:
                        op2 = determinaropciones(cat_elegida, False)
                    else:
                        op1 = determinaropciones(cat_elegida, False)
            print()
            print("Aciertos:", correctas, "de 6")
            if correctas >= 4:
                print("Felicidades!!! Ha ganado", apuesta, "creditos!!!")
                registrar_resultado(pos, apuesta, True)
            else:
                print("Oh, no... Usted ha perdido", apuesta, "creditos.")
                registrar_resultado(pos, -apuesta, False)
            reg = leer_jugador(pos)
            print("Saldo actual:", reg.Creditos)
            if reg.Creditos > 0:
                continuar = preguntar_continuar()
if reg.Creditos <= 0:
    print("No tiene mas creditos en su saldo")
input("Presione Enter para continuar...")
cierre()
