'''
Proyecto realizado por Joaquín del Castillo, Thiago Finoli, Guido Paciencia y Lucas Ruberto
Comisión 1k05
'''

"""
Declarativa de variables globales
nombre : str
cont_juego1, mejor_racha_juego1, cont_juego2, cont_victorias_juego2, cont_juego4, cont_victorias_juego4 : int
"""

import random, os


nombre = ""

cont_juego1 = 0
mejor_racha_juego1 = 0

cont_juego2 = 0
cont_victorias_juego2 = 0

# cont_juego3 = 0 -> fuera de servicio
# cont_victorias_juego2 = 0

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

def juego3():
    os.system("cls")
    print("\033[4m\033[94mBLACKJACK SIMPLE\033[0m")
    cartel()

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

    while continua=="S":
        print("Usted tiene ",saldo," créditos disponibles para jugar")
        apuesta=input("¿Cuántos créditos desea apostar en la siguiente jugada?: ")
        if(not apuesta.isdigit() or int(apuesta) > saldo or int(apuesta) <= 0):
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
            print("Adivinaste! Tu apuesta de ",apuesta," créditos se ha duplicado! ")
            saldo=saldo+apuesta
            cont_victorias_juego4=cont_victorias_juego4+1
            cont_juego4=cont_juego4+1
            # print("Tu saldo actual es de",saldo,"créditos y tu racha es de",racha,)
        else:
            if (eleccion.lower()=="impar" and secreto % 2 == 1):
                print("Adivinaste! Tu apuesta de ",apuesta," créditos se ha duplicado! ")
                saldo=saldo+apuesta
                cont_victorias_juego4=cont_victorias_juego4+1
                cont_juego4=cont_juego4+1
                # print("Tu saldo actual es de",saldo,"créditos y tu racha es de ",racha,)
            else:
                print("No,fallaste")
                saldo=saldo-apuesta
                cont_juego4=cont_juego4+1
                print("Tu saldo actual es de ",saldo," créditos")
        continua=input("¿Desea volver a jugar? Ingrese S para si o N para no: ")
        while(continua!="S" and continua!="N"):
            continua=input("Ingrese una opción valida: ")

def cartel():
    print("... bajo construcción ...")
    input("Presione Enter para continuar...")

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
        print("\033[94mBlackJack Simple:\033[0m \n   fuera de servicio \n")
        print("\033[95mPar o Impar:\033[0m \n   cantidad de partidas jugadas: ", cont_juego4, "\n   cantidad de victorias: ", cont_victorias_juego4, "\n")
        input("Presione Enter para continuar...")

def salir():
    os.system("cls")
    input("Gracias por jugar, no apueste, juega por diversión!!")

def menu():
    print("........\033[4m\033[92mMENU PRINCIPAL\033[0m ")
    print("A- \033[96m↑ Mayor o Menor ↓\033[0m ")
    print("B- \033[1m\033[91mNúmero Secreto [?]\033[0m ")
    print("C- \033[94m♦ BlackJack Simple ♦\033[0m ")
    print("D- \033[95m[1] Dados - Par o impar [6]\033[0m ")
    print("E- \033[93mReporte\033[0m ")
    print("S- \033[97mFin DEL PROGRAMA\033[0m ")


# Función principal que controla el flujo del programa

# Banner inicial
print("+------------------------------------------------------------+")
print("|                                                            |")
print("|  JUEGOS DE APUESTA PROHIBIDOS PARA MENORES DE EDAD         |")
print("|                                                            |")
print("|     EL JUEGO PUEDE SER PERJUDICIAL PARA LA SALUD           |")
print("|                                                            |")
print("+------------------------------------------------------------+")
input()

# Loop principal del programa
opc = " "
while opc != "s":
    os.system("cls")
    menu()
    opc = str(input("Ingrese su opción: ")).lower()

    while (opc < "a" or opc > "e") and opc != "s":
        os.system("cls")
        menu()
        opc = str(input("Ingreso Invalido - reintente: ")).lower()

    match opc:
        case "a": juego1()
        case "b": juego2()
        case "c": juego3()
        case "d": juego4()
        case "e": reporte()
        case "s": salir()
