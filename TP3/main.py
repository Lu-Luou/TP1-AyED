'''
Proyecto realizado por Joaquín del Castillo, Thiago Finoli, Guido Pacienzia y Lucas Ruberto
Comisión 1k05
Trabajo Práctico Nro. 3 - Suite de Juegos "Azar y Lógica" con registros y archivos
'''

import random, os, pickle, getpass

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
CARPETA : str (carpeta donde está este programa; en la entrega es c:\\tp3\\)
FD_CATEGORIAS, FD_OPCIONES, FD_JUGADORES : str (nombre físico de cada archivo)
LARGO_NOMBRE, LARGO_NOMBRE_CATEGORIA, LARGO_PREGUNTA, LARGO_OBJETO : int
CREDITO_INICIAL : float
FILA_GANADAS, FILA_PERDIDAS : int (filas de la matriz juegos)
JUEGO_MAYOR_MENOR, JUEGO_NUMERO_SECRETO, JUEGO_BLACKJACK, JUEGO_PAR_IMPAR, CANT_JUEGOS : int (columnas de la matriz juegos)
"""
CARPETA = os.path.dirname(os.path.abspath(__file__)) + os.sep
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
cadena, resultado, mensaje, dato, respuesta, opcion1, opcion2, primera, ultima, opc, nombre, titulo, color, texto1, texto2 : str
largo, i, inicio, fin, cant_puntos, cant_digitos, minimo, maximo : int
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

def encabezado(titulo, color):
    # Limpia la pantalla y muestra el título subrayado con el color ANSI indicado
    os.system("cls")
    print("\033[4m\033[" + color + "m" + titulo + "\033[0m\n")

def pausa():
    input("\nPresione Enter para continuar...")

def cartel(texto1, texto2):
    # Recuadro grande dibujado con caracteres, con dos líneas de texto
    print("+------------------------------------------------------------+")
    print("|                                                            |")
    print("|  " + ajustar_cadena(texto1, 58) + "|")
    print("|                                                            |")
    print("|  " + ajustar_cadena(texto2, 58) + "|")
    print("|                                                            |")
    print("+------------------------------------------------------------+")

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

def pedir_entero_rango(mensaje, minimo, maximo):
    dato = recortar(input(mensaje))
    while not dato.isdigit() or int(dato) < minimo or int(dato) > maximo:
        print("Error: debe ingresar un número entero entre " + str(minimo) + " y " + str(maximo) + ".")
        dato = recortar(input(mensaje))
    return int(dato)

def pedir_entre_dos(mensaje, opcion1, opcion2):
    # Devuelve la respuesta en minúsculas; sólo acepta opcion1 u opcion2 (sin distinguir mayúsculas)
    respuesta = recortar(input(mensaje)).lower()
    while respuesta != opcion1 and respuesta != opcion2:
        print("Opción inválida: ingrese " + opcion1 + " o " + opcion2 + ".")
        respuesta = recortar(input(mensaje)).lower()
    return respuesta

def pedir_si_no(mensaje):
    return pedir_entre_dos(mensaje + " (S/N): ", "s", "n") == "s"

def pedir_opcion(primera, ultima):
    # Opción de un menú: un único carácter entre 'primera' y 'ultima'
    opc = recortar(input("Ingrese su opción: ")).lower()
    while len(opc) != 1 or opc < primera or opc > ultima:
        opc = recortar(input("Ingreso inválido - reintente: ")).lower()
    return opc

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
CANT_RONDAS, MIN_ACIERTOS, MIN_OPCIONES_CATEGORIA, MAX_OPCIONES_CATEGORIA : int (constantes)
posiciones : array de int, tamaño MAX_OPCIONES_CATEGORIA (posición en el archivo de cada opción
             de la categoría elegida; -1 = opción ya sorteada en la partida)
pos, pos_actual, tam, cantidad, casillero, correctas, ronda, eleccion, nro_categoria : int
apuesta : float
continuar : bool
jug : Jugador
cat : Categoria
op, op1, op2 : Opcion
"""
CANT_RONDAS = 6
MIN_ACIERTOS = 4
MIN_OPCIONES_CATEGORIA = CANT_RONDAS + 1     # 2 opciones en la primera ronda y una nueva en cada una de las siguientes
MAX_OPCIONES_CATEGORIA = 100

def cargar_opciones(nro_categoria, posiciones):
    # Guarda en 'posiciones' dónde empieza cada opción de la categoría y devuelve cuántas guardó
    cantidad = 0
    archivo = open(FD_OPCIONES, "rb")
    tam = os.path.getsize(FD_OPCIONES)
    while archivo.tell() < tam and cantidad < MAX_OPCIONES_CATEGORIA:
        pos_actual = archivo.tell()
        op = pickle.load(archivo)
        if op.nro_categoria == nro_categoria:
            posiciones[cantidad] = pos_actual
            cantidad = cantidad + 1
    archivo.close()
    return cantidad

def sortear_opcion(posiciones, cantidad):
    # Sortea una opción que todavía no salió en la partida y la marca con -1
    casillero = random.randint(0, cantidad - 1)
    while posiciones[casillero] == -1:
        casillero = random.randint(0, cantidad - 1)
    op = leer_registro(FD_OPCIONES, posiciones[casillero])
    posiciones[casillero] = -1
    return op

def jugar_partida_mayor_menor(cat):
    # Juega las rondas con la categoría elegida y devuelve la cantidad de aciertos
    posiciones = [-1] * MAX_OPCIONES_CATEGORIA
    cantidad = cargar_opciones(cat.nro_categoria, posiciones)
    op1 = sortear_opcion(posiciones, cantidad)
    op2 = sortear_opcion(posiciones, cantidad)
    correctas = 0
    for ronda in range(1, CANT_RONDAS + 1):
        print("\nRonda " + str(ronda) + " de " + str(CANT_RONDAS) + " - " + recortar(cat.nombre_categoria))
        print(recortar(cat.pregunta))
        eleccion = pedir_entero_rango("1- " + recortar(op1.objeto) + "  /  2- " + recortar(op2.objeto) + ": ", 1, 2)
        print("1- " + recortar(op1.objeto) + " " + str(op1.valor) + "  /  2- " + recortar(op2.objeto) + " " + str(op2.valor))
        if (eleccion == 1 and op1.valor >= op2.valor) or (eleccion == 2 and op2.valor >= op1.valor):
            print("¡La respuesta es correcta!")
            correctas = correctas + 1
        else:
            print("Ups... la respuesta es incorrecta.")
        if ronda < CANT_RONDAS:
            input("Presione Enter para continuar...")
            # La opción correcta (la de mayor valor) sigue en la ronda siguiente
            if op1.valor >= op2.valor:
                op2 = sortear_opcion(posiciones, cantidad)
            else:
                op1 = sortear_opcion(posiciones, cantidad)
    return correctas

def juego_mayor_menor():
    encabezado("MAYOR O MENOR", "96")
    pos = identificar_jugador()
    jug = leer_registro(FD_JUGADORES, pos)
    continuar = True
    while jug.creditos > 0 and continuar:
        print("\nSaldo actual: " + formato_creditos(jug.creditos))
        apuesta = pedir_apuesta(jug.creditos)
        print("\nCategorías:")
        if mostrar_categorias(True) == 0:
            print("No hay categorías activas. Un administrador debe dar de alta alguna.")
            continuar = False
        else:
            cat = leer_registro(FD_CATEGORIAS, pedir_categoria(True))
            if contar_opciones(cat.nro_categoria) < MIN_OPCIONES_CATEGORIA:
                print("Esa categoría tiene menos de " + str(MIN_OPCIONES_CATEGORIA) + " opciones y no se puede jugar.")
                print("Un administrador debe agregar más opciones.")
                continuar = False
            else:
                correctas = jugar_partida_mayor_menor(cat)
                print("\nAciertos: " + str(correctas) + " de " + str(CANT_RONDAS))
                if correctas >= MIN_ACIERTOS:
                    print("\033[92m¡Felicidades! Ganó " + formato_creditos(apuesta) + ".\033[0m")
                    registrar_resultado(pos, JUEGO_MAYOR_MENOR, True, apuesta)
                else:
                    print("\033[91mOh, no... Perdió " + formato_creditos(apuesta) + ".\033[0m")
                    registrar_resultado(pos, JUEGO_MAYOR_MENOR, False, -apuesta)
                jug = leer_registro(FD_JUGADORES, pos)
                print("Saldo actual: " + formato_creditos(jug.creditos))
                if jug.creditos > 0:
                    continuar = pedir_si_no("\n¿Desea volver a jugar?")
    if jug.creditos <= 0:
        print("No tiene más créditos en su saldo.")
    pausa()


"""
Declarativa de funciones y variables juego 2: Número Secreto
MAX_INTENTOS, MIN_SECRETO, MAX_SECRETO : int (constantes)
pos, numero_secreto, numero, intentos : int
adivino : bool
"""
MAX_INTENTOS = 5
MIN_SECRETO = 1
MAX_SECRETO = 100

def juego_numero_secreto():
    encabezado("NÚMERO SECRETO", "91")
    pos = identificar_jugador()
    numero_secreto = random.randint(MIN_SECRETO, MAX_SECRETO)
    intentos = 0
    adivino = False
    while intentos < MAX_INTENTOS and not adivino:
        print("\nLe quedan " + str(MAX_INTENTOS - intentos) + " intentos.")
        numero = pedir_entero_rango("Ingrese un número entre " + str(MIN_SECRETO) + " y " + str(MAX_SECRETO) + ": ", MIN_SECRETO, MAX_SECRETO)
        intentos = intentos + 1
        if numero == numero_secreto:
            adivino = True
        elif numero > numero_secreto:
            print("El número secreto es menor.")
        else:
            print("El número secreto es mayor.")
    if adivino:
        print("\n\033[92m¡Enhorabuena! Adivinaste el número " + str(numero_secreto) + " en " + str(intentos) + " intentos.\033[0m")
    else:
        print("\n\033[91mOh no, perdiste el juego. El número secreto era " + str(numero_secreto) + ".\033[0m")
    registrar_resultado(pos, JUEGO_NUMERO_SECRETO, adivino, 0)
    pausa()


"""
Declarativa de funciones y variables juego 3: Blackjack
CANT_CARTAS_MAZO, CANT_VALORES, MAX_CARTAS_MANO : int (constantes)
PALOS : str (constante, un símbolo por palo)
nombre, titular, texto_cartas, accion : str
pos, carta, valor, palo, total, cant_ases, puntos_jugador, puntos_banca, resultado, i : int
cant_cartas, cant_cartas_jugador, cant_cartas_banca : int
jugando, otra : bool
mazo : array de bool, tamaño CANT_CARTAS_MAZO (True = carta ya repartida)
mano, mano_jugador, mano_banca : array de int, tamaño MAX_CARTAS_MANO
Cada carta es un número de 0 a 51: carta % 13 es su valor (0 = "2" ... 12 = "A") y carta // 13 su palo.
"""
CANT_CARTAS_MAZO = 52
CANT_VALORES = 13
MAX_CARTAS_MANO = 12
PALOS = "♠♥♦♣"

def repartir_carta(mazo):
    # Un solo mazo: se sortea hasta encontrar una carta que no se haya repartido
    carta = random.randint(0, CANT_CARTAS_MAZO - 1)
    while mazo[carta]:
        carta = random.randint(0, CANT_CARTAS_MAZO - 1)
    mazo[carta] = True
    return carta

def agregar_carta(mano, cant_cartas, mazo):
    # Agrega a la mano una carta del mazo y devuelve la nueva cantidad de cartas
    mano[cant_cartas] = repartir_carta(mazo)
    return cant_cartas + 1

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
    cant_cartas_jugador = 0
    cant_cartas_banca = 0
    for i in range(2):
        cant_cartas_jugador = agregar_carta(mano_jugador, cant_cartas_jugador, mazo)
        cant_cartas_banca = agregar_carta(mano_banca, cant_cartas_banca, mazo)
    puntos_jugador = calcular_puntos(mano_jugador, cant_cartas_jugador)
    puntos_banca = calcular_puntos(mano_banca, cant_cartas_banca)

    print("Banca: " + nombre_carta(mano_banca[0]) + " [carta oculta]")
    mostrar_mano(nombre, mano_jugador, cant_cartas_jugador)

    # Turno del jugador: pide cartas hasta plantarse, llegar a 21 o pasarse
    jugando = puntos_jugador < 21
    while jugando:
        accion = pedir_entre_dos("\n¿Desea Pedir otra carta o Plantarse?: ", "pedir", "plantarse")
        if accion == "pedir":
            cant_cartas_jugador = agregar_carta(mano_jugador, cant_cartas_jugador, mazo)
            puntos_jugador = calcular_puntos(mano_jugador, cant_cartas_jugador)
            mostrar_mano(nombre, mano_jugador, cant_cartas_jugador)
            jugando = puntos_jugador < 21
        else:
            jugando = False

    if puntos_jugador > 21:
        print("\n\033[91mTe pasaste de 21 con " + str(puntos_jugador) + " puntos. ¡Perdiste!\033[0m")
        resultado = -1
    else:
        # Turno de la banca: pide con 16 o menos y se planta con 17 o más
        if puntos_jugador == 21:
            print("\n¡Llegaste a 21!")
        print("\nTurno de la Banca:")
        mostrar_mano("Banca", mano_banca, cant_cartas_banca)
        while puntos_banca < 17:
            cant_cartas_banca = agregar_carta(mano_banca, cant_cartas_banca, mazo)
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
    encabezado("BLACKJACK", "94")
    pos = identificar_jugador()
    nombre = recortar(leer_registro(FD_JUGADORES, pos).nombre)
    otra = True
    while otra:
        print()
        resultado = jugar_partida_blackjack(nombre)
        # El empate no cuenta como partida ganada ni perdida
        if resultado != 0:
            registrar_resultado(pos, JUEGO_BLACKJACK, resultado == 1, 0)
        otra = pedir_si_no("\n¿Desea jugar otra partida?")
        if otra:
            encabezado("BLACKJACK", "94")


"""
Declarativa de funciones y variables juego 4: Par o Impar
eleccion, paridad : str
pos, dado1, dado2, suma : int
apuesta : float
continuar : bool
jug : Jugador
"""
def juego_par_impar():
    encabezado("PAR O IMPAR", "95")
    pos = identificar_jugador()
    jug = leer_registro(FD_JUGADORES, pos)
    continuar = True
    while jug.creditos > 0 and continuar:
        print("\nSaldo actual: " + formato_creditos(jug.creditos))
        apuesta = pedir_apuesta(jug.creditos)
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        suma = dado1 + dado2
        eleccion = pedir_entre_dos("Se tiraron dos dados. ¿La suma es Par o Impar?: ", "par", "impar")
        if suma % 2 == 0:
            paridad = "par"
        else:
            paridad = "impar"

        print("\nSalieron " + str(dado1) + " y " + str(dado2) + ": la suma es " + str(suma) + ", un número " + paridad + ".")
        if eleccion == paridad:
            print("\033[92m¡Ganaste! Tu apuesta de " + formato_creditos(apuesta) + " se suma a tus créditos.\033[0m")
            registrar_resultado(pos, JUEGO_PAR_IMPAR, True, apuesta)
        else:
            print("\033[91mPerdiste... Tu apuesta de " + formato_creditos(apuesta) + " se resta de tus créditos.\033[0m")
            registrar_resultado(pos, JUEGO_PAR_IMPAR, False, -apuesta)
        jug = leer_registro(FD_JUGADORES, pos)
        print("Saldo actual: " + formato_creditos(jug.creditos))
        if jug.creditos > 0:
            continuar = pedir_si_no("\n¿Desea volver a jugar?")
    if jug.creditos <= 0:
        print("No tiene más créditos para jugar.")
    pausa()


"""
Declarativa de funciones y variables del Reporte
opc, nombre, nombre_buscado : str
pos, cantidad, juego, ganadas, perdidas, i, j : int
jugo_algo : bool
jugadores : array de Jugador, tamaño cantidad
jug, aux : Jugador
"""
def nombre_juego(juego):
    match juego:
        case 0:
            nombre = "\033[96mMayor o Menor\033[0m"
        case 1:
            nombre = "\033[91mNúmero Secreto\033[0m"
        case 2:
            nombre = "\033[94mBlackjack\033[0m"
        case _:
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
    encabezado("JUGADORES POR CANTIDAD DE CRÉDITOS", "93")
    cantidad = contar_registros(FD_JUGADORES)
    if cantidad == 0:
        print("Todavía no hay jugadores registrados.")
    else:
        jugadores = cargar_jugadores(cantidad)
        ordenar_por_creditos_descendente(jugadores, cantidad)
        for i in range(cantidad):
            print("   " + str(i + 1) + ". " + jugadores[i].nombre + " " + formato_creditos(jugadores[i].creditos))
    pausa()

def reporte_juegos_de_jugador():
    encabezado("JUEGOS JUGADOS POR UN JUGADOR", "93")
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
    pausa()

def reporte():
    opc = " "
    while opc != "c":
        encabezado("REPORTE", "93")
        print("a- Lista de jugadores ordenados de mayor a menor por créditos")
        print("b- Juegos jugados por un jugador")
        print("c- Volver al menú principal")
        opc = pedir_opcion("a", "c")
        match opc:
            case "a":
                reporte_jugadores_por_creditos()
            case "b":
                reporte_juegos_de_jugador()


"""
Declarativa de funciones y variables de Administración de Juegos
MAX_INTENTOS_CLAVE : int (constante)
clave, nombre, pregunta, objeto, opc : str
intentos, pos, nro_categoria, cantidad, valor : int
acceso, otra : bool
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
        pausa()
    return acceso

def alta_categoria():
    encabezado("ALTA DE CATEGORÍA", "93")
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
    pausa()

def modificacion_categoria():
    encabezado("MODIFICACIÓN DE CATEGORÍA", "93")
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
    pausa()

def baja_categoria():
    encabezado("BAJA DE CATEGORÍA", "93")
    if mostrar_categorias(True) == 0:
        print("No hay categorías activas para dar de baja.")
    else:
        print()
        pos = pedir_categoria(True)
        cat = leer_registro(FD_CATEGORIAS, pos)
        if pedir_si_no("¿Confirma la baja de la categoría \"" + recortar(cat.nombre_categoria) + "\"?"):
            cat.estado = "I"
            modificar_registro(FD_CATEGORIAS, pos, cat)
            print("La categoría " + str(cat.nro_categoria) + " quedó Inactiva.")
        else:
            print("Baja cancelada.")
    pausa()

def administrar_categorias():
    opc = " "
    while opc != "4":
        encabezado("ADMINISTRAR CATEGORÍAS", "93")
        print("1- Alta")
        print("2- Modificación")
        print("3- Baja")
        print("4- Volver")
        opc = pedir_opcion("1", "4")
        match opc:
            case "1":
                alta_categoria()
            case "2":
                modificacion_categoria()
            case "3":
                baja_categoria()

def alta_opciones():
    encabezado("ALTA DE OPCIONES", "93")
    if mostrar_categorias(True) == 0:
        print("No hay categorías activas. Antes de registrar opciones se deben dar de alta categorías.")
    else:
        print()
        cat = leer_registro(FD_CATEGORIAS, pedir_categoria(True))
        nro_categoria = cat.nro_categoria
        print("\nCategoría: " + recortar(cat.nombre_categoria))
        print("Pregunta: " + recortar(cat.pregunta))

        otra = True
        while otra:
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
    pausa()

def consulta_opciones():
    encabezado("CONSULTA DE OPCIONES", "93")
    if mostrar_categorias(False) == 0:
        print("No hay categorías registradas.")
    else:
        print()
        cat = leer_registro(FD_CATEGORIAS, pedir_categoria(False))
        print("\nCategoría " + str(cat.nro_categoria) + " - " + recortar(cat.nombre_categoria))
        print("Pregunta: " + recortar(cat.pregunta))
        if mostrar_opciones(cat.nro_categoria) == 0:
            print("   La categoría no tiene opciones cargadas.")
    pausa()

def administrar_opciones():
    opc = " "
    while opc != "3":
        encabezado("ADMINISTRAR OPCIONES", "93")
        print("1- Alta")
        print("2- Consulta")
        print("3- Volver")
        opc = pedir_opcion("1", "3")
        match opc:
            case "1":
                alta_opciones()
            case "2":
                consulta_opciones()

def administracion_juegos():
    encabezado("ADMINISTRACIÓN DE JUEGOS", "93")
    if ingresar_clave_admin():
        opc = " "
        while opc != "3":
            encabezado("ADMINISTRACIÓN DE JUEGOS", "93")
            print("1- Administrar Categorías")
            print("2- Administrar Opciones")
            print("3- Volver")
            opc = pedir_opcion("1", "3")
            match opc:
                case "1":
                    administrar_categorias()
                case "2":
                    administrar_opciones()


"""
Declarativa de funciones y variables del menú principal
CLAVE_ADMIN : str (constante, contraseña de administrador)
opc : str
"""
CLAVE_ADMIN = "admin2026"

def menu():
    encabezado("MENÚ DE OPCIONES", "92")
    print("a- \033[96m↑ Juego del menor-mayor ↓\033[0m")
    print("b- \033[91mAdivinar el número secreto [?]\033[0m")
    print("c- \033[94m♦ Blackjack ♦\033[0m")
    print("d- \033[95m[1] Par o impar [6]\033[0m")
    print("e- \033[93mReporte\033[0m")
    print("f- \033[93mAdministración de Juegos\033[0m")
    print("g- Salir del programa")

def principal():
    # Si todavía no existen los archivos de categorías y opciones, se crean con datos de ejemplo
    if not os.path.exists(FD_CATEGORIAS) and not os.path.exists(FD_OPCIONES):
        crear_datos_iniciales()

    os.system("cls")
    cartel("JUEGOS DE APUESTA PROHIBIDOS PARA MENORES DE EDAD", "EL JUEGO PUEDE SER PERJUDICIAL PARA LA SALUD")
    pausa()

    opc = " "
    while opc != "g":
        menu()
        opc = pedir_opcion("a", "g")
        match opc:
            case "a":
                juego_mayor_menor()
            case "b":
                juego_numero_secreto()
            case "c":
                juego_blackjack()
            case "d":
                juego_par_impar()
            case "e":
                reporte()
            case "f":
                administracion_juegos()

    os.system("cls")
    cartel("Gracias por jugar, no apueste, juega por diversión", " ")
    input("\nPresione Enter para salir...")


"""
Programa principal
(sólo se ejecuta al correr main.py, no cuando los tests importan sus funciones)
"""
if __name__ == "__main__":
    principal()
