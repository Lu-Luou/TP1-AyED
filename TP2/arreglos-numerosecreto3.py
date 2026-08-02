import random,os
max_jugadores=10
cont_veces_jugadas_numero_secreto=[0]*10
jugadores_numero_secreto=[""]*10
cant_jugadores_numero_secreto=0
cont_victorias_numero_secreto=[0]*10
cont_derrotas_numero_secreto=[0]*10
def validarnombre(cadena):
    if len(cadena) == 0:
        return False
    for i in range(len(cadena)):
        if cadena[i].isdigit():
            return False
    return True
while True: ## SACAR ESTE WHILR PARA IMPLEMENTAR EL JUEGO EN EL MAIN
    print("\033[4m\033[91mNÚMERO SECRETO\033[0m")
    numero_secreto=random.randint(1,100)
    intentos=6
    ganador= False
    nombre =input("Ingrese su nombre: ")
    while not validarnombre(nombre):
        print("Error: El nombre no puede contener números ni estar vacío.")
        nombre = input("Por favor, reingrese un nombre válido: ")
    encontrado=False
    j=0
    pos2=-1
    while j < cant_jugadores_numero_secreto and not encontrado:
        if nombre == jugadores_numero_secreto[j]:
            encontrado = True
            pos2=j
        else:
            j = j + 1
    juega=True
    if not encontrado:
        if cant_jugadores_numero_secreto < max_jugadores:
            pos2=cant_jugadores_numero_secreto
            jugadores_numero_secreto[cant_jugadores_numero_secreto] = nombre
            cant_jugadores_numero_secreto = cant_jugadores_numero_secreto + 1
        else:
            print("Error.Se permiten como máximo 10 jugadores")
            juega=False
    if juega:

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
                print("¡¡Enhorabuena, ganaste en",intentos,"intentos", nombre,"!! El número secreto era ", numero_secreto)
                cont_victorias_numero_secreto[pos2]=cont_victorias_numero_secreto[pos2]+1
            else:
                if intentos==0:
                    print("Oh no, perdiste el juego")
                    print("El número secreto era", numero_secreto)
                    cont_derrotas_numero_secreto[pos2]=cont_derrotas_numero_secreto[pos2]+1
        input("Presione Enter para continuar...")
        cont_veces_jugadas_numero_secreto[pos2]=cont_veces_jugadas_numero_secreto[pos2]+1