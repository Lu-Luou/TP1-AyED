'''
Proyecto realizado por Joaquín del Castillo, Thiago Finoli, Guido Pacienzia y Lucas Ruberto
Comisión 1k05
'''

"""
Declarativa de variables globales
MAX_JUGADORES : int (constante, máximo de jugadores por juego)
jugadores_mayor_menor, jugadores_numero_secreto, jugadores_blackjack, jugadores_par_impar : array de str, tamaño MAX_JUGADORES
cant_jugadores_mayor_menor, cant_jugadores_numero_secreto, cant_jugadores_blackjack, cant_jugadores_par_impar : int
cont_veces_jugadas_mayor_menor, mejor_racha_mayor_menor : array de int, tamaño MAX_JUGADORES
cont_veces_jugadas_numero_secreto, cont_victorias_numero_secreto, cont_derrotas_numero_secreto : array de int, tamaño MAX_JUGADORES
cont_veces_jugadas_blackjack, cont_victorias_blackjack : array de int, tamaño MAX_JUGADORES
cont_veces_jugadas_par_impar, cont_victorias_par_impar, saldo_par_impar : array de int, tamaño MAX_JUGADORES
"""

import random, os


MAX_JUGADORES = 10

jugadores_mayor_menor = [""] * MAX_JUGADORES
cant_jugadores_mayor_menor = 0
cont_veces_jugadas_mayor_menor =[0] * MAX_JUGADORES
mejor_racha_mayor_menor = [0] * MAX_JUGADORES

jugadores_numero_secreto = [""] * MAX_JUGADORES
cant_jugadores_numero_secreto = 0
cont_veces_jugadas_numero_secreto = [0] * MAX_JUGADORES
cont_victorias_numero_secreto = [0] * MAX_JUGADORES
cont_derrotas_numero_secreto = [0] * MAX_JUGADORES

jugadores_blackjack = [""] * MAX_JUGADORES
cant_jugadores_blackjack = 0
cont_veces_jugadas_blackjack = [0] * MAX_JUGADORES
cont_victorias_blackjack =[0] * MAX_JUGADORES

jugadores_par_impar = [""] * MAX_JUGADORES
cant_jugadores_par_impar = 0
cont_veces_jugadas_par_impar = [0] * MAX_JUGADORES
cont_victorias_par_impar = [0] * MAX_JUGADORES
saldo_par_impar = [1000] * MAX_JUGADORES

"""
Declarativa de funciones y variables compartidas entre juegos
cadena, nombre : str
i, pos, cant_jugadores : int
"""
def validarnombre(cadena):
    if len(cadena) == 0:
        return False
    for i in range(len(cadena)):
        if cadena[i].isdigit():
            return False
    return True

def buscar_jugador(nombre, jugadores, cant_jugadores):
    pos = -1
    i = 0
    while i < cant_jugadores and pos == -1:
        if jugadores[i] == nombre:
            pos = i
        else:
            i = i + 1
    return pos

"""
Declarativa de variables juego 1: Mayor o Menor
nombre, opcion_usuario : str
pos, numero_mostrado, siguiente_numero, racha : int
jugando, avanza : bool
"""
def juego1():
    global cant_jugadores_mayor_menor
    os.system("cls")
    print("\033[4m\033[96mMAYOR O MENOR\033[0m")

    nombre = input("Ingrese su nombre: ")
    while not validarnombre(nombre):
        print("Error: El nombre no puede contener números ni estar vacío.")
        nombre = input("Por favor, reingrese un nombre válido: ")

    pos = buscar_jugador(nombre, jugadores_mayor_menor, cant_jugadores_mayor_menor)

    if pos == -1:
        if cant_jugadores_mayor_menor < MAX_JUGADORES:
            pos = cant_jugadores_mayor_menor
            jugadores_mayor_menor[pos] = nombre
            cant_jugadores_mayor_menor = cant_jugadores_mayor_menor + 1
        else:
            print("Error. Se permiten como máximo " + str(MAX_JUGADORES) + " jugadores en este juego.")
            input("Presione Enter para continuar...")
            return

    numero_mostrado = random.randint(1, 1000)
    siguiente_numero = random.randint(1, 1000)

    jugando = True
    racha = 0

    while jugando:
        print("El número actual es:", numero_mostrado)
        opcion_usuario = input("Ingrese Mayor o Menor: ").lower()

        while opcion_usuario != "mayor" and opcion_usuario != "menor":
            print("Debe ingresar alguna opción válida")
            opcion_usuario = input("Ingrese Mayor o Menor: ").lower()

        # Si vuelve a salir el mismo número el juego sigue, pero la racha no suma.
        if siguiente_numero == numero_mostrado:
            print("Salió de nuevo el " + str(siguiente_numero) + ", la racha se mantiene en " + str(racha))
            avanza = True
        else:
            if opcion_usuario == "mayor":
                avanza = siguiente_numero > numero_mostrado
            else:
                avanza = siguiente_numero < numero_mostrado

            if avanza:
                racha = racha + 1

        if avanza:
            numero_mostrado = siguiente_numero
            siguiente_numero = random.randint(1, 1000)
        else:
            jugando = False

    print("Oh no, " + nombre + ", perdiste. El número era " + str(siguiente_numero))
    print("Tuviste una racha de " + str(racha) + " aciertos")
    input("Presione Enter para continuar...")

    if mejor_racha_mayor_menor[pos] < racha:
        mejor_racha_mayor_menor[pos] = racha
    cont_veces_jugadas_mayor_menor[pos] = cont_veces_jugadas_mayor_menor[pos] + 1

"""
Declarativa de variables juego 2: Numero Secreto
MAX_INTENTOS : int (constante, intentos disponibles por partida)
nombre, numero : str
pos, numero_secreto, intentos : int
ganador : bool
"""
MAX_INTENTOS = 6

def juego2():
    global cant_jugadores_numero_secreto
    os.system("cls")
    print("\033[4m\033[91mNÚMERO SECRETO\033[0m")

    nombre = input("Ingrese su nombre: ")
    while not validarnombre(nombre):
        print("Error: El nombre no puede contener números ni estar vacío.")
        nombre = input("Por favor, reingrese un nombre válido: ")

    pos = buscar_jugador(nombre, jugadores_numero_secreto, cant_jugadores_numero_secreto)

    if pos == -1:
        if cant_jugadores_numero_secreto < MAX_JUGADORES:
            pos = cant_jugadores_numero_secreto
            jugadores_numero_secreto[pos] = nombre
            cant_jugadores_numero_secreto = cant_jugadores_numero_secreto + 1
        else:
            print("Error. Se permiten como máximo " + str(MAX_JUGADORES) + " jugadores en este juego.")
            input("Presione Enter para continuar...")
            return

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
            print("¡¡Enhorabuena " + nombre + "! Ganaste en " + str(MAX_INTENTOS - intentos) + " intentos. El número secreto era", numero_secreto)
            cont_victorias_numero_secreto[pos] = cont_victorias_numero_secreto[pos] + 1
        else:
            if intentos==0:
                print("Oh no, perdiste el juego")
                print("El número secreto era", numero_secreto)
                cont_derrotas_numero_secreto[pos] = cont_derrotas_numero_secreto[pos] + 1
    input("Presione Enter para continuar...")
    cont_veces_jugadas_numero_secreto[pos] = cont_veces_jugadas_numero_secreto[pos] + 1

"""
Declarativa de variables juego 3: Blackjack
CANT_VALORES, MAX_CARTAS_MANO : int (constantes)
nombre, opcion_usuario, continua : str
pos, puntos_jugador, puntos_banca, indice_valor, i : int
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
    global cant_jugadores_blackjack
    os.system("cls")
    print("\033[4m\033[94mBLACKJACK SIMPLE\033[0m")

    nombre = input("Ingrese su nombre: ")
    while not validarnombre(nombre):
        print("Error: El nombre no puede contener números ni estar vacío.")
        nombre = input("Por favor, reingrese un nombre válido: ")

    pos = buscar_jugador(nombre, jugadores_blackjack, cant_jugadores_blackjack)

    if pos == -1:
        if cant_jugadores_blackjack < MAX_JUGADORES:
            pos = cant_jugadores_blackjack
            jugadores_blackjack[pos] = nombre
            cant_jugadores_blackjack = cant_jugadores_blackjack + 1
        else:
            print("Error. Se permiten como máximo " + str(MAX_JUGADORES) + " jugadores en este juego.")
            input("Presione Enter para continuar...")
            return

    continua = "S"

    while continua.upper() == "S":
        os.system("cls")
        print("\033[4m\033[94mBLACKJACK SIMPLE\033[0m")

        # cant_repartidas_por_valor[i] cuenta cuántas cartas del valor i
        # ya se repartieron en esta partida. Al ser un solo mazo de 52 cartas (4 palos),
        # cada valor puede salir como máximo 4 veces.
        cant_repartidas_por_valor = [0] * CANT_VALORES

        mano_jugador = [0] * MAX_CARTAS_MANO
        mano_banca = [0] * MAX_CARTAS_MANO
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
                cont_victorias_blackjack[pos] = cont_victorias_blackjack[pos] + 1
            elif puntos_jugador > puntos_banca:
                print("\n" + nombre + " gana con " + str(puntos_jugador) + " contra " + str(puntos_banca) + " de la Banca")
                cont_victorias_blackjack[pos] = cont_victorias_blackjack[pos] + 1
            elif puntos_jugador < puntos_banca:
                print("\nLa Banca gana con " + str(puntos_banca) + " contra " + str(puntos_jugador) + " de " + nombre)
            else:
                print("\nEmpate entre " + nombre + " y la Banca con " + str(puntos_jugador) + " puntos")

        cont_veces_jugadas_blackjack[pos] = cont_veces_jugadas_blackjack[pos] + 1
        input("Presione Enter para continuar...")

        continua = input("¿Desea jugar otra partida? Ingrese S para si o N para no: ")
        while continua.upper() != "S" and continua.upper() != "N":
            continua = input("Ingrese una opción válida: ")

"""
Declarativa de variables juego 4: Par o Impar
nombre, eleccion, continua, apuesta_str, paridad : str
pos, num1, num2, secreto, apuesta : int
"""
def juego4():
    global cant_jugadores_par_impar
    os.system("cls")
    print("\033[4m\033[95mPAR O IMPAR\033[0m")

    nombre = input("Ingrese su nombre: ")
    while not validarnombre(nombre):
        print("Error: El nombre no puede contener números ni estar vacío.")
        nombre = input("Por favor, reingrese un nombre válido: ")

    pos = buscar_jugador(nombre, jugadores_par_impar, cant_jugadores_par_impar)

    if pos == -1:
        if cant_jugadores_par_impar < MAX_JUGADORES:
            pos = cant_jugadores_par_impar
            jugadores_par_impar[pos] = nombre
            cant_jugadores_par_impar = cant_jugadores_par_impar + 1
        else:
            print("Error. Se permiten como máximo " + str(MAX_JUGADORES) + " jugadores en este juego.")
            input("Presione Enter para continuar...")
            return
        
    if saldo_par_impar[pos] <= 0:
        print("Lo sentimos, " + nombre + ", no tienes créditos para jugar.")
        input("Presione Enter para continuar...")
        return
    continua="S"

    while continua.upper()=="S":
        os.system("cls")
        print("Usted tiene $",saldo_par_impar[pos]," créditos disponibles para jugar")
        apuesta=input("¿Cuántos créditos desea apostar en la siguiente jugada?: ")
        while(not apuesta.isdigit() or int(apuesta) > saldo_par_impar[pos] or int(apuesta) <= 0):
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
            saldo_par_impar[pos] = saldo_par_impar[pos] + apuesta
            cont_victorias_par_impar[pos] = cont_victorias_par_impar[pos] + 1
            cont_veces_jugadas_par_impar[pos] = cont_veces_jugadas_par_impar[pos] + 1
        else:
            if (eleccion.lower()=="impar" and secreto % 2 == 1):
                input("\nAdivinaste! " + str(secreto) + " es Impar. Tu apuesta de " + str(apuesta) + " créditos se ha duplicado! ")
                saldo_par_impar[pos] = saldo_par_impar[pos] + apuesta
                cont_victorias_par_impar[pos] = cont_victorias_par_impar[pos] + 1
                cont_veces_jugadas_par_impar[pos] = cont_veces_jugadas_par_impar[pos] + 1
            else:
                if secreto % 2 == 0:
                    paridad = "Par."
                else:
                    paridad = "Impar."
                input("\nOh no!! Fallaste... La suma de los dados es " + str(secreto) + " que es un número " + paridad + " Tu apuesta de " + str(apuesta) + " créditos se perdió... ")
                saldo_par_impar[pos] = saldo_par_impar[pos] - apuesta
                cont_veces_jugadas_par_impar[pos] = cont_veces_jugadas_par_impar[pos] + 1
                print("Tu saldo actual es de $", saldo_par_impar[pos], " créditos")
        os.system("cls")
        print("Tu saldo actual es de $", saldo_par_impar[pos], " créditos")
        if saldo_par_impar[pos] == 0:
            input("Que mal... te quedaste sin créditos!! Presione Enter para salir del juego...")
            continua = "N"
        else:
            continua=input("¿Desea volver a jugar? Ingrese S para si o N para no: ")
            while(continua.upper()!="S" and continua.upper()!="N"):
                continua=input("Ingrese una opción valida: ")

"""
Declarativa de funciones y variables del Reporte
titulo, etiqueta_valor, nombre_buscado : str
i, j, cantidad, pos : int
ascendente, intercambiar, jugo_algo : bool
nombres, valores, nombres_copia, valores_copia : list / array.array
"""
def copiar_arreglo_int(origen, cantidad):
    copia = [0] * cantidad
    for i in range(cantidad):
        copia[i] = origen[i]
    return copia

def copiar_arreglo_str(origen, cantidad):
    copia = [""] * cantidad
    for i in range(cantidad):
        copia[i] = origen[i]
    return copia

def ordenar_por_valor(nombres, valores, cantidad, ascendente):
    for i in range(cantidad):
        for j in range(cantidad - i - 1):
            if ascendente:
                intercambiar = valores[j] > valores[j + 1]
            else:
                intercambiar = valores[j] < valores[j + 1]

            if intercambiar:
                temp_valor = valores[j]
                valores[j] = valores[j + 1]
                valores[j + 1] = temp_valor

                temp_nombre = nombres[j]
                nombres[j] = nombres[j + 1]
                nombres[j + 1] = temp_nombre

def mostrar_ranking(titulo, jugadores, valores, cantidad, ascendente, etiqueta_valor):
    print(titulo)
    if cantidad == 0:
        print("   No hay jugadores registrados en este juego todavía.\n")
        return

    nombres_copia = copiar_arreglo_str(jugadores, cantidad)
    valores_copia = copiar_arreglo_int(valores, cantidad)
    ordenar_por_valor(nombres_copia, valores_copia, cantidad, ascendente)

    for i in range(cantidad):
        print("   " + str(i + 1) + ". " + nombres_copia[i] + " - " + etiqueta_valor + ": " + str(valores_copia[i]))
    print()

def reporte_ranking_victorias():
    os.system("cls")
    print("........\033[93m\033[4mRANKING DE VICTORIAS POR JUEGO\033[0m........\n")
    mostrar_ranking("\033[91mNúmero Secreto:\033[0m", jugadores_numero_secreto, cont_victorias_numero_secreto, cant_jugadores_numero_secreto, False, "victorias")
    mostrar_ranking("\033[94mBlackJack Simple:\033[0m", jugadores_blackjack, cont_victorias_blackjack, cant_jugadores_blackjack, False, "victorias")
    mostrar_ranking("\033[95mPar o Impar:\033[0m", jugadores_par_impar, cont_victorias_par_impar, cant_jugadores_par_impar, False, "victorias")
    input("Presione Enter para continuar...")

def reporte_juegos_de_jugador():
    os.system("cls")
    print("........\033[93m\033[4mJUEGOS JUGADOS POR UN JUGADOR\033[0m........\n")
    nombre_buscado = input("Ingrese el nombre del jugador a consultar: ")

    jugo_algo = False

    pos = buscar_jugador(nombre_buscado, jugadores_mayor_menor, cant_jugadores_mayor_menor)
    if pos != -1:
        jugo_algo = True
        print("\033[96mMayor o Menor:\033[0m mejor racha de " + str(mejor_racha_mayor_menor[pos]) + " aciertos (" + str(cont_veces_jugadas_mayor_menor[pos]) + " partidas jugadas)")

    pos = buscar_jugador(nombre_buscado, jugadores_numero_secreto, cant_jugadores_numero_secreto)
    if pos != -1:
        jugo_algo = True
        print("\033[91mNúmero Secreto:\033[0m " + str(cont_victorias_numero_secreto[pos]) + " victorias, " + str(cont_derrotas_numero_secreto[pos]) + " derrotas (" + str(cont_veces_jugadas_numero_secreto[pos]) + " partidas jugadas)")

    pos = buscar_jugador(nombre_buscado, jugadores_blackjack, cant_jugadores_blackjack)
    if pos != -1:
        jugo_algo = True
        print("\033[94mBlackJack Simple:\033[0m " + str(cont_victorias_blackjack[pos]) + " victorias (" + str(cont_veces_jugadas_blackjack[pos]) + " partidas jugadas)")

    pos = buscar_jugador(nombre_buscado, jugadores_par_impar, cant_jugadores_par_impar)
    if pos != -1:
        jugo_algo = True
        print("\033[95mPar o Impar:\033[0m crédito actual $" + str(saldo_par_impar[pos]) + ", " + str(cont_victorias_par_impar[pos]) + " aciertos (" + str(cont_veces_jugadas_par_impar[pos]) + " partidas jugadas)")

    if not jugo_algo:
        print("El jugador \"" + nombre_buscado + "\" no participó en ningún juego.")

    input("\nPresione Enter para continuar...")

def reporte_credito_par_impar():
    os.system("cls")
    print("........\033[93m\033[4mCRÉDITO EN PAR O IMPAR\033[0m........\n")
    mostrar_ranking("\033[95mPar o Impar (de menor a mayor crédito):\033[0m", jugadores_par_impar, saldo_par_impar, cant_jugadores_par_impar, True, "crédito")
    input("Presione Enter para continuar...")

def reporte_racha_mayor_menor():
    os.system("cls")
    print("........\033[93m\033[4mRACHA EN MAYOR O MENOR\033[0m........\n")
    nombre_buscado = input("Ingrese el nombre del jugador a consultar: ")
    pos = buscar_jugador(nombre_buscado, jugadores_mayor_menor, cant_jugadores_mayor_menor)

    if pos == -1:
        print("El jugador \"" + nombre_buscado + "\" no jugó a Mayor o Menor.")
    else:
        print(nombre_buscado + " tiene una mejor racha de " + str(mejor_racha_mayor_menor[pos]) + " aciertos en " + str(cont_veces_jugadas_mayor_menor[pos]) + " partidas jugadas.")

    input("\nPresione Enter para continuar...")

def reporte():
    total_jugadores = cant_jugadores_mayor_menor + cant_jugadores_numero_secreto + cant_jugadores_blackjack + cant_jugadores_par_impar

    if total_jugadores == 0:
        os.system("cls")
        print("No se han registrado juegos aún, por favor juegue alguna partida para generar un reporte.")
        input("Presione Enter para continuar...")
        return

    opc_reporte = " "
    while opc_reporte != "e":
        os.system("cls")
        print("........\033[93m\033[4mREPORTE DE JUEGOS\033[0m........ ")
        print("a- Ranking de victorias por juego (excepto Mayor o Menor)")
        print("b- Juegos jugados por un jugador")
        print("c- Crédito de jugadores de Par o Impar (de menor a mayor)")
        print("d- Racha de un jugador en Mayor o Menor")
        print("e- Volver al menú principal")

        opc_reporte = input("Ingrese su opción: ").lower()
        while opc_reporte != "a" and opc_reporte != "b" and opc_reporte != "c" and opc_reporte != "d" and opc_reporte != "e":
            opc_reporte = input("Ingreso inválido - reintente: ").lower()

        match opc_reporte:
            case "a": reporte_ranking_victorias()
            case "b": reporte_juegos_de_jugador()
            case "c": reporte_credito_par_impar()
            case "d": reporte_racha_mayor_menor()

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
    print("F- \033[97mFin DEL PROGRAMA\033[0m ")


# Inicio del programa
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
while opc != "f":
    menu()
    opc = str(input("Ingrese su opción: ")).lower()

    while len(opc) != 1 or opc < "a" or opc > "f":
        menu()
        opc = str(input("Ingreso Invalido - reintente: ")).lower()

    match opc:
        case "a": juego1()
        case "b": juego2()
        case "c": juego3()
        case "d": juego4()
        case "e": reporte()
        case "f": salir()
