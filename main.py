'''
Proyecto realizado por Joaquin del Castillo, Thiago Finoli, Guido Paciencia y Lucas Ruberto
Comisión 1k05
'''

# Declaración de funciones, variables y librerias

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


def juego1():
    global nombre, cont_juego1, mejor_racha_juego1
    os.system("cls")
    print("MAYOR O MENOR")

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

    print("Oh no, " + str(nombre) + ", perdiste. El numero era " + str(siguiente_numero))
    print("Tuviste una racha de " + str(racha) + " aciertos")
    input("Presione Enter para continuar...")

    if mejor_racha_juego1 < racha:
        mejor_racha_juego1 = racha
    cont_juego1 = cont_juego1 + 1

def juego2():
    global nombre, cont_juego2, cont_victorias_juego2
    os.system("cls")
    print("NUMERO SECRETO")

    numero_secreto=random.randint(1,100)
    intentos=6
    ganador=0
    nombre =input("Ingrese su nombre: ")

    while(intentos > 0 and ganador==0):
        print("Usted tiene",intentos,"intentos")
        numero = int(input("Ingrese un número entre 1 y 100: "))
        while int(numero) < 1 or int(numero) > 100:
            numero=int(input("Por favor, ingrese un número válido entre 1 y 100: "))
        if numero==numero_secreto:
            ganador=1
        else:
            if numero > numero_secreto:
                print("El número secreto es menor")
                intentos=intentos-1
            else:
                print("El número secreto es mayor")
                intentos=intentos-1
        if ganador==1:
            print("¡¡Enhorabuena,ganaste ", nombre,"!! El número secreto era ", numero_secreto)
            cont_victorias_juego2=cont_victorias_juego2+1
        else:
            if intentos==0:
                print("Oh no,perdiste el juego")
                print("El número secreto era", numero_secreto)
    input("Presione Enter para continuar...")        
    cont_juego2=cont_juego2+1

def juego3():
    os.system("cls")
    print("BLACKJACK SIMPLE")
    cartel()

def juego4():
    global nombre, cont_juego4, cont_victorias_juego4
    os.system("cls")
    print("PAR O IMPAR")

    saldo=10000
    continua="S"

    while continua=="S":
        print("Usted tiene ",saldo," créditos disponibles para jugar")
        apuesta=int(input("¿Cuantos créditos desea apostar en la siguiente jugada?"))
        if(apuesta>saldo or 0>=apuesta):
            while(apuesta>=saldo or 0>=apuesta):
                apuesta=int(input("Ingrese una apuesta menor o igual a su saldo,mayor a 0"))
        num1=random.randint(1,6)
        num2=random.randint(1,6)
        secreto=num1+num2
        eleccion=input("¿La suma es Par o Impar?")
        while(eleccion!= "Par" and eleccion!= "Impar"):
            eleccion=input("Ingrese una ópcion valida entre Par o Impar")
        if (eleccion=="Par" and secreto % 2 == 0):
            print("Adivinaste!!!Tu apuesta de",apuesta,"créditos se ha duplicado!!! ")
            saldo=saldo+apuesta
            cont_victorias_juego4=cont_victorias_juego4+1
            cont_juego4=cont_juego4+1
            # print("Tu saldo actual es de",saldo,"créditos y tu racha es de",racha,)
        else:
            if (eleccion=="Impar" and secreto % 2 == 1):
                print("Adivinaste!!!Tu apuesta de",apuesta,"creditos se ha duplicado!!! ")
                saldo=saldo+apuesta
                cont_victorias_juego4=cont_victorias_juego4+1
                cont_juego4=cont_juego4+1
                # print("Tu saldo actual es de",saldo,"créditos y tu racha es de ",racha,)
            else:
                print("No,fallaste")
                saldo=saldo-apuesta
                cont_juego4=cont_juego4+1
                print("Tu saldo actual es de",saldo,"créditos")
        continua=input("¿Desea volver a jugar?Ingrese S para si o N para no")
        while(continua!="S" and continua!="N"):
            continua=input("Ingrese una opción valida")

def cartel():
    print("... bajo construcción ...")
    input("Presione Enter para continuar...")

def reporte():
    os.system("cls")
    if nombre == "":
        print("No se han registrado juegos aún, por favor juegue alguna partida para generar un reporte.")
        input("Presione Enter para continuar...")
    else:
        print("........REPORTE DE JUEGOS........ ")
        print("Nombre del jugador: ", nombre, "\n")
        print("Mayor o Menor: \n   mejor racha: ", mejor_racha_juego1, "\n   cantidad de partidas jugadas: ", cont_juego1, "\n")
        print("Numero Secreto: \n   cantidad de partidas jugadas: ", cont_juego2, "\n   cantidad de victorias: ", cont_victorias_juego2, "\n")
        print("BlackJack Simple: \n   fuera de servicio \n")
        print("Par o Impar: \n   cantidad de partidas jugadas: ", cont_juego4, "\n   cantidad de victorias: ", cont_victorias_juego4, "\n")
        input("Presione Enter para continuar...")

def salir():
    os.system("cls")
    input("Gracias por jugar, no apueste, juega por diversión!!")

def menu():
    print("........MENU PRINCIPAL. ")
    print("A- Mayor o Menor ")
    print("B- Numero Secreto. ")
    print("C- BlackJack Simple ")
    print("D- Dados.- Par o impar ")
    print("E- Reporte ")
    print("S- Fin DEL PROGRAMA")


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
    opc = str(input("Ingrese su opcion: ")).lower()

    while (opc < "a" or opc > "e") and opc != "s":
        os.system("cls")
        menu()
        opc = str(input("Ingreso Invalido - reintente: ")).lower()

    match opc:
        case "a": juego1()
        case "b": juego2()
        case "c": cartel()
        case "d": juego4()
        case "e": reporte()
        case "s": salir()
