import random
import os
global nombre
os.system("cls")

## esta función se declara una sola vez en el main
def validarnombre(cadena):
    if len(cadena) == 0:
        return False
    for i in range(len(cadena)):
        if cadena[i].isdigit():
            return False
    return True
## Estas variables se deben declarar una sola vez en el main ni bien arranca el programa
max_jugadores=10
jugadores_par_impar = [""] * max_jugadores
cont_jugadores_par_impar = 0
saldo_jugadores=[1000]*10
cont_victorias_par_impar = [0] * 10
cont_veces_jugadas_par_impar = [0] * 10

while True:
    continua="S"
    print("\033[4m\033[95mPAR O IMPAR\033[0m")
    nombre =input("Ingrese su nombre: ")
    while not validarnombre(nombre):
        print("Error: El nombre no puede contener números ni estar vacío.")
        nombre = input("Por favor, reingrese un nombre válido: ")
    encontrado=False
    pos=-1
    for i in range(cont_jugadores_par_impar):
        if nombre == jugadores_par_impar[i]:
            encontrado = True
            pos=i
    juega=True
    if not encontrado:
        if cont_jugadores_par_impar < max_jugadores:
            pos=cont_jugadores_par_impar
            jugadores_par_impar[cont_jugadores_par_impar] = nombre
            cont_jugadores_par_impar = cont_jugadores_par_impar + 1
        else:
            print("Error.Se permiten como máximo 10 jugadores")
            juega=False

    if juega:
        while continua.upper()=="S":
            os.system("cls")
            print("Usted tiene ",saldo_jugadores[pos]," créditos disponibles para jugar")
            apuesta=input("¿Cuántos créditos desea apostar en la siguiente jugada?: ")
            while(not apuesta.isdigit() or int(apuesta) > saldo_jugadores[pos] or int(apuesta) <= 0):
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
                saldo_jugadores[pos]=saldo_jugadores[pos]+apuesta
                cont_victorias_par_impar[pos]=cont_victorias_par_impar[pos]+1
                cont_veces_jugadas_par_impar[pos]=cont_veces_jugadas_par_impar[pos]+1
            else:
                if (eleccion.lower()=="impar" and secreto % 2 == 1):
                    input("\nAdivinaste! " + str(secreto) + " es Impar. Tu apuesta de " + str(apuesta) + " créditos se ha duplicado! ")
                    saldo_jugadores[pos]=saldo_jugadores[pos]+apuesta
                    cont_victorias_par_impar[pos]=cont_victorias_par_impar[pos]+1
                    cont_veces_jugadas_par_impar[pos]=cont_veces_jugadas_par_impar[pos]+1
                else:
                    input("\nOh no!! Fallaste... La suma de los dados es " + str(secreto) + " que es un número " + ("Par." if secreto % 2 == 0 else "Impar.") + " Tu apuesta de " + str(apuesta) + " créditos se perdió... ")
                    saldo_jugadores[pos]=saldo_jugadores[pos]-apuesta
                    cont_veces_jugadas_par_impar[pos]=cont_veces_jugadas_par_impar[pos]+1
                    print("Tu saldo actual es de ",saldo_jugadores[pos]," créditos")
            os.system("cls")
            print("Tu saldo actual es de ",saldo_jugadores[pos]," créditos")
            if saldo_jugadores[pos] == 0:
                input("Que mal... te quedaste sin créditos!! Presione Enter para salir del juego...")
                continua = "N"
            else:
                continua=input("¿Desea volver a jugar? Ingrese S para si o N para no: ")
                while(continua.upper()!="S" and continua.upper()!="N"):
                    continua=input("Ingrese una opción valida: ")