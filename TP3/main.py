'''
Proyecto realizado por Joaquín del Castillo, Thiago Finoli, Guido Pacienzia y Lucas Ruberto
Comisión 1k05
Trabajo Práctico Nro. 3 - Suite de Juegos "Azar y Lógica" con registros y archivos
'''

import random, os, pickle, getpass

from TP2.main import juego1, juego2

"""
Declarativa de registros
Categoria:
    nro_categoria : int (consecutivo secuencial desde 1)
    nombre_categoria : str (30 caracteres)
    pregunta : str (200 caracteres)
    estado : str ("A" Activa / "I" Inactiva)
Opcion:
    nro_categoria : int (relaciona la opción con su categoría)
    nro_opcion : int (consecutivo dentro de la categoría)
    objeto : str (100 caracteres)
    valor : int
Jugador:
    nombre : str (30 caracteres)
    creditos : float
    juegos : matriz 2x4 de int
             fila 0 = veces que ganó, fila 1 = veces que perdió
             columna 0 = mayor/menor, 1 = número secreto, 2 = blackjack, 3 = par/impar
"""
class Categoria:
    def __init__(self):
        self.nro_categoria = 0          # entero
        self.nombre_categoria = " "     # string (30)
        self.pregunta = " "             # string (200)
        self.estado = "A"               # string: A = Activa, I = Inactiva

class Opcion:
    def __init__(self):
        self.nro_categoria = 0          # entero
        self.nro_opcion = 0             # entero
        self.objeto = " "               # string (100)
        self.valor = 0                  # entero

class Jugador:
    def __init__(self):
        self.nombre = " "                               # string (30)
        self.creditos = 0.00                            # real
        self.juegos = [[0] * 4 for i in range(2)]       # matriz 2x4 de enteros


"""
Declarativa de constantes globales
CARPETA, FD_CATEGORIAS, FD_OPCIONES, FD_JUGADORES : str (todos los archivos quedan en la carpeta c:\\tp3\\)
LARGO_NOMBRE, LARGO_NOMBRE_CATEGORIA, LARGO_PREGUNTA, LARGO_OBJETO : int
CREDITO_INICIAL : float
FILA_GANADAS, FILA_PERDIDAS : int (filas de la matriz juegos)
JUEGO_MAYOR_MENOR, JUEGO_NUMERO_SECRETO, JUEGO_BLACKJACK, JUEGO_PAR_IMPAR, CANT_JUEGOS : int (columnas de la matriz juegos)
"""
CARPETA = "c:\\tp3\\"
FD_CATEGORIAS = CARPETA + "categorias.dat"
FD_OPCIONES = CARPETA + "opciones.dat"
FD_JUGADORES = CARPETA + "jugadores.dat"

LARGO_NOMBRE = 30
LARGO_NOMBRE_CATEGORIA = 30
LARGO_PREGUNTA = 200
LARGO_OBJETO = 100

CREDITO_INICIAL = 10000.00

FILA_GANADAS = 0
FILA_PERDIDAS = 1

JUEGO_MAYOR_MENOR = 0
JUEGO_NUMERO_SECRETO = 1
JUEGO_BLACKJACK = 2
JUEGO_PAR_IMPAR = 3
CANT_JUEGOS = 4


"""
Declarativa de funciones y variables generales
cadena, resultado, mensaje, dato, respuesta, nombre : str
largo, i, inicio, fin, cant_puntos, cant_digitos : int
creditos, apuesta, valor : float
valido, tiene_digitos : bool
"""

def ajustar_cadena(cadena, largo):
    # Devuelve la cadena con exactamente 'largo' caracteres: la recorta o la completa con espacios,
    # así todos los registros guardan los campos de texto con longitud fija.
    resultado = ""
    for i in range(largo):
        if i < len(cadena):
            resultado = resultado + cadena[i]
        else:
            resultado = resultado + " "
    return resultado

def recortar(cadena):
    # Quita los espacios del principio y del final de la cadena
    inicio = 0
    while inicio < len(cadena) and cadena[inicio] == " ":
        inicio = inicio + 1
    fin = len(cadena) - 1
    while fin >= inicio and cadena[fin] == " ":
        fin = fin - 1
    resultado = ""
    for i in range(inicio, fin + 1):
        resultado = resultado + cadena[i]
    return resultado

def es_real(cadena):
    # Admite dígitos con, como máximo, un punto decimal (sin signo)
    valido = True
    cant_puntos = 0
    cant_digitos = 0
    i = 0
    while valido and i < len(cadena):
        if cadena[i] == ".":
            cant_puntos = cant_puntos + 1
            if cant_puntos > 1:
                valido = False
        elif cadena[i] >= "0" and cadena[i] <= "9":
            cant_digitos = cant_digitos + 1
        else:
            valido = False
        i = i + 1
    return valido and cant_digitos > 0

def contiene_digitos(cadena):
    tiene_digitos = False
    i = 0
    while i < len(cadena) and not tiene_digitos:
        if cadena[i] >= "0" and cadena[i] <= "9":
            tiene_digitos = True
        i = i + 1
    return tiene_digitos

def validar_texto(cadena, largo):
    return len(cadena) > 0 and len(cadena) <= largo

def validar_nombre(cadena):
    return validar_texto(cadena, LARGO_NOMBRE) and not contiene_digitos(cadena)

def formato_creditos(valor):
    return f"${valor:.2f}"

def pedir_texto(mensaje, largo):
    dato = recortar(input(mensaje))
    while not validar_texto(dato, largo):
        print("Error: el texto no puede estar vacío ni superar los " + str(largo) + " caracteres.")
        dato = recortar(input(mensaje))
    return dato

def pedir_entero(mensaje):
    dato = recortar(input(mensaje))
    while not dato.isdigit():
        print("Error: debe ingresar un número entero.")
        dato = recortar(input(mensaje))
    return int(dato)

def pedir_si_no(mensaje):
    respuesta = recortar(input(mensaje + " Ingrese S para sí o N para no: ")).upper()
    while respuesta != "S" and respuesta != "N":
        respuesta = recortar(input("Opción inválida. Ingrese S para sí o N para no: ")).upper()
    return respuesta

def pedir_nombre_jugador():
    nombre = recortar(input("Ingrese su nombre: "))
    while not validar_nombre(nombre):
        print("Error: el nombre no puede estar vacío, contener números ni superar los " + str(LARGO_NOMBRE) + " caracteres.")
        nombre = recortar(input("Por favor, reingrese un nombre válido: "))
    return nombre

def pedir_apuesta(creditos):
    apuesta = 0.00
    while apuesta <= 0 or apuesta > creditos:
        dato = recortar(input("¿Cuántos créditos desea apostar? (disponible " + formato_creditos(creditos) + "): "))
        if not es_real(dato):
            print("Error: debe ingresar un número positivo (use punto para los decimales).")
        else:
            apuesta = round(float(dato), 2)
            if apuesta <= 0:
                print("Error: la apuesta debe ser mayor a 0.")
            elif apuesta > creditos:
                print("Error: no puede apostar más de lo que tiene (" + formato_creditos(creditos) + ").")
    return apuesta


"""
Declarativa de funciones y variables de manejo de archivos (acceso directo con pickle)
fd, fd_aux : str (nombre físico del archivo)
archivo, original, auxiliar : file (archivo binario)
pos, pos_actual, pos_reemplazo, tam, tam_anterior, cantidad : int
reg, reg_nuevo : Categoria / Opcion / Jugador
"""
def abrir_archivo(fd):
    if not os.path.exists(fd):
        archivo = open(fd, "w+b")
    else:
        archivo = open(fd, "r+b")
    return archivo

def leer_registro(fd, pos):
    archivo = open(fd, "rb")
    archivo.seek(pos, 0)
    reg = pickle.load(archivo)
    archivo.close()
    return reg

def agregar_registro(fd, reg):
    # Graba el registro al final del archivo y devuelve la posición (en bytes) donde quedó
    archivo = abrir_archivo(fd)
    archivo.seek(0, 2)
    pos = archivo.tell()
    pickle.dump(reg, archivo)
    archivo.close()
    return pos

def reescribir_archivo(fd, pos_reemplazo, reg_nuevo):
    # Copia el archivo a uno auxiliar reemplazando el registro de la posición indicada
    fd_aux = fd + ".aux"
    original = open(fd, "rb")
    auxiliar = open(fd_aux, "wb")
    tam = os.path.getsize(fd)
    while original.tell() < tam:
        pos_actual = original.tell()
        reg = pickle.load(original)
        if pos_actual == pos_reemplazo:
            pickle.dump(reg_nuevo, auxiliar)
        else:
            pickle.dump(reg, auxiliar)
    original.close()
    auxiliar.close()
    os.remove(fd)
    os.rename(fd_aux, fd)

def modificar_registro(fd, pos, reg):
    # Acceso directo: se posiciona en el registro y lo regraba en el mismo lugar.
    # Pickle puede cambiar el tamaño del registro (por ejemplo, un contador que pasa de 255
    # o un texto con tildes), y en ese caso pisaría el registro siguiente: por eso, si el
    # tamaño cambió, se reescribe el archivo completo.
    archivo = open(fd, "r+b")
    archivo.seek(pos, 0)
    pickle.load(archivo)
    tam_anterior = archivo.tell() - pos
    if len(pickle.dumps(reg)) == tam_anterior:
        archivo.seek(pos, 0)
        pickle.dump(reg, archivo)
        archivo.close()
    else:
        archivo.close()
        reescribir_archivo(fd, pos, reg)

def contar_registros(fd):
    cantidad = 0
    if os.path.exists(fd):
        archivo = open(fd, "rb")
        tam = os.path.getsize(fd)
        while archivo.tell() < tam:
            pickle.load(archivo)
            cantidad = cantidad + 1
        archivo.close()
    return cantidad


"""
Declarativa de funciones y variables de Jugadores
nombre : str
pos, pos_actual, tam, juego : int
gano : bool
variacion_creditos : float
jug : Jugador
"""
def buscar_jugador(nombre):
    # Devuelve la posición del jugador en el archivo, o -1 si no existe
    pos = -1
    if os.path.exists(FD_JUGADORES):
        archivo = open(FD_JUGADORES, "rb")
        tam = os.path.getsize(FD_JUGADORES)
        while archivo.tell() < tam and pos == -1:
            pos_actual = archivo.tell()
            jug = pickle.load(archivo)
            if recortar(jug.nombre) == nombre:
                pos = pos_actual
        archivo.close()
    return pos

def alta_jugador(nombre):
    jug = Jugador()
    jug.nombre = ajustar_cadena(nombre, LARGO_NOMBRE)
    jug.creditos = CREDITO_INICIAL
    return agregar_registro(FD_JUGADORES, jug)

def identificar_jugador():
    # Pide el nombre; si el jugador no existe lo da de alta. Devuelve su posición en el archivo.
    nombre = pedir_nombre_jugador()
    pos = buscar_jugador(nombre)
    if pos == -1:
        pos = alta_jugador(nombre)
        print("¡Bienvenido/a " + nombre + "! Quedó registrado/a con un crédito inicial de " + formato_creditos(CREDITO_INICIAL) + ".")
    else:
        jug = leer_registro(FD_JUGADORES, pos)
        print("¡Hola de nuevo, " + nombre + "! Créditos disponibles: " + formato_creditos(jug.creditos) + ".")
    return pos

def registrar_resultado(pos, juego, gano, variacion_creditos):
    jug = leer_registro(FD_JUGADORES, pos)
    if gano:
        jug.juegos[FILA_GANADAS][juego] = jug.juegos[FILA_GANADAS][juego] + 1
    else:
        jug.juegos[FILA_PERDIDAS][juego] = jug.juegos[FILA_PERDIDAS][juego] + 1
    jug.creditos = round(jug.creditos + variacion_creditos, 2)
    modificar_registro(FD_JUGADORES, pos, jug)


"""
Declarativa de funciones y variables de Categorías y Opciones
nombre, objeto, linea : str
pos, pos_actual, pos_excluida, tam, nro, nro_categoria, ultimo, cantidad : int
solo_activas, existe : bool
cat : Categoria
op : Opcion
"""
def buscar_categoria_por_numero(nro):
    pos = -1
    if os.path.exists(FD_CATEGORIAS):
        archivo = open(FD_CATEGORIAS, "rb")
        tam = os.path.getsize(FD_CATEGORIAS)
        while archivo.tell() < tam and pos == -1:
            pos_actual = archivo.tell()
            cat = pickle.load(archivo)
            if cat.nro_categoria == nro:
                pos = pos_actual
        archivo.close()
    return pos

def buscar_categoria_por_nombre(nombre):
    # Las mayúsculas y minúsculas no se distinguen
    pos = -1
    if os.path.exists(FD_CATEGORIAS):
        archivo = open(FD_CATEGORIAS, "rb")
        tam = os.path.getsize(FD_CATEGORIAS)
        while archivo.tell() < tam and pos == -1:
            pos_actual = archivo.tell()
            cat = pickle.load(archivo)
            if recortar(cat.nombre_categoria).lower() == nombre.lower():
                pos = pos_actual
        archivo.close()
    return pos

def proximo_nro_categoria():
    ultimo = 0
    if os.path.exists(FD_CATEGORIAS):
        archivo = open(FD_CATEGORIAS, "rb")
        tam = os.path.getsize(FD_CATEGORIAS)
        while archivo.tell() < tam:
            cat = pickle.load(archivo)
            if cat.nro_categoria > ultimo:
                ultimo = cat.nro_categoria
        archivo.close()
    return ultimo + 1

def mostrar_categorias(solo_activas):
    # Lista número y nombre de las categorías y devuelve cuántas mostró
    cantidad = 0
    if os.path.exists(FD_CATEGORIAS):
        archivo = open(FD_CATEGORIAS, "rb")
        tam = os.path.getsize(FD_CATEGORIAS)
        while archivo.tell() < tam:
            cat = pickle.load(archivo)
            if not solo_activas or cat.estado == "A":
                cantidad = cantidad + 1
                linea = "   " + str(cat.nro_categoria) + " - " + recortar(cat.nombre_categoria)
                if cat.estado == "I":
                    linea = linea + " (inactiva)"
                print(linea)
        archivo.close()
    return cantidad

def pedir_categoria(solo_activas):
    # Pide un número de categoría existente (y activa si se indica) y devuelve su posición en el archivo
    pos = -1
    while pos == -1:
        nro = pedir_entero("Ingrese el número de categoría: ")
        pos = buscar_categoria_por_numero(nro)
        if pos == -1:
            print("Error: no existe una categoría con el número " + str(nro) + ".")
        elif solo_activas:
            cat = leer_registro(FD_CATEGORIAS, pos)
            if cat.estado != "A":
                print("Error: la categoría " + str(nro) + " está inactiva.")
                pos = -1
    return pos

def pedir_nombre_categoria(pos_excluida):
    # Pide un nombre que no esté usado por otra categoría (pos_excluida permite conservar el propio al modificar)
    nombre = pedir_texto("Ingrese el nombre de la categoría: ", LARGO_NOMBRE_CATEGORIA)
    pos = buscar_categoria_por_nombre(nombre)
    while pos != -1 and pos != pos_excluida:
        print("Error: ya existe una categoría llamada \"" + nombre + "\" (no se distinguen mayúsculas de minúsculas).")
        nombre = pedir_texto("Ingrese el nombre de la categoría: ", LARGO_NOMBRE_CATEGORIA)
        pos = buscar_categoria_por_nombre(nombre)
    return nombre

def contar_opciones(nro_categoria):
    cantidad = 0
    if os.path.exists(FD_OPCIONES):
        archivo = open(FD_OPCIONES, "rb")
        tam = os.path.getsize(FD_OPCIONES)
        while archivo.tell() < tam:
            op = pickle.load(archivo)
            if op.nro_categoria == nro_categoria:
                cantidad = cantidad + 1
        archivo.close()
    return cantidad

def existe_objeto(nro_categoria, objeto):
    existe = False
    if os.path.exists(FD_OPCIONES):
        archivo = open(FD_OPCIONES, "rb")
        tam = os.path.getsize(FD_OPCIONES)
        while archivo.tell() < tam and not existe:
            op = pickle.load(archivo)
            if op.nro_categoria == nro_categoria and recortar(op.objeto).lower() == objeto.lower():
                existe = True
        archivo.close()
    return existe

def mostrar_opciones(nro_categoria):
    cantidad = 0
    if os.path.exists(FD_OPCIONES):
        archivo = open(FD_OPCIONES, "rb")
        tam = os.path.getsize(FD_OPCIONES)
        while archivo.tell() < tam:
            op = pickle.load(archivo)
            if op.nro_categoria == nro_categoria:
                cantidad = cantidad + 1
                print("   " + str(op.nro_opcion) + ". " + recortar(op.objeto) + " - Valor: " + str(op.valor))
        archivo.close()
    return cantidad


"""
Declarativa de funciones y variables de la carga inicial de datos
archivo : file
nro, nro_categoria, nro_opcion, valor : int
nombre, pregunta, objeto : str
cat : Categoria
op : Opcion
"""
def grabar_categoria_inicial(archivo, nro, nombre, pregunta):
    cat = Categoria()
    cat.nro_categoria = nro
    cat.nombre_categoria = ajustar_cadena(nombre, LARGO_NOMBRE_CATEGORIA)
    cat.pregunta = ajustar_cadena(pregunta, LARGO_PREGUNTA)
    cat.estado = "A"
    pickle.dump(cat, archivo)

def grabar_opcion_inicial(archivo, nro_categoria, nro_opcion, objeto, valor):
    op = Opcion()
    op.nro_categoria = nro_categoria
    op.nro_opcion = nro_opcion
    op.objeto = ajustar_cadena(objeto, LARGO_OBJETO)
    op.valor = valor
    pickle.dump(op, archivo)

def crear_datos_iniciales():
    # Todas las preguntas están formuladas de modo que la respuesta correcta es la de MAYOR valor
    archivo = open(FD_CATEGORIAS, "wb")
    grabar_categoria_inicial(archivo, 1, "Edad Famosos", "¿Quién es más joven? (valor: año de nacimiento)")
    grabar_categoria_inicial(archivo, 2, "Duración Películas", "¿Qué película dura más? (valor: minutos)")
    grabar_categoria_inicial(archivo, 3, "Habitantes Países", "¿Qué país tiene más habitantes? (valor: millones de habitantes)")
    grabar_categoria_inicial(archivo, 4, "Estreno Películas", "¿Qué película se estrenó más recientemente? (valor: año de estreno)")
    grabar_categoria_inicial(archivo, 5, "Edad de Famosos", "¿Quién es mayor?")
    grabar_categoria_inicial(archivo, 6, "Area de Paises(km²)", "¿Que pais es mas grande?")
    grabar_categoria_inicial(archivo, 7, "Velocidad de Animales(km/h)", "¿Que animal es mas rapido?")
    archivo.close()

    archivo = open(FD_OPCIONES, "wb")
    grabar_opcion_inicial(archivo, 1, 1, "Lionel Messi", 1987)
    grabar_opcion_inicial(archivo, 1, 2, "Cristiano Ronaldo", 1985)
    grabar_opcion_inicial(archivo, 1, 3, "Shakira", 1977)
    grabar_opcion_inicial(archivo, 1, 4, "Tom Cruise", 1962)
    grabar_opcion_inicial(archivo, 1, 5, "Taylor Swift", 1989)
    grabar_opcion_inicial(archivo, 1, 6, "Bad Bunny", 1994)
    grabar_opcion_inicial(archivo, 1, 7, "Emilia Mernes", 1996)
    grabar_opcion_inicial(archivo, 1, 8, "Ricardo Darín", 1957)
    grabar_opcion_inicial(archivo, 1, 9, "Mirtha Legrand", 1927)
    grabar_opcion_inicial(archivo, 1, 10, "Lali Espósito", 1991)

    grabar_opcion_inicial(archivo, 2, 1, "Titanic", 194)
    grabar_opcion_inicial(archivo, 2, 2, "El Padrino", 175)
    grabar_opcion_inicial(archivo, 2, 3, "Toy Story", 81)
    grabar_opcion_inicial(archivo, 2, 4, "El Señor de los Anillos: El Retorno del Rey", 201)
    grabar_opcion_inicial(archivo, 2, 5, "Avengers: Endgame", 181)
    grabar_opcion_inicial(archivo, 2, 6, "Relatos Salvajes", 122)
    grabar_opcion_inicial(archivo, 2, 7, "El Secreto de sus Ojos", 129)
    grabar_opcion_inicial(archivo, 2, 8, "Shrek", 90)
    grabar_opcion_inicial(archivo, 2, 9, "Oppenheimer", 180)
    grabar_opcion_inicial(archivo, 2, 10, "Interestelar", 169)

    grabar_opcion_inicial(archivo, 3, 1, "India", 1441)
    grabar_opcion_inicial(archivo, 3, 2, "China", 1410)
    grabar_opcion_inicial(archivo, 3, 3, "Estados Unidos", 341)
    grabar_opcion_inicial(archivo, 3, 4, "Brasil", 212)
    grabar_opcion_inicial(archivo, 3, 5, "México", 130)
    grabar_opcion_inicial(archivo, 3, 6, "Japón", 124)
    grabar_opcion_inicial(archivo, 3, 7, "Alemania", 84)
    grabar_opcion_inicial(archivo, 3, 8, "España", 48)
    grabar_opcion_inicial(archivo, 3, 9, "Argentina", 46)
    grabar_opcion_inicial(archivo, 3, 10, "Uruguay", 3)

    grabar_opcion_inicial(archivo, 4, 1, "Star Wars", 1977)
    grabar_opcion_inicial(archivo, 4, 2, "Volver al Futuro", 1985)
    grabar_opcion_inicial(archivo, 4, 3, "Jurassic Park", 1993)
    grabar_opcion_inicial(archivo, 4, 4, "Toy Story", 1995)
    grabar_opcion_inicial(archivo, 4, 5, "Matrix", 1999)
    grabar_opcion_inicial(archivo, 4, 6, "Gladiador", 2000)
    grabar_opcion_inicial(archivo, 4, 7, "Avatar", 2009)
    grabar_opcion_inicial(archivo, 4, 8, "Frozen", 2013)
    grabar_opcion_inicial(archivo, 4, 9, "Coco", 2017)
    grabar_opcion_inicial(archivo, 4, 10, "Barbie", 2023)

    grabar_opcion_inicial(archivo, 5, 1, "Mirtha Legrand", 99)
    grabar_opcion_inicial(archivo, 5, 2, "Paul McCartney", 84)
    grabar_opcion_inicial(archivo, 5, 3, "Susana Gimenez", 82)
    grabar_opcion_inicial(archivo, 5, 4, "Guillermo Francella", 71)
    grabar_opcion_inicial(archivo, 5, 5, "Tom Hanks", 70)
    grabar_opcion_inicial(archivo, 5, 6, "Ricardo Darin", 69)
    grabar_opcion_inicial(archivo, 5, 7, "Marcelo Tinelli", 66)
    grabar_opcion_inicial(archivo, 5, 8, "Tom Cruise", 64)
    grabar_opcion_inicial(archivo, 5, 9, "Fito Paez", 63)
    grabar_opcion_inicial(archivo, 5, 10, "Brad Pitt", 62)
    grabar_opcion_inicial(archivo, 5, 11, "Elon Musk", 55)
    grabar_opcion_inicial(archivo, 5, 12, "Shakira", 49)
    grabar_opcion_inicial(archivo, 5, 13, "Mark Zuckerberg", 42)
    grabar_opcion_inicial(archivo, 5, 14, "Cristiano Ronaldo", 41)
    grabar_opcion_inicial(archivo, 5, 15, "Lady Gaga", 40)
    grabar_opcion_inicial(archivo, 5, 16, "Lionel Messi", 39)
    grabar_opcion_inicial(archivo, 5, 17, "Angel Di Maria", 38)
    grabar_opcion_inicial(archivo, 5, 18, "Taylor Swift", 36)
    grabar_opcion_inicial(archivo, 5, 19, "Neymar", 34)
    grabar_opcion_inicial(archivo, 5, 20, "Bad Bunny", 32)
    grabar_opcion_inicial(archivo, 5, 21, "Tini Stoessel", 29)
    grabar_opcion_inicial(archivo, 5, 22, "Kylian Mbappe", 27)
    grabar_opcion_inicial(archivo, 5, 23, "Lamine Yamal", 19)

    grabar_opcion_inicial(archivo, 6, 1, "Rusia", 17098000)
    grabar_opcion_inicial(archivo, 6, 2, "Canada", 9985000)
    grabar_opcion_inicial(archivo, 6, 3, "Brasil", 8516000)
    grabar_opcion_inicial(archivo, 6, 4, "Australia", 7692000)
    grabar_opcion_inicial(archivo, 6, 5, "India", 3287000)
    grabar_opcion_inicial(archivo, 6, 6, "Argentina", 2780000)
    grabar_opcion_inicial(archivo, 6, 7, "Kazajistan", 2725000)
    grabar_opcion_inicial(archivo, 6, 8, "Argelia", 2382000)
    grabar_opcion_inicial(archivo, 6, 9, "RD Congo", 2345000)
    grabar_opcion_inicial(archivo, 6, 10, "Arabia Saudita", 2150000)
    grabar_opcion_inicial(archivo, 6, 11, "Mexico", 1964000)
    grabar_opcion_inicial(archivo, 6, 12, "Indonesia", 1905000)
    grabar_opcion_inicial(archivo, 6, 13, "Libia", 1760000)
    grabar_opcion_inicial(archivo, 6, 14, "Iran", 1648000)
    grabar_opcion_inicial(archivo, 6, 15, "Mongolia", 1564000)
    grabar_opcion_inicial(archivo, 6, 16, "Peru", 1285000)
    grabar_opcion_inicial(archivo, 6, 17, "Colombia", 1142000)
    grabar_opcion_inicial(archivo, 6, 18, "Egipto", 1001000)
    grabar_opcion_inicial(archivo, 6, 19, "Venezuela", 916000)
    grabar_opcion_inicial(archivo, 6, 20, "Turquia", 784000)
    grabar_opcion_inicial(archivo, 6, 21, "Chile", 756000)
    grabar_opcion_inicial(archivo, 6, 22, "España", 506000)
    grabar_opcion_inicial(archivo, 6, 23, "Japon", 378000)
    grabar_opcion_inicial(archivo, 6, 24, "Alemania", 357000)
    grabar_opcion_inicial(archivo, 6, 25, "Italia", 301000)
    grabar_opcion_inicial(archivo, 6, 26, "Reino Unido", 244000)
    grabar_opcion_inicial(archivo, 6, 27, "Uruguay", 176000)
    grabar_opcion_inicial(archivo, 6, 28, "Grecia", 132000)
    grabar_opcion_inicial(archivo, 6, 29, "Portugal", 92000)
    grabar_opcion_inicial(archivo, 6, 30, "Suiza", 41000)

    grabar_opcion_inicial(archivo, 7, 1, "Halcon peregrino (en picada)", 389)
    grabar_opcion_inicial(archivo, 7, 2, "Aguila real (en picada)", 240)
    grabar_opcion_inicial(archivo, 7, 3, "Vencejo comun", 112)
    grabar_opcion_inicial(archivo, 7, 4, "Guepardo", 110)
    grabar_opcion_inicial(archivo, 7, 5, "Berrendo", 88)
    grabar_opcion_inicial(archivo, 7, 6, "Leon", 80)
    grabar_opcion_inicial(archivo, 7, 7, "Tiburon mako", 74)
    grabar_opcion_inicial(archivo, 7, 8, "Galgo", 72)
    grabar_opcion_inicial(archivo, 7, 9, "Avestruz", 70)
    grabar_opcion_inicial(archivo, 7, 10, "Coyote", 69)
    grabar_opcion_inicial(archivo, 7, 11, "Cebra", 65)
    grabar_opcion_inicial(archivo, 7, 12, "Lobo gris", 64)
    grabar_opcion_inicial(archivo, 7, 13, "Delfin comun", 60)
    grabar_opcion_inicial(archivo, 7, 14, "Leopardo", 58)
    grabar_opcion_inicial(archivo, 7, 15, "Bufalo africano", 57)
    grabar_opcion_inicial(archivo, 7, 16, "Orca", 56)
    grabar_opcion_inicial(archivo, 7, 17, "Rinoceronte negro", 55)
    grabar_opcion_inicial(archivo, 7, 18, "Zorro rojo", 50)
    grabar_opcion_inicial(archivo, 7, 19, "Gato domestico", 48)
    grabar_opcion_inicial(archivo, 7, 20, "Usain Bolt (humano)", 45)
    grabar_opcion_inicial(archivo, 7, 21, "Elefante africano", 40)
    grabar_opcion_inicial(archivo, 7, 22, "Pinguino papua", 36)
    grabar_opcion_inicial(archivo, 7, 23, "Tortuga laud", 35)
    grabar_opcion_inicial(archivo, 7, 24, "Hipopotamo", 30)
    grabar_opcion_inicial(archivo, 7, 25, "Abeja", 24)
    grabar_opcion_inicial(archivo, 7, 26, "Ardilla", 20)
    grabar_opcion_inicial(archivo, 7, 27, "Cocodrilo (en tierra)", 17)
    grabar_opcion_inicial(archivo, 7, 28, "Gallina", 14)
    grabar_opcion_inicial(archivo, 7, 29, "Raton", 13)
    grabar_opcion_inicial(archivo, 7, 30, "Mosca domestica", 7)
    archivo.close()


"""
Declarativa de funciones y variables juego 1: Mayor o Menor
MIN_OPCIONES_CATEGORIA, MAX_OPCIONES_CATEGORIA : int (constantes)
Posiciones_opciones : array de int, tamaño MAX_OPCIONES_CATEGORIA (posición en el archivo de cada opción
                      de la categoría elegida; -1 = opción ya sorteada en la partida)
cantidad_opc : int (cantidad de opciones cargadas en Posiciones_opciones)
pos, poscate, cat_elegida, correctas, rondas, eleccion, casillero, indice_carga : int
apuesta : float
continuar, nombrecate, preguntacate, texto_cate, texto_eleccion, texto_continuar : str
reg : Jugador
regcate : Categoria
op1, op2, opcion_sorteada : Opcion
"""
MIN_OPCIONES_CATEGORIA = 7
MAX_OPCIONES_CATEGORIA = 100
Posiciones_opciones = [-1] * MAX_OPCIONES_CATEGORIA
cantidad_opc = 0

def titulo_mayor_menor():
    print("\033[4m\033[96mMAYOR O MENOR\033[0m\n")

def contar_activas():
    cant_activas = 0
    if os.path.exists(FD_CATEGORIAS):
        arLoCate = open(FD_CATEGORIAS, "rb")
        tam_cate_cont = os.path.getsize(FD_CATEGORIAS)
        while arLoCate.tell() < tam_cate_cont:
            reg_cate_cont = pickle.load(arLoCate)
            if reg_cate_cont.estado == "A":
                cant_activas = cant_activas + 1
        arLoCate.close()
    return cant_activas

def muestracategorias():
    arLoCate = open(FD_CATEGORIAS, "rb")
    tam_cate_muestra = os.path.getsize(FD_CATEGORIAS)
    while arLoCate.tell() < tam_cate_muestra:
        reg_cate_muestra = pickle.load(arLoCate)
        if reg_cate_muestra.estado == "A":
            print(reg_cate_muestra.nro_categoria, "-", recortar(reg_cate_muestra.nombre_categoria))
    arLoCate.close()

def busqueda_categoria(nro_cate_buscada, solo_activas):
    pos_cate_encontrada = -1
    if os.path.exists(FD_CATEGORIAS):
        arLoCate = open(FD_CATEGORIAS, "rb")
        tam_cate_busq = os.path.getsize(FD_CATEGORIAS)
        while arLoCate.tell() < tam_cate_busq and pos_cate_encontrada == -1:
            pos_inicio_cate = arLoCate.tell()
            reg_cate_busq = pickle.load(arLoCate)
            if reg_cate_busq.nro_categoria == nro_cate_buscada:
                if not solo_activas or reg_cate_busq.estado == "A":
                    pos_cate_encontrada = pos_inicio_cate
        arLoCate.close()
    return pos_cate_encontrada

def determinaropciones(nro_cate_sorteo, es_primera):
    # La primera vez carga en Posiciones_opciones la posición de cada opción de la categoría.
    # En cada llamada sortea una que todavía no salió y la marca con -1.
    global Posiciones_opciones, cantidad_opc
    arLoOpc = open(FD_OPCIONES, "rb")
    if es_primera == True:
        tam_opc_sorteo = os.path.getsize(FD_OPCIONES)
        indice_carga = 0
        while arLoOpc.tell() < tam_opc_sorteo:
            pos_inicio_opc = arLoOpc.tell()
            reg_opc_sorteo = pickle.load(arLoOpc)
            if reg_opc_sorteo.nro_categoria == nro_cate_sorteo:
                Posiciones_opciones[indice_carga] = pos_inicio_opc
                indice_carga = indice_carga + 1
        cantidad_opc = indice_carga
    casillero = random.randint(0, cantidad_opc - 1)
    while Posiciones_opciones[casillero] == -1:
        casillero = random.randint(0, cantidad_opc - 1)
    arLoOpc.seek(Posiciones_opciones[casillero], 0)
    opcion_sorteada = pickle.load(arLoOpc)
    arLoOpc.close()
    Posiciones_opciones[casillero] = -1
    return opcion_sorteada

def pedir_categoria_mayor_menor():
    print("Categorias")
    muestracategorias()
    texto_cate = recortar(input("Selecciona una categoria para iniciar el juego: "))
    while not texto_cate.isdigit() or busqueda_categoria(int(texto_cate), True) == -1:
        texto_cate = recortar(input("Categoria invalida, elegi una de la lista: "))
    nro_cate_valida = int(texto_cate)
    return nro_cate_valida

def pedir_eleccion(opcion_izq, opcion_der):
    texto_eleccion = recortar(input("1- " + recortar(opcion_izq.objeto) + "  /  2- " + recortar(opcion_der.objeto) + ": "))
    while texto_eleccion != "1" and texto_eleccion != "2":
        print("Error: debe ingresar 1 o 2.")
        texto_eleccion = recortar(input("1- " + recortar(opcion_izq.objeto) + "  /  2- " + recortar(opcion_der.objeto) + ": "))
    eleccion_numero = int(texto_eleccion)
    return eleccion_numero

def preguntar_continuar():
    texto_continuar = recortar(input("¿Desea volver a jugar? (S/N): ")).upper()
    while texto_continuar != "S" and texto_continuar != "N":
        print("Error: ingrese S o N.")
        texto_continuar = recortar(input("¿Desea volver a jugar? (S/N): ")).upper()
    return texto_continuar

def juego_mayor_menor():
    os.system("cls")
    titulo_mayor_menor()
    pos = identificar_jugador()
    reg = leer_registro(FD_JUGADORES, pos)
    continuar = "S"
    while reg.creditos > 0 and continuar == "S":
        print()
        print("Saldo actual:", reg.creditos)
        if contar_activas() == 0:
            print("No hay categorias activas. Un administrador debe dar de alta alguna.")
            continuar = "N"
        else:
            apuesta = pedir_apuesta(reg.creditos)
            cat_elegida = pedir_categoria_mayor_menor()
            if contar_opciones(cat_elegida) < MIN_OPCIONES_CATEGORIA:
                print("Esa categoria tiene menos de " + str(MIN_OPCIONES_CATEGORIA) + " opciones y no se puede jugar.")
                print("Un administrador debe agregar mas opciones.")
                continuar = "N"
            else:
                poscate = busqueda_categoria(cat_elegida, True)
                regcate = leer_registro(FD_CATEGORIAS, poscate)
                nombrecate = recortar(regcate.nombre_categoria)
                preguntacate = recortar(regcate.pregunta)
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
                    print("1-", recortar(op1.objeto), op1.valor, "/ 2-", recortar(op2.objeto), op2.valor)
                    if (eleccion == 1 and op1.valor >= op2.valor) or (eleccion == 2 and op2.valor >= op1.valor):
                        print("La respuesta es correcta!!!")
                        correctas = correctas + 1
                    else:
                        print("Ups... la respuesta es incorrecta...")
                    if rondas != 6:
                        input("Presione Enter para continuar...")
                        if op1.valor >= op2.valor:
                            op2 = determinaropciones(cat_elegida, False)
                        else:
                            op1 = determinaropciones(cat_elegida, False)
                print()
                print("Aciertos:", correctas, "de 6")
                if correctas >= 4:
                    print("Felicidades!!! Ha ganado", apuesta, "creditos!!!")
                    registrar_resultado(pos, JUEGO_MAYOR_MENOR, True, apuesta)
                else:
                    print("Oh, no... Usted ha perdido", apuesta, "creditos.")
                    registrar_resultado(pos, JUEGO_MAYOR_MENOR, False, -apuesta)
                reg = leer_registro(FD_JUGADORES, pos)
                print("Saldo actual:", reg.creditos)
                if reg.creditos > 0:
                    continuar = preguntar_continuar()
    if reg.creditos <= 0:
        print("No tiene mas creditos en su saldo")
    input("Presione Enter para continuar...")


"""
Declarativa de variables juego 2: Número Secreto
MAX_INTENTOS : int (constante, intentos disponibles por partida)
pos, numero_secreto, intentos : int
numero, nom : str
ganador : bool
"""
MAX_INTENTOS = 5

def juego_numero_secreto():
    os.system("cls")
    print("\033[4m\033[91mNÚMERO SECRETO\033[0m")
    pos = identificar_jugador()
    nom = recortar(leer_registro(FD_JUGADORES, pos).nombre)
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
            registrar_resultado(pos, JUEGO_NUMERO_SECRETO, True, 0)
        else:
            if intentos==0:
                print("Oh no, perdiste el juego")
                print("El número secreto era", numero_secreto)
                registrar_resultado(pos, JUEGO_NUMERO_SECRETO, False, 0)
    input("Presione Enter para continuar...")


"""
Declarativa de funciones y variables juego 3: Blackjack
CANT_CARTAS_MAZO, CANT_VALORES, MAX_CARTAS_MANO : int (constantes)
PALOS : str (constante, un símbolo por palo)
nombre, titular, texto_cartas, opcion_usuario, continua : str
pos, carta, valor, palo, total, cant_ases, puntos_jugador, puntos_banca, resultado, i : int
cant_cartas, cant_cartas_jugador, cant_cartas_banca : int
jugando : bool
mazo : array de bool, tamaño CANT_CARTAS_MAZO (True = carta ya repartida)
mano, mano_jugador, mano_banca : array de int, tamaño MAX_CARTAS_MANO
Cada carta es un número de 0 a 51: carta % 13 es su valor (0 = "2" ... 12 = "A") y carta // 13 su palo.
"""
CANT_CARTAS_MAZO = 52
CANT_VALORES = 13
MAX_CARTAS_MANO = 12
PALOS = "♠♥♦♣"

def titulo_blackjack():
    print("\033[4m\033[94mBLACKJACK SIMPLE\033[0m\n")

def repartir_carta(mazo):
    # Un solo mazo: se sortea hasta encontrar una carta que no se haya repartido
    carta = random.randint(0, CANT_CARTAS_MAZO - 1)
    while mazo[carta]:
        carta = random.randint(0, CANT_CARTAS_MAZO - 1)
    mazo[carta] = True
    return carta

def nombre_carta(carta):
    valor = carta % CANT_VALORES
    palo = carta // CANT_VALORES
    match valor:
        case _ if valor <= 8:
            nombre = str(valor + 2)
        case 9:
            nombre = "J"
        case 10:
            nombre = "Q"
        case 11:
            nombre = "K"
        case _:
            nombre = "A"
    return nombre + PALOS[palo]

def calcular_puntos(mano, cant_cartas):
    total = 0
    cant_ases = 0
    for i in range(cant_cartas):
        valor = mano[i] % CANT_VALORES
        match valor:
            case 12:
                total = total + 11
                cant_ases = cant_ases + 1
            case _ if valor >= 9:
                total = total + 10
            case _:
                total = total + (valor + 2)

    # Cada As vale 11, salvo que convenga contarlo como 1 para no pasarse de 21
    while total > 21 and cant_ases > 0:
        total = total - 10
        cant_ases = cant_ases - 1
    return total

def mostrar_mano(titular, mano, cant_cartas):
    texto_cartas = ""
    for i in range(cant_cartas):
        texto_cartas = texto_cartas + nombre_carta(mano[i]) + " "
    print(titular + ": " + texto_cartas + "(Total: " + str(calcular_puntos(mano, cant_cartas)) + ")")

def jugar_partida_blackjack(nombre):
    # Devuelve 1 si gana el jugador, -1 si gana la banca y 0 si hay empate
    mazo = [False] * CANT_CARTAS_MAZO
    mano_jugador = [0] * MAX_CARTAS_MANO
    mano_banca = [0] * MAX_CARTAS_MANO

    for i in range(2):
        mano_jugador[i] = repartir_carta(mazo)
    cant_cartas_jugador = 2
    for i in range(2):
        mano_banca[i] = repartir_carta(mazo)
    cant_cartas_banca = 2

    puntos_jugador = calcular_puntos(mano_jugador, cant_cartas_jugador)
    puntos_banca = calcular_puntos(mano_banca, cant_cartas_banca)

    print("Banca: " + nombre_carta(mano_banca[0]) + " [carta oculta]")
    mostrar_mano(nombre, mano_jugador, cant_cartas_jugador)

    jugando = puntos_jugador < 21
    while jugando:
        opcion_usuario = recortar(input("\n¿Desea Pedir otra carta o Plantarse?: ")).lower()
        while opcion_usuario != "pedir" and opcion_usuario != "plantarse":
            opcion_usuario = recortar(input("Ingrese una opción válida, Pedir o Plantarse: ")).lower()

        if opcion_usuario == "pedir":
            mano_jugador[cant_cartas_jugador] = repartir_carta(mazo)
            cant_cartas_jugador = cant_cartas_jugador + 1
            puntos_jugador = calcular_puntos(mano_jugador, cant_cartas_jugador)
            mostrar_mano(nombre, mano_jugador, cant_cartas_jugador)
            jugando = puntos_jugador < 21
        else:
            jugando = False

    if puntos_jugador > 21:
        print("\n\033[91mTe pasaste de 21 con " + str(puntos_jugador) + " puntos. ¡Perdiste!\033[0m")
        resultado = -1
    else:
        if puntos_jugador == 21:
            print("\n¡Llegaste a 21!")
        print("\nTurno de la Banca:")
        mostrar_mano("Banca", mano_banca, cant_cartas_banca)
        while puntos_banca < 17:
            mano_banca[cant_cartas_banca] = repartir_carta(mazo)
            cant_cartas_banca = cant_cartas_banca + 1
            puntos_banca = calcular_puntos(mano_banca, cant_cartas_banca)
            mostrar_mano("Banca", mano_banca, cant_cartas_banca)

        if puntos_banca > 21:
            print("\n\033[92mLa Banca se pasó de 21 con " + str(puntos_banca) + " puntos. ¡" + nombre + " gana!\033[0m")
            resultado = 1
        elif puntos_jugador > puntos_banca:
            print("\n\033[92m" + nombre + " gana con " + str(puntos_jugador) + " contra " + str(puntos_banca) + " de la Banca.\033[0m")
            resultado = 1
        elif puntos_jugador < puntos_banca:
            print("\n\033[91mLa Banca gana con " + str(puntos_banca) + " contra " + str(puntos_jugador) + " de " + nombre + ".\033[0m")
            resultado = -1
        else:
            print("\nEmpate entre " + nombre + " y la Banca con " + str(puntos_jugador) + " puntos.")
            resultado = 0
    return resultado

def juego_blackjack():
    os.system("cls")
    titulo_blackjack()
    pos = identificar_jugador()
    nombre = recortar(leer_registro(FD_JUGADORES, pos).nombre)
    print()

    continua = "S"
    while continua == "S":
        resultado = jugar_partida_blackjack(nombre)
        if resultado == 1:
            registrar_resultado(pos, JUEGO_BLACKJACK, True, 0)
        elif resultado == -1:
            registrar_resultado(pos, JUEGO_BLACKJACK, False, 0)

        continua = pedir_si_no("\n¿Desea jugar otra partida?")
        if continua == "S":
            os.system("cls")
            titulo_blackjack()


"""
Declarativa de variables juego 4: Par o Impar
eleccion, continua, paridad : str
pos, dado1, dado2, suma : int
apuesta : float
acerto : bool
jug : Jugador
"""
def titulo_par_impar():
    print("\033[4m\033[95mPAR O IMPAR\033[0m\n")

def juego_par_impar():
    os.system("cls")
    titulo_par_impar()
    pos = identificar_jugador()
    jug = leer_registro(FD_JUGADORES, pos)

    if jug.creditos <= 0:
        print("Lo sentimos, no tiene créditos para jugar.")
        input("\nPresione Enter para continuar...")
    else:
        continua = "S"
        while continua == "S":
            print("\nUsted tiene " + formato_creditos(jug.creditos) + " créditos disponibles.")
            apuesta = pedir_apuesta(jug.creditos)

            dado1 = random.randint(1, 6)
            dado2 = random.randint(1, 6)
            suma = dado1 + dado2

            eleccion = recortar(input("Se tiraron dos dados. ¿La suma es Par o Impar?: ")).lower()
            while eleccion != "par" and eleccion != "impar":
                eleccion = recortar(input("Ingrese una opción válida, Par o Impar: ")).lower()

            if suma % 2 == 0:
                paridad = "par"
            else:
                paridad = "impar"
            acerto = eleccion == paridad

            print("\nSalieron " + str(dado1) + " y " + str(dado2) + ": la suma es " + str(suma) + ", un número " + paridad + ".")
            if acerto:
                print("\033[92m¡Ganaste! Tu apuesta de " + formato_creditos(apuesta) + " se suma a tus créditos.\033[0m")
                registrar_resultado(pos, JUEGO_PAR_IMPAR, True, apuesta)
            else:
                print("\033[91mPerdiste... Tu apuesta de " + formato_creditos(apuesta) + " se resta de tus créditos.\033[0m")
                registrar_resultado(pos, JUEGO_PAR_IMPAR, False, -apuesta)

            jug = leer_registro(FD_JUGADORES, pos)
            print("Tu saldo actual es de " + formato_creditos(jug.creditos) + ".")

            if jug.creditos <= 0:
                print("Que mal... ¡te quedaste sin créditos!")
                input("\nPresione Enter para continuar...")
                continua = "N"
            else:
                continua = pedir_si_no("\n¿Desea volver a jugar?")
                if continua == "S":
                    os.system("cls")
                    titulo_par_impar()


"""
Declarativa de funciones y variables del Reporte
opc_reporte, nombre_buscado : str
pos, cantidad, juego, ganadas, perdidas, i, j : int
jugo_algo : bool
jugadores : array de Jugador, tamaño cantidad
jug, aux : Jugador
"""
def nombre_juego(juego):
    if juego == JUEGO_MAYOR_MENOR:
        nombre = "\033[96mMayor o Menor\033[0m"
    elif juego == JUEGO_NUMERO_SECRETO:
        nombre = "\033[91mNúmero Secreto\033[0m"
    elif juego == JUEGO_BLACKJACK:
        nombre = "\033[94mBlackJack Simple\033[0m"
    else:
        nombre = "\033[95mPar o Impar\033[0m"
    return nombre

def cargar_jugadores(cantidad):
    jugadores = [None] * cantidad
    archivo = open(FD_JUGADORES, "rb")
    for i in range(cantidad):
        jugadores[i] = pickle.load(archivo)
    archivo.close()
    return jugadores

def ordenar_por_creditos_descendente(jugadores, cantidad):
    # Ordenamiento por selección, de mayor a menor cantidad de créditos
    for i in range(cantidad - 1):
        for j in range(i + 1, cantidad):
            if jugadores[j].creditos > jugadores[i].creditos:
                aux = jugadores[i]
                jugadores[i] = jugadores[j]
                jugadores[j] = aux

def reporte_jugadores_por_creditos():
    os.system("cls")
    print("........\033[93m\033[4mJUGADORES POR CANTIDAD DE CRÉDITOS\033[0m........\n")
    cantidad = contar_registros(FD_JUGADORES)
    if cantidad == 0:
        print("Todavía no hay jugadores registrados.")
    else:
        jugadores = cargar_jugadores(cantidad)
        ordenar_por_creditos_descendente(jugadores, cantidad)
        for i in range(cantidad):
            print("   " + str(i + 1) + ". " + jugadores[i].nombre + " " + formato_creditos(jugadores[i].creditos))
    input("\nPresione Enter para continuar...")

def reporte_juegos_de_jugador():
    os.system("cls")
    print("........\033[93m\033[4mJUEGOS JUGADOS POR UN JUGADOR\033[0m........\n")
    nombre_buscado = recortar(input("Ingrese el nombre del jugador a consultar: "))
    pos = buscar_jugador(nombre_buscado)

    if pos == -1:
        print("El jugador \"" + nombre_buscado + "\" no está registrado.")
    else:
        jug = leer_registro(FD_JUGADORES, pos)
        print("\nJugador: " + recortar(jug.nombre))
        jugo_algo = False
        for juego in range(CANT_JUEGOS):
            ganadas = jug.juegos[FILA_GANADAS][juego]
            perdidas = jug.juegos[FILA_PERDIDAS][juego]
            if ganadas + perdidas > 0:
                jugo_algo = True
                print("   " + nombre_juego(juego) + ": ganó " + str(ganadas) + " y perdió " + str(perdidas) + " veces")
        if not jugo_algo:
            print("   Todavía no ganó ni perdió ninguna partida.")
        print("Créditos restantes: " + formato_creditos(jug.creditos))
    input("\nPresione Enter para continuar...")

def reporte():
    opc_reporte = " "
    while opc_reporte != "c":
        os.system("cls")
        print("........\033[93m\033[4mREPORTE\033[0m........ ")
        print("a- Lista de jugadores ordenados de mayor a menor por créditos")
        print("b- Juegos jugados por un jugador")
        print("c- Volver al menú principal")

        opc_reporte = recortar(input("Ingrese su opción: ")).lower()
        while opc_reporte != "a" and opc_reporte != "b" and opc_reporte != "c":
            opc_reporte = recortar(input("Ingreso inválido - reintente: ")).lower()

        match opc_reporte:
            case "a":
                reporte_jugadores_por_creditos()
            case "b":
                reporte_juegos_de_jugador()


"""
Declarativa de funciones y variables de Administración de Juegos
MAX_INTENTOS_CLAVE : int (constante)
clave, nombre, pregunta, objeto, confirma, otra, opc_admin, opc_categorias, opc_opciones : str
intentos, pos, nro_categoria, cantidad, valor : int
acceso : bool
cat : Categoria
op : Opcion
"""
MAX_INTENTOS_CLAVE = 3

def ingresar_clave_admin():
    # La contraseña no se muestra mientras se escribe (getpass)
    intentos = 0
    acceso = False
    while intentos < MAX_INTENTOS_CLAVE and not acceso:
        clave = getpass.getpass("Ingrese la contraseña de administrador: ")
        intentos = intentos + 1
        if clave == CLAVE_ADMIN:
            acceso = True
        elif intentos < MAX_INTENTOS_CLAVE:
            print("Contraseña incorrecta. Le quedan " + str(MAX_INTENTOS_CLAVE - intentos) + " intentos.")
    if not acceso:
        print("\nSuperó los 3 intentos de ingresar contraseña, salga e intente nuevamente")
        input("\nPresione Enter para continuar...")
    return acceso

def alta_categoria():
    os.system("cls")
    print("........\033[93m\033[4mALTA DE CATEGORÍA\033[0m........\n")
    nombre = pedir_nombre_categoria(-1)
    print("Formule la pregunta de modo que la respuesta correcta sea la opción de MAYOR valor.")
    pregunta = pedir_texto("Ingrese la pregunta: ", LARGO_PREGUNTA)

    cat = Categoria()
    cat.nro_categoria = proximo_nro_categoria()
    cat.nombre_categoria = ajustar_cadena(nombre, LARGO_NOMBRE_CATEGORIA)
    cat.pregunta = ajustar_cadena(pregunta, LARGO_PREGUNTA)
    cat.estado = "A"
    agregar_registro(FD_CATEGORIAS, cat)

    print("\nCategoría " + str(cat.nro_categoria) + " - " + nombre + " registrada correctamente.")
    print("Recuerde cargarle al menos " + str(MIN_OPCIONES_CATEGORIA) + " opciones para poder jugarla.")
    input("\nPresione Enter para continuar...")

def modificacion_categoria():
    os.system("cls")
    print("........\033[93m\033[4mMODIFICACIÓN DE CATEGORÍA\033[0m........\n")
    if mostrar_categorias(True) == 0:
        print("No hay categorías activas para modificar.")
    else:
        print()
        pos = pedir_categoria(True)
        cat = leer_registro(FD_CATEGORIAS, pos)
        print("Nombre actual: " + recortar(cat.nombre_categoria))
        nombre = pedir_nombre_categoria(pos)
        cat.nombre_categoria = ajustar_cadena(nombre, LARGO_NOMBRE_CATEGORIA)
        modificar_registro(FD_CATEGORIAS, pos, cat)
        print("\nLa categoría " + str(cat.nro_categoria) + " ahora se llama \"" + nombre + "\".")
    input("\nPresione Enter para continuar...")

def baja_categoria():
    os.system("cls")
    print("........\033[93m\033[4mBAJA DE CATEGORÍA\033[0m........\n")
    if mostrar_categorias(True) == 0:
        print("No hay categorías activas para dar de baja.")
    else:
        print()
        pos = pedir_categoria(True)
        cat = leer_registro(FD_CATEGORIAS, pos)
        confirma = pedir_si_no("¿Confirma la baja de la categoría \"" + recortar(cat.nombre_categoria) + "\"?")
        if confirma == "S":
            cat.estado = "I"
            modificar_registro(FD_CATEGORIAS, pos, cat)
            print("La categoría " + str(cat.nro_categoria) + " quedó Inactiva.")
        else:
            print("Baja cancelada.")
    input("\nPresione Enter para continuar...")

def administrar_categorias():
    opc_categorias = " "
    while opc_categorias != "4":
        os.system("cls")
        print("........\033[93m\033[4mADMINISTRAR CATEGORÍAS\033[0m........ ")
        print("1- Alta")
        print("2- Modificación")
        print("3- Baja")
        print("4- Volver")

        opc_categorias = recortar(input("Ingrese su opción: "))
        while opc_categorias != "1" and opc_categorias != "2" and opc_categorias != "3" and opc_categorias != "4":
            opc_categorias = recortar(input("Ingreso inválido - reintente: "))

        match opc_categorias:
            case "1":
                alta_categoria()
            case "2":
                modificacion_categoria()
            case "3":
                baja_categoria()

def alta_opciones():
    os.system("cls")
    print("........\033[93m\033[4mALTA DE OPCIONES\033[0m........\n")
    if mostrar_categorias(True) == 0:
        print("No hay categorías activas. Antes de registrar opciones se deben dar de alta categorías.")
        input("\nPresione Enter para continuar...")
    else:
        print()
        pos = pedir_categoria(True)
        cat = leer_registro(FD_CATEGORIAS, pos)
        nro_categoria = cat.nro_categoria
        print("\nCategoría: " + recortar(cat.nombre_categoria))
        print("Pregunta: " + recortar(cat.pregunta))

        otra = "S"
        while otra == "S":
            objeto = pedir_texto("\nObjeto: ", LARGO_OBJETO)
            while existe_objeto(nro_categoria, objeto):
                print("Error: \"" + objeto + "\" ya está cargado en esta categoría.")
                objeto = pedir_texto("Objeto: ", LARGO_OBJETO)
            valor = pedir_entero("Valor: ")

            op = Opcion()
            op.nro_categoria = nro_categoria
            op.nro_opcion = contar_opciones(nro_categoria) + 1
            op.objeto = ajustar_cadena(objeto, LARGO_OBJETO)
            op.valor = valor
            agregar_registro(FD_OPCIONES, op)
            print("Opción " + str(op.nro_opcion) + " registrada: " + objeto + " - Valor: " + str(valor))

            otra = pedir_si_no("\n¿Desea cargar otra opción en esta categoría?")

        cantidad = contar_opciones(nro_categoria)
        print("\nLa categoría tiene " + str(cantidad) + " opciones cargadas.")
        if cantidad < MIN_OPCIONES_CATEGORIA:
            print("Atención: hacen falta al menos " + str(MIN_OPCIONES_CATEGORIA) + " opciones para poder jugarla.")
        input("\nPresione Enter para continuar...")

def consulta_opciones():
    os.system("cls")
    print("........\033[93m\033[4mCONSULTA DE OPCIONES\033[0m........\n")
    if mostrar_categorias(False) == 0:
        print("No hay categorías registradas.")
    else:
        print()
        pos = pedir_categoria(False)
        cat = leer_registro(FD_CATEGORIAS, pos)
        print("\nCategoría " + str(cat.nro_categoria) + " - " + recortar(cat.nombre_categoria))
        print("Pregunta: " + recortar(cat.pregunta))
        if mostrar_opciones(cat.nro_categoria) == 0:
            print("   La categoría no tiene opciones cargadas.")
    input("\nPresione Enter para continuar...")

def administrar_opciones():
    opc_opciones = " "
    while opc_opciones != "3":
        os.system("cls")
        print("........\033[93m\033[4mADMINISTRAR OPCIONES\033[0m........ ")
        print("1- Alta")
        print("2- Consulta")
        print("3- Volver")

        opc_opciones = recortar(input("Ingrese su opción: "))
        while opc_opciones != "1" and opc_opciones != "2" and opc_opciones != "3":
            opc_opciones = recortar(input("Ingreso inválido - reintente: "))

        match opc_opciones:
            case "1":
                alta_opciones()
            case "2":
                consulta_opciones()

def administracion_juegos():
    os.system("cls")
    print("........\033[93m\033[4mADMINISTRACIÓN DE JUEGOS\033[0m........\n")
    if ingresar_clave_admin():
        opc_admin = " "
        while opc_admin != "3":
            os.system("cls")
            print("........\033[93m\033[4mADMINISTRACIÓN DE JUEGOS\033[0m........ ")
            print("1- Administrar Categorías")
            print("2- Administrar Opciones")
            print("3- Volver")

            opc_admin = recortar(input("Ingrese su opción: "))
            while opc_admin != "1" and opc_admin != "2" and opc_admin != "3":
                opc_admin = recortar(input("Ingreso inválido - reintente: "))

            match opc_admin:
                case "1":
                    administrar_categorias()
                case "2":
                    administrar_opciones()


"""
Declarativa de funciones del menú principal
"""
def cartel_inicial():
    os.system("cls")
    print("+------------------------------------------------------------+")
    print("|                                                            |")
    print("|  JUEGOS DE APUESTA PROHIBIDOS PARA MENORES DE EDAD         |")
    print("|                                                            |")
    print("|     EL JUEGO PUEDE SER PERJUDICIAL PARA LA SALUD           |")
    print("|                                                            |")
    print("+------------------------------------------------------------+")
    input("\nPresione Enter para continuar...")

def salir():
    os.system("cls")
    input("Gracias por jugar, no apueste, juega por diversión")

def menu():
    os.system("cls")
    print("........\033[4m\033[92mMENÚ DE OPCIONES\033[0m ")
    print("a- \033[96m↑ Juego del menor-mayor ↓\033[0m ")
    print("b- \033[1m\033[91mAdivinar el número secreto [?]\033[0m ")
    print("c- \033[94m♦ Blackjack ♦\033[0m ")
    print("d- \033[95m[1] Par o impar [6]\033[0m ")
    print("e- \033[93mReporte\033[0m ")
    print("f- \033[93mAdministración de Juegos\033[0m ")
    print("g- \033[97mSalir del programa\033[0m ")


"""
Programa principal
CLAVE_ADMIN : str (constante, contraseña de administrador)
opc : str
"""
CLAVE_ADMIN = "admin2026"

# Si todavía no existen los archivos de categorías y opciones, se crean con datos de ejemplo
if not os.path.exists(FD_CATEGORIAS) and not os.path.exists(FD_OPCIONES):
    crear_datos_iniciales()

cartel_inicial()

opc = " "
while opc != "g":
    menu()
    opc = recortar(input("Ingrese su opción: ")).lower()

    while len(opc) != 1 or opc < "a" or opc > "g":
        menu()
        opc = recortar(input("Ingreso inválido - reintente: ")).lower()

    match opc:
        case "a": juego_mayor_menor()
        case "b": juego_numero_secreto()
        case "c": juego_blackjack()
        case "d": juego_par_impar()
        case "e": reporte()
        case "f": administracion_juegos()
        case "g": salir()
