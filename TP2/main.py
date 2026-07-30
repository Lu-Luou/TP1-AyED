'''
Proyecto realizado por Joaquín del Castillo, Thiago Finoli, Guido Pacienzia y Lucas Ruberto
Comisión 1k05
'''

"""
Declarativa de variables globales
nombre : str
cont_juego1, mejor_racha_juego1, cont_juego2, cont_victorias_juego2, cont_juego4, cont_victorias_juego4 : int
"""

import random, os
import array


nombre = ""

cont_juego1 = 0
mejor_racha_juego1 = 0

cont_juego2 = 0
cont_victorias_juego2 = 0

cont_juego3 = 0
cont_victorias_juego3 = 0

cont_juego4 = 0
cont_victorias_juego4 = 0

"""
Declarativa de variables juego 1: Mayor o Menor
opcion_usuario : str
numero_mostrado, siguiente_numero, racha : int
jugando : bool
"""

def juego1():
    global nombre, cont_juego1, mejor_racha_juego1
    os.system("cls")
    print("\033[4m\033[96mMAYOR O MENOR\033[0m")

    nombre = input("Ingrese su nombre: ")

    numero_mostrado = random.randint(1, 1000)
    siguiente_numero = random.randint(1, 1000)

    while numero_mostrado == siguiente_numero:
        siguiente_numero = random.randint(1, 1000)

    jugando = True
    racha = 0

    while jugando:
        print("El número actual es:", numero_mostrado)
        opcion_usuario = input("Ingrese Mayor o Menor: ").lower()

        while opcion_usuario != "mayor" and opcion_usuario != "menor":
            print("Debe ingresar alguna opción válida")
            opcion_usuario = input("Ingrese Mayor o Menor: ").lower()

        if opcion_usuario == "mayor":
            if siguiente_numero > numero_mostrado:
                racha = racha + 1
                numero_mostrado = siguiente_numero
                siguiente_numero = random.randint(1,1000)
                while siguiente_numero==numero_mostrado:
                    siguiente_numero=random.randint(1,1000)
            else:
                jugando = False
        else:
            if siguiente_numero<numero_mostrado:
                racha = racha + 1
                numero_mostrado=siguiente_numero
                siguiente_numero=random.randint(1,1000)
                while siguiente_numero==numero_mostrado:
                    siguiente_numero=random.randint(1,1000)
            else:
                jugando = False

    print("Oh no, " + str(nombre) + ", perdiste. El número era " + str(siguiente_numero))
    print("Tuviste una racha de " + str(racha) + " aciertos")
    input("Presione Enter para continuar...")

    if mejor_racha_juego1 < racha:
        mejor_racha_juego1 = racha
    cont_juego1 = cont_juego1 + 1

"""
Declarativa de variables juego 2: Numero Secreto
numero_secreto, intentos, numero: int
ganador : bool
"""
def juego2():
    global nombre, cont_juego2, cont_victorias_juego2
    os.system("cls")
    print("\033[4m\033[91mNÚMERO SECRETO\033[0m")

    numero_secreto=random.randint(1,100)
    intentos=6
    ganador= False
    nombre =input("Ingrese su nombre: ")

    while(intentos > 0 and ganador==False):
        print("Usted tiene",intentos,"intentos")
        numero = input("Ingrese un número entre 1 y 100: ")
        while not numero.isdigit() or int(numero) < 1 or int(numero) > 100:
            numero=input("Por favor, ingrese un número válido entre 1 y 100: ")
        numero=int(numero)
        if numero==numero_secreto:
            ganador=True
        else:
            if numero > numero_secreto:
                print("El número secreto es menor")
                intentos=intentos-1
            else:
                print("El número secreto es mayor")
                intentos=intentos-1
        if ganador==True:
            print("¡¡Enhorabuena, ganaste ", nombre,"!! El número secreto era ", numero_secreto)
            cont_victorias_juego2=cont_victorias_juego2+1
        else:
            if intentos==0:
                print("Oh no, perdiste el juego")
                print("El número secreto era", numero_secreto)
    input("Presione Enter para continuar...")
    cont_juego2=cont_juego2+1

"""
Declarativa de variables juego 3: Blackjack
CANT_VALORES, MAX_CARTAS_MANO : int (constantes)
opcion_usuario, continua : str
puntos_jugador, puntos_banca, indice_valor, i : int
jugando : bool
mano_jugador, mano_banca, cant_repartidas_por_valor : array.array de int ('i')
cant_cartas_jugador, cant_cartas_banca : int
"""
CANT_VALORES = 13
MAX_CARTAS_MANO = 15

def repartir_carta(cant_repartidas_por_valor):
    indice_valor = random.randint(0, CANT_VALORES - 1)
    while cant_repartidas_por_valor[indice_valor] >= 4:
        indice_valor = random.randint(0, CANT_VALORES - 1)
    cant_repartidas_por_valor[indice_valor] = cant_repartidas_por_valor[indice_valor] + 1
    return indice_valor

def calcular_puntos(mano, cant_cartas):
    total = 0
    cant_ases = 0
    for i in range(cant_cartas):
        indice_valor = mano[i]
        if indice_valor == 12:
            total = total + 11
            cant_ases = cant_ases + 1
        elif indice_valor >= 9:
            total = total + 10
        else:
            total = total + (indice_valor + 2)

    while total > 21 and cant_ases > 0:
        total = total - 10
        cant_ases = cant_ases - 1

    return total

def nombre_carta(indice_valor):
    if indice_valor <= 8:
        return str(indice_valor + 2)
    elif indice_valor == 9:
        return "J"
    elif indice_valor == 10:
        return "Q"
    elif indice_valor == 11:
        return "K"
    else:
        return "A"

def mostrar_mano(titular, mano, cant_cartas):
    texto_cartas = ""
    for i in range(cant_cartas):
        texto_cartas = texto_cartas + nombre_carta(mano[i]) + " "
    print(titular + ": " + texto_cartas + "(Total: " + str(calcular_puntos(mano, cant_cartas)) + ")")

def juego3():
    global nombre, cont_juego3, cont_victorias_juego3
    os.system("cls")
    print("\033[4m\033[94mBLACKJACK SIMPLE\033[0m")

    nombre = input("Ingrese su nombre: ")
    continua = "S"

    while continua.upper() == "S":
        os.system("cls")
        print("\033[4m\033[94mBLACKJACK SIMPLE\033[0m")

        # cant_repartidas_por_valor[i] cuenta cuántas cartas del valor i
        # ya se repartieron en esta partida. Al ser un solo mazo de 52 cartas (4 palos),
        # cada valor puede salir como máximo 4 veces.
        cant_repartidas_por_valor = array.array('i', [0] * CANT_VALORES)

        mano_jugador = array.array('i', [0] * MAX_CARTAS_MANO)
        mano_banca = array.array('i', [0] * MAX_CARTAS_MANO)
        cant_cartas_jugador = 0
        cant_cartas_banca = 0

        for i in range(2):
            mano_jugador[i] = repartir_carta(cant_repartidas_por_valor)
        cant_cartas_jugador = 2

        for i in range(2):
            mano_banca[i] = repartir_carta(cant_repartidas_por_valor)
        cant_cartas_banca = 2

        puntos_jugador = calcular_puntos(mano_jugador, cant_cartas_jugador)
        puntos_banca = calcular_puntos(mano_banca, cant_cartas_banca)

        mostrar_mano("Banca", mano_banca, cant_cartas_banca)
        mostrar_mano(nombre, mano_jugador, cant_cartas_jugador)

        jugando = True

        while jugando:
            if puntos_jugador == 21:
                jugando = False
            else:
                opcion_usuario = input("¿Desea Pedir otra carta o Plantarse?: ").lower()
                while opcion_usuario != "pedir" and opcion_usuario != "plantarse":
                    opcion_usuario = input("Ingrese una opción válida, Pedir o Plantarse: ").lower()

                if opcion_usuario == "pedir":
                    mano_jugador[cant_cartas_jugador] = repartir_carta(cant_repartidas_por_valor)
                    cant_cartas_jugador = cant_cartas_jugador + 1
                    puntos_jugador = calcular_puntos(mano_jugador, cant_cartas_jugador)
                    mostrar_mano(nombre, mano_jugador, cant_cartas_jugador)

                    if puntos_jugador >= 21:
                        jugando = False
                else:
                    jugando = False

        if puntos_jugador > 21:
            print("\nTe pasaste de 21 con " + str(puntos_jugador) + " puntos. ¡Perdiste!")
        else:
            while puntos_banca < 17:
                mano_banca[cant_cartas_banca] = repartir_carta(cant_repartidas_por_valor)
                cant_cartas_banca = cant_cartas_banca + 1
                puntos_banca = calcular_puntos(mano_banca, cant_cartas_banca)

            mostrar_mano("Banca", mano_banca, cant_cartas_banca)

            if puntos_banca > 21:
                print("\nLa Banca se pasó de 21 con " + str(puntos_banca) + " puntos. ¡" + nombre + " gana!")
                cont_victorias_juego3 = cont_victorias_juego3 + 1
            elif puntos_jugador > puntos_banca:
                print("\n" + nombre + " gana con " + str(puntos_jugador) + " contra " + str(puntos_banca) + " de la Banca")
                cont_victorias_juego3 = cont_victorias_juego3 + 1
            elif puntos_jugador < puntos_banca:
                print("\nLa Banca gana con " + str(puntos_banca) + " contra " + str(puntos_jugador) + " de " + nombre)
            else:
                print("\nEmpate entre " + nombre + " y la Banca con " + str(puntos_jugador) + " puntos")

        cont_juego3 = cont_juego3 + 1
        input("Presione Enter para continuar...")

        continua = input("¿Desea jugar otra partida? Ingrese S para si o N para no: ")
        while continua.upper() != "S" and continua.upper() != "N":
            continua = input("Ingrese una opción válida: ")


"""
Declarativa de variables juego 4: Par o Impar
eleccion, continua : str
num1, num2, secreto: int
"""
def juego4():
    global nombre, cont_juego4, cont_victorias_juego4
    os.system("cls")
    print("\033[4m\033[95mPAR O IMPAR\033[0m")

    saldo=10000
    continua="S"
    nombre =input("Ingrese su nombre: ")

    while continua.upper()=="S":
        os.system("cls")
        print("Usted tiene ",saldo," créditos disponibles para jugar")
        apuesta=input("¿Cuántos créditos desea apostar en la siguiente jugada?: ")
        while(not apuesta.isdigit() or int(apuesta) > saldo or int(apuesta) <= 0):
            apuesta=input("Ingrese una apuesta menor o igual a su saldo, mayor a 0: ")
        apuesta=int(apuesta)
        num1=random.randint(1,6)
        num2=random.randint(1,6)
        secreto=num1+num2
        eleccion=input("¿La suma es Par o Impar?: ")
        while(eleccion.lower()!= "par" and eleccion.lower()!= "impar"):
            eleccion=input("Ingrese una ópcion válida entre Par o Impar: ")
        if (eleccion.lower()=="par" and secreto % 2 == 0):
            input("\nAdivinaste! " + str(secreto) + " es Par. Tu apuesta de " + str(apuesta) + " créditos se ha duplicado! ")
            saldo=saldo+apuesta
            cont_victorias_juego4=cont_victorias_juego4+1
            cont_juego4=cont_juego4+1
        else:
            if (eleccion.lower()=="impar" and secreto % 2 == 1):
                input("\nAdivinaste! " + str(secreto) + " es Impar. Tu apuesta de " + str(apuesta) + " créditos se ha duplicado! ")
                saldo=saldo+apuesta
                cont_victorias_juego4=cont_victorias_juego4+1
                cont_juego4=cont_juego4+1
            else:
                input("\nOh no!! Fallaste... La suma de los dados es " + str(secreto) + " que es un número " + ("Par." if secreto % 2 == 0 else "Impar.") + " Tu apuesta de " + str(apuesta) + " créditos se perdió... ")
                saldo=saldo-apuesta
                cont_juego4=cont_juego4+1
                print("Tu saldo actual es de ",saldo," créditos")
        os.system("cls")
        print("Tu saldo actual es de ",saldo," créditos")
        if saldo == 0:
            input("Que mal... te quedaste sin créditos!! Presione Enter para salir del juego...")
            continua = "N"
        else:
            continua=input("¿Desea volver a jugar? Ingrese S para si o N para no: ")
            while(continua.upper()!="S" and continua.upper()!="N"):
                continua=input("Ingrese una opción valida: ")

def reporte():
    os.system("cls")
    if nombre == "":
        print("No se han registrado juegos aún, por favor juegue alguna partida para generar un reporte.")
        input("Presione Enter para continuar...")
    else:
        print("........\033[93m\033[4mREPORTE DE JUEGOS\033[0m........ ")
        print("Nombre del jugador: ", nombre, "\n")
        print("\033[96mMayor o Menor:\033[0m \n   mejor racha: ", mejor_racha_juego1, "\n   cantidad de partidas jugadas: ", cont_juego1, "\n")
        print("\033[1m\033[91mNúmero Secreto:\033[0m \n   cantidad de partidas jugadas: ", cont_juego2, "\n   cantidad de victorias: ", cont_victorias_juego2, "\n")
        print("\033[94mBlackJack Simple:\033[0m \n   cantidad de partidas jugadas: ", cont_juego3, "\n   cantidad de victorias: ", cont_victorias_juego3, "\n")
        print("\033[95mPar o Impar:\033[0m \n   cantidad de partidas jugadas: ", cont_juego4, "\n   cantidad de victorias: ", cont_victorias_juego4, "\n")
        input("Presione Enter para continuar...")

def salir():
    os.system("cls")
    input("Gracias por jugar, no apueste, juega por diversión!!")

def menu():
    os.system("cls")
    print("........\033[4m\033[92mMENU PRINCIPAL\033[0m ")
    print("A- \033[96m↑ Mayor o Menor ↓\033[0m ")
    print("B- \033[1m\033[91mNúmero Secreto [?]\033[0m ")
    print("C- \033[94m♦ BlackJack Simple ♦\033[0m ")
    print("D- \033[95m[1] Dados - Par o impar [6]\033[0m ")
    print("E- \033[93mReporte\033[0m ")
    print("S- \033[97mFin DEL PROGRAMA\033[0m ")


# Función principal que controla el flujo del programa

# Banner inicial
print("\033[93m+------------------------------------------------------------+")
print("|                                                            |")
print("|  JUEGOS DE APUESTA PROHIBIDOS PARA MENORES DE EDAD         |")
print("|                                                            |")
print("|     EL JUEGO PUEDE SER PERJUDICIAL PARA LA SALUD           |")
print("|                                                            |")
print("+------------------------------------------------------------+\033[0m")
input()

# Loop principal del programa
opc = " "
while opc != "s":
    menu()
    opc = str(input("Ingrese su opción: ")).lower()

    while (opc < "a" or opc > "e") and opc != "s":
        menu()
        opc = str(input("Ingreso Invalido - reintente: ")).lower()

    match opc:
        case "a": juego1()
        case "b": juego2()
        case "c": juego3()
        case "d": juego4()
        case "e": reporte()
        case "s": salir()
