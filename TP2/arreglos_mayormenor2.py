import os
import random
import array
max_jugadores=10
contadores_juego1=[0]*10
jugadores_MM=[""]*10
cantjugadores1=0
mejores_racha_juego1=[0]*10
def validarnombre(cadena):
    if len(cadena) == 0:
        return False
    for i in range(len(cadena)):
        if cadena[i].isdigit():
            return False
    return True
print("\033[4m\033[96mMAYOR O MENOR\033[0m")
nombre =input("Ingrese su nombre: ")
while not validarnombre(nombre):
    print("Error: El nombre no puede contener números ni estar vacío.")
    nombre = input("Por favor, reingrese un nombre válido: ")
encontrado=False
i=0
pos=-1
while i < cantjugadores1 and not encontrado:
    if nombre == jugadores_MM[i]:
     encontrado = True
     pos=i
    else:
     i = i + 1
juega=True
if not encontrado:
 if cantjugadores1 < max_jugadores:
     pos=cantjugadores1
     jugadores_MM[cantjugadores1] = nombre
     cantjugadores1 = cantjugadores1 + 1
 else:
     print("Error.Se permiten como máximo 10 jugadores")
     juega=False
if juega:
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

    print("Oh no, " + str(jugadores_MM[pos]) + ", perdiste. El número era " + str(siguiente_numero))
    print("Tuviste una racha de " + str(racha) + " aciertos")
    input("Presione Enter para continuar...")

    if mejores_racha_juego1[pos] < racha:
        mejores_racha_juego1[pos] = racha
    contadores_juego1[pos] = contadores_juego1[pos]+1
