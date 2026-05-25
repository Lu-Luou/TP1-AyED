'''
Proyecto realizado por Joaquin del Castillo, Thiago Finoli, Guido Paciencia y Lucas Ruberto
Comisión 1k05
'''

# Declaración de funciones, variables y librerias

import random, os

def juego1():
    os.system("cls")
    global nombre, cont_juego1, mejor_racha_juego1
    nombre = input("Ingrese su nombre: ")

    numero_mostrado = random.randint(1, 1000)
    siguiente_numero = random.randint(1, 1000)

    while numero_mostrado == siguiente_numero:
        siguiente_numero = random.randint(1, 1000)

    jugando = True
    racha = 0

    while jugando:
        print("El numero actual es:", numero_mostrado)
        opcion_usuario = input("Ingrese Mayor o Menor: ").lower()

        while opcion_usuario != "mayor" and opcion_usuario != "menor":
            print("Debe ingresar alguna opción valida")
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

    print("Oh no," + str(nombre) + ", perdiste. El numero era " + str(siguiente_numero))
    print("Tuviste una racha de " + str(racha) + " aciertos")

    if mejor_racha_juego1 < racha:
        mejor_racha_juego1 = racha
    cont_juego1 = cont_juego1 + 1

def juego2():
    global nombre, cont_juego2, cont_victorias_juego2
    numero_secreto=random.randint(1,100)
    intentos=6
    ganador=0

    nombre =input("Indique nombre del jugador")

    while(intentos>0 and ganador==0):
        print("Usted tiene",intentos,"intentos")
        valido=False
        while not valido:
            numero=input("Ingrese un número entre 1 y 100")
            try:
                numero = int(numero)
                if(numero >=1 and numero <=100):
                    valido = True

                else:
                    print("Ingrese un número válido entre 1 y 100")

            except:
                print("Debe ingresar un número")
        if numero==numero_secreto:
            ganador=1

        else:

            if numero>numero_secreto:
                print("El número secreto es menor")
                intentos=intentos-1

            else:
                print("El número secreto es mayor")
                intentos=intentos-1
        if ganador==1:
            print(nombre,"¡¡Enhorabuena,ganaste!!")

        else:
            if intentos==0:
                print("Oh no,perdiste el juego")
                print("El número secreto era", numero_secreto)

def juego3():
    return 0

def juego4():
    return 0

def cartel():
    print("... bajo construcción ...")

def reporte():
    print("........REPORTE DE JUEGOS. ")
    print("Mayor o Menor, mejor racha: ", mejor_racha_juego1)

def salir():
    print("Gracias por jugar, no apueste, juega por diversión")
    input()

def menu():
    print("........MENU PRINCIPAL. ")
    print("A- Mayor o Menor ")
    print("B- Numero Secreto. ")
    print("C- BlackJack Simple ")
    print("D- Dados.- Par o impar ")
    print("E- Reporte ")
    print("S- Fin DEL PROGRAMA")


nombre = ""

cont_juego1 = 0
mejor_racha_juego1 = 0

cont_juego2 = 0
cont_victorias_juego2 = 0

# cont_juego3 = 0 -> fuera de servicio
# cont_victorias_juego2 = 0

cont_juego4 = 0
cont_victorias_juego4 = 0

"""Función principal que controla el flujo del programa"""

# Banner inicial
print("+------------------------------------------------------------+")
print("|                                                            |")
print("|  JUEGOS DE APUESTA PROHIBIDOS PARA MENORES DE EDAD         |")
print("|                                                            |")
print("|     EL JUEGO PUEDE SER PERJUDICIAL PARA LA SALUD           |")
print("|                                                            |")
print("+------------------------------------------------------------+")
input()
os.system("cls")

# Loop principal del programa
opc = " "
while opc != "s":
    menu()
    opc = str(input("Ingrese su opcion: ")).lower()

    while (opc < "a" or opc > "e") and opc != "s":
        os.system("cls")
        opc = str(input("Ingreso Invalido - reintente ")).lower()

    match opc:
        case "a": 
            juego1()
        case "b": juego2()
    
        case "c": cartel()
        case "d": juego4()
        case "e": reporte()
        case "s": salir()