'''
Tests del TP3. Se ejecutan desde la carpeta tp3 con:  python -m unittest -v
Cada test trabaja con archivos .dat en una carpeta temporal, así no se tocan los datos reales.
'''

import ast, io, os, pickle, shutil, subprocess, sys, tempfile, unittest
from contextlib import redirect_stdout
from unittest import mock

import main

CARPETA_TP3 = os.path.dirname(os.path.abspath(__file__))


def carta(valor, palo=0):
    # Arma el número de carta que usa main: "2".."10" -> 0..8, J=9, Q=10, K=11, A=12
    figuras = {"J": 9, "Q": 10, "K": 11, "A": 12}
    if valor in figuras:
        indice = figuras[valor]
    else:
        indice = int(valor) - 2
    return palo * main.CANT_VALORES + indice


def leer_todos(fd):
    registros = []
    with open(fd, "rb") as archivo:
        tam = os.path.getsize(fd)
        while archivo.tell() < tam:
            registros.append(pickle.load(archivo))
    return registros


class BaseTest(unittest.TestCase):
    # Redirige los archivos a una carpeta temporal y anula el "cls"

    def setUp(self):
        self.carpeta = tempfile.mkdtemp()
        rutas = {
            "FD_CATEGORIAS": os.path.join(self.carpeta, "categorias.dat"),
            "FD_OPCIONES": os.path.join(self.carpeta, "opciones.dat"),
            "FD_JUGADORES": os.path.join(self.carpeta, "jugadores.dat"),
        }
        for nombre, ruta in rutas.items():
            parche = mock.patch.object(main, nombre, ruta)
            parche.start()
            self.addCleanup(parche.stop)
        parche = mock.patch.object(main.os, "system")
        parche.start()
        self.addCleanup(parche.stop)
        self.addCleanup(shutil.rmtree, self.carpeta, True)

    def ejecutar(self, funcion, entradas, *args):
        # Ejecuta la función respondiendo cada input() con las entradas dadas (lista o función)
        if callable(entradas):
            efecto = entradas
        else:
            efecto = list(entradas)
        salida = io.StringIO()
        with mock.patch("builtins.input", side_effect=efecto), redirect_stdout(salida):
            resultado = funcion(*args)
        self.salida = salida.getvalue()
        return resultado

    def jugador(self, nombre):
        return main.leer_registro(main.FD_JUGADORES, main.buscar_jugador(nombre))

    def crear_categoria(self, nro, nombre, valores, estado="A"):
        cat = main.Categoria()
        cat.nro_categoria = nro
        cat.nombre_categoria = main.ajustar_cadena(nombre, main.LARGO_NOMBRE_CATEGORIA)
        cat.pregunta = main.ajustar_cadena("¿Cuál es mayor?", main.LARGO_PREGUNTA)
        cat.estado = estado
        main.agregar_registro(main.FD_CATEGORIAS, cat)
        for i in range(len(valores)):
            op = main.Opcion()
            op.nro_categoria = nro
            op.nro_opcion = i + 1
            op.objeto = main.ajustar_cadena("Objeto " + str(nro) + "-" + str(i + 1), main.LARGO_OBJETO)
            op.valor = valores[i]
            main.agregar_registro(main.FD_OPCIONES, op)


class TestUtilidades(unittest.TestCase):

    def test_ajustar_cadena_completa_y_recorta(self):
        self.assertEqual(main.ajustar_cadena("ab", 5), "ab   ")
        self.assertEqual(main.ajustar_cadena("abcdef", 3), "abc")

    def test_recortar(self):
        self.assertEqual(main.recortar("   hola mundo  "), "hola mundo")
        self.assertEqual(main.recortar("    "), "")

    def test_es_real(self):
        for valido in ("10", "10.5", ".5", "100."):
            self.assertTrue(main.es_real(valido), valido)
        for invalido in ("", ".", "1.2.3", "-5", "abc", "1,5"):
            self.assertFalse(main.es_real(invalido), invalido)

    def test_validar_nombre(self):
        self.assertTrue(main.validar_nombre("Lucas"))
        self.assertFalse(main.validar_nombre(""))
        self.assertFalse(main.validar_nombre("Lucas2"))
        self.assertFalse(main.validar_nombre("x" * 31))


class TestArchivos(BaseTest):

    def test_agregar_y_leer_por_posicion(self):
        pos1 = main.alta_jugador("Ana")
        pos2 = main.alta_jugador("Beto")
        self.assertEqual(pos1, 0)
        self.assertEqual(main.recortar(main.leer_registro(main.FD_JUGADORES, pos2).nombre), "Beto")
        self.assertEqual(main.contar_registros(main.FD_JUGADORES), 2)

    def test_modificar_registro_que_cambia_de_tamano_no_pisa_al_siguiente(self):
        pos1 = main.alta_jugador("Ana")
        main.alta_jugador("Beto")
        jug = main.leer_registro(main.FD_JUGADORES, pos1)
        jug.juegos[0][0] = 70000            # pickle lo guarda con más bytes que un 0
        jug.creditos = 123.45
        main.modificar_registro(main.FD_JUGADORES, pos1, jug)
        registros = leer_todos(main.FD_JUGADORES)
        self.assertEqual(len(registros), 2)
        self.assertEqual(registros[0].juegos[0][0], 70000)
        self.assertEqual(main.recortar(registros[1].nombre), "Beto")


class TestJugadores(BaseTest):

    def test_jugador_nuevo_arranca_con_10000(self):
        self.ejecutar(main.identificar_jugador, ["Ana"])
        jug = self.jugador("Ana")
        self.assertEqual(jug.creditos, 10000.0)
        self.assertEqual(jug.juegos, [[0, 0, 0, 0], [0, 0, 0, 0]])

    def test_jugador_existente_no_se_duplica(self):
        pos1 = self.ejecutar(main.identificar_jugador, ["Ana"])
        pos2 = self.ejecutar(main.identificar_jugador, ["  Ana  "])
        self.assertEqual(pos1, pos2)
        self.assertEqual(main.contar_registros(main.FD_JUGADORES), 1)

    def test_nombre_invalido_se_vuelve_a_pedir(self):
        self.ejecutar(main.identificar_jugador, ["", "Ana1", "Ana"])
        self.assertIn("no puede estar vacío", self.salida)
        self.assertNotEqual(main.buscar_jugador("Ana"), -1)

    def test_registrar_resultado(self):
        pos = main.alta_jugador("Ana")
        main.registrar_resultado(pos, main.JUEGO_PAR_IMPAR, True, 500)
        main.registrar_resultado(pos, main.JUEGO_PAR_IMPAR, False, -200)
        main.registrar_resultado(pos, main.JUEGO_BLACKJACK, True, 0)
        jug = self.jugador("Ana")
        self.assertEqual(jug.creditos, 10300.0)
        self.assertEqual(jug.juegos[main.FILA_GANADAS], [0, 0, 1, 1])
        self.assertEqual(jug.juegos[main.FILA_PERDIDAS], [0, 0, 0, 1])


class TestDatosIniciales(BaseTest):
    # La consigna pide al menos 3 categorías y 10 opciones por categoría

    def verificar_datos(self, categorias, opciones):
        self.assertGreaterEqual(len(categorias), 3)
        for i in range(len(categorias)):
            cat = categorias[i]
            self.assertEqual(cat.nro_categoria, i + 1)          # consecutivo desde 1
            self.assertEqual(cat.estado, "A")
            self.assertLessEqual(len(cat.nombre_categoria), main.LARGO_NOMBRE_CATEGORIA)
            propias = [op for op in opciones if op.nro_categoria == cat.nro_categoria]
            self.assertGreaterEqual(len(propias), 10, main.recortar(cat.nombre_categoria))
            self.assertEqual([op.nro_opcion for op in propias], list(range(1, len(propias) + 1)))
            objetos = [main.recortar(op.objeto).lower() for op in propias]
            self.assertEqual(len(objetos), len(set(objetos)), "objetos repetidos")

    def test_crear_datos_iniciales(self):
        main.crear_datos_iniciales()
        self.verificar_datos(leer_todos(main.FD_CATEGORIAS), leer_todos(main.FD_OPCIONES))

    def test_archivos_entregados(self):
        # Los .dat de la entrega se grabaron corriendo main.py, por eso sus clases figuran en __main__
        class Lector(pickle.Unpickler):
            def find_class(self, modulo, nombre):
                if modulo == "__main__":
                    modulo = "main"
                return super().find_class(modulo, nombre)

        def cargar(nombre_archivo):
            registros = []
            ruta = os.path.join(CARPETA_TP3, nombre_archivo)
            with open(ruta, "rb") as archivo:
                while archivo.tell() < os.path.getsize(ruta):
                    registros.append(Lector(archivo).load())
            return registros

        self.verificar_datos(cargar("categorias.dat"), cargar("opciones.dat"))


class TestMayorMenor(BaseTest):

    def setUp(self):
        super().setUp()
        self.crear_categoria(1, "Numeros", [10, 20, 30, 40, 50, 60, 70, 80])
        self.crear_categoria(2, "Corta", [1, 2, 3])
        self.crear_categoria(3, "Dada de baja", [1, 2, 3, 4, 5, 6, 7, 8], "I")

    def responder(self, acertar):
        # Lee las dos opciones del mensaje "1- X  /  2- Y: " y elige la de mayor (o menor) valor
        valores = {}
        for op in leer_todos(main.FD_OPCIONES):
            valores[main.recortar(op.objeto)] = op.valor

        def entrada(mensaje):
            respuesta = ""
            if mensaje.startswith("1- "):
                izq, der = mensaje[3:-2].split("  /  2- ")
                if (valores[izq] > valores[der]) == acertar:
                    respuesta = "1"
                else:
                    respuesta = "2"
            return respuesta
        return entrada

    def test_sorteo_sin_repetir(self):
        posiciones = [-1] * main.MAX_OPCIONES_CATEGORIA
        cantidad = main.cargar_opciones(1, posiciones)
        self.assertEqual(cantidad, 8)
        sorteadas = [main.sortear_opcion(posiciones, cantidad).nro_opcion for i in range(cantidad)]
        self.assertEqual(sorted(sorteadas), list(range(1, 9)))

    def test_partida_perfecta_y_la_correcta_sigue(self):
        cat = main.leer_registro(main.FD_CATEGORIAS, 0)
        correctas = self.ejecutar(main.jugar_partida_mayor_menor, self.responder(True), cat)
        self.assertEqual(correctas, main.CANT_RONDAS)
        self.assertEqual(self.salida.count("Ronda "), 6)

    def test_partida_toda_mal(self):
        cat = main.leer_registro(main.FD_CATEGORIAS, 0)
        self.assertEqual(self.ejecutar(main.jugar_partida_mayor_menor, self.responder(False), cat), 0)

    def test_juego_ganado_suma_la_apuesta(self):
        entradas = self.responder(True)
        guion = iter(["Ana", "500", "1"])

        def entrada(mensaje):
            respuesta = entradas(mensaje)
            if "¿Desea volver" in mensaje:
                respuesta = "n"
            elif not mensaje.startswith("1- ") and "Presione" not in mensaje:
                respuesta = next(guion)
            return respuesta

        self.ejecutar(main.juego_mayor_menor, entrada)
        jug = self.jugador("Ana")
        self.assertEqual(jug.creditos, 10500.0)
        self.assertEqual(jug.juegos[main.FILA_GANADAS][main.JUEGO_MAYOR_MENOR], 1)

    def test_categoria_inactiva_no_se_puede_elegir_y_corta_no_se_juega(self):
        self.ejecutar(main.juego_mayor_menor, ["Ana", "500", "3", "9", "2", ""])
        self.assertIn("está inactiva", self.salida)
        self.assertIn("no existe una categoría", self.salida)
        self.assertIn("menos de 7 opciones", self.salida)
        self.assertNotIn("Dada de baja", self.salida)
        self.assertEqual(self.jugador("Ana").creditos, 10000.0)


class TestNumeroSecreto(BaseTest):

    def test_adivina_en_el_segundo_intento(self):
        with mock.patch.object(main.random, "randint", return_value=42):
            self.ejecutar(main.juego_numero_secreto, ["Ana", "abc", "0", "101", "50", "42", ""])
        self.assertIn("El número secreto es menor", self.salida)
        self.assertIn("en 2 intentos", self.salida)
        self.assertIn("Le quedan 4 intentos", self.salida)
        self.assertEqual(self.jugador("Ana").juegos[main.FILA_GANADAS][main.JUEGO_NUMERO_SECRETO], 1)

    def test_pierde_tras_cinco_intentos(self):
        with mock.patch.object(main.random, "randint", return_value=42):
            self.ejecutar(main.juego_numero_secreto, ["Ana", "1", "2", "3", "4", "5", ""])
        self.assertIn("El número secreto era 42", self.salida)
        self.assertEqual(self.salida.count("El número secreto es mayor"), 5)
        self.assertEqual(self.jugador("Ana").juegos[main.FILA_PERDIDAS][main.JUEGO_NUMERO_SECRETO], 1)


class TestBlackjack(BaseTest):

    def test_calcular_puntos(self):
        casos = [
            (["A", "K"], 21),
            (["A", "A", "9"], 21),
            (["A", "A", "A"], 13),
            (["K", "Q", "5"], 25),
            (["A", "5", "K"], 16),
            (["2", "10"], 12),
        ]
        for cartas, esperado in casos:
            mano = [carta(c) for c in cartas]
            self.assertEqual(main.calcular_puntos(mano, len(mano)), esperado, cartas)

    def test_nombre_carta(self):
        self.assertEqual(main.nombre_carta(carta("10", 1)), "10♥")
        self.assertEqual(main.nombre_carta(carta("A", 3)), "A♣")
        self.assertEqual(main.nombre_carta(carta("J")), "J♠")

    def test_un_solo_mazo_sin_repetidas(self):
        mazo = [False] * main.CANT_CARTAS_MAZO
        repartidas = [main.repartir_carta(mazo) for i in range(52)]
        self.assertEqual(sorted(repartidas), list(range(52)))
        self.assertTrue(all(mazo))

    def partida(self, cartas, entradas):
        # Las cartas se reparten en orden: jugador, banca, jugador, banca y luego las que se pidan
        with mock.patch.object(main, "repartir_carta", side_effect=[carta(c) for c in cartas]):
            return self.ejecutar(main.jugar_partida_blackjack, entradas, "Ana")

    def test_jugador_gana_al_plantarse(self):
        self.assertEqual(self.partida(["K", "10", "9", "7"], ["Plantarse"]), 1)

    def test_jugador_se_pasa(self):
        self.assertEqual(self.partida(["K", "10", "6", "7", "Q"], ["pedir"]), -1)
        self.assertIn("Te pasaste de 21", self.salida)

    def test_banca_pide_con_16_y_se_pasa(self):
        self.assertEqual(self.partida(["K", "10", "8", "6", "9"], ["xx", "plantarse"]), 1)
        self.assertIn("Opción inválida", self.salida)
        self.assertIn("La Banca se pasó", self.salida)

    def test_empate(self):
        self.assertEqual(self.partida(["K", "10", "8", "8"], ["plantarse"]), 0)

    def test_con_21_pasa_directo_a_la_banca(self):
        self.assertEqual(self.partida(["A", "10", "K", "9"], []), 1)
        self.assertIn("¡Llegaste a 21!", self.salida)

    def test_juego_registra_ganadas_y_perdidas_pero_no_empates(self):
        with mock.patch.object(main, "jugar_partida_blackjack", side_effect=[1, 0, -1]):
            self.ejecutar(main.juego_blackjack, ["Ana", "s", "s", "n"])
        jug = self.jugador("Ana")
        self.assertEqual(jug.juegos[main.FILA_GANADAS][main.JUEGO_BLACKJACK], 1)
        self.assertEqual(jug.juegos[main.FILA_PERDIDAS][main.JUEGO_BLACKJACK], 1)


class TestParImpar(BaseTest):

    def test_gana_y_pierde(self):
        with mock.patch.object(main.random, "randint", side_effect=[3, 4, 2, 2]):   # 7 impar, 4 par
            self.ejecutar(main.juego_par_impar, ["Ana", "100", "IMPAR", "s", "250.5", "impar", "n", ""])
        jug = self.jugador("Ana")
        self.assertEqual(jug.creditos, 10000 + 100 - 250.5)
        self.assertEqual(jug.juegos[main.FILA_GANADAS][main.JUEGO_PAR_IMPAR], 1)
        self.assertEqual(jug.juegos[main.FILA_PERDIDAS][main.JUEGO_PAR_IMPAR], 1)

    def test_apuestas_invalidas(self):
        with mock.patch.object(main.random, "randint", side_effect=[1, 1]):
            self.ejecutar(main.juego_par_impar, ["Ana", "abc", "-5", "0", "20000", "50", "par", "n", ""])
        self.assertIn("debe ingresar un número positivo", self.salida)
        self.assertIn("mayor a 0", self.salida)
        self.assertIn("no puede apostar más", self.salida)
        self.assertEqual(self.jugador("Ana").creditos, 10050.0)

    def test_sin_creditos_no_puede_seguir_jugando(self):
        with mock.patch.object(main.random, "randint", side_effect=[1, 1]):
            self.ejecutar(main.juego_par_impar, ["Ana", "10000", "impar", ""])
        self.assertEqual(self.jugador("Ana").creditos, 0)
        # Si pidiera otra apuesta se quedaría sin entradas y el test fallaría
        self.ejecutar(main.juego_par_impar, ["Ana", ""])
        self.assertIn("No tiene más créditos", self.salida)


class TestReporte(BaseTest):

    def test_ordenar_por_creditos(self):
        for nombre, creditos in (("Ana", 50), ("Beto", 300), ("Caro", 120)):
            pos = main.alta_jugador(nombre)
            main.registrar_resultado(pos, 0, True, creditos)
        self.ejecutar(main.reporte_jugadores_por_creditos, [""])
        self.assertLess(self.salida.index("Beto"), self.salida.index("Caro"))
        self.assertLess(self.salida.index("Caro"), self.salida.index("Ana"))

    def test_juegos_de_un_jugador(self):
        pos = main.alta_jugador("Ana")
        main.registrar_resultado(pos, main.JUEGO_BLACKJACK, True, 0)
        main.registrar_resultado(pos, main.JUEGO_BLACKJACK, False, 0)
        self.ejecutar(main.reporte_juegos_de_jugador, ["Ana", ""])
        self.assertIn("ganó 1 y perdió 1 veces", self.salida)
        self.assertIn("$10000.00", self.salida)
        self.ejecutar(main.reporte_juegos_de_jugador, ["Nadie", ""])
        self.assertIn("no está registrado", self.salida)

    def test_submenu_valida_opcion(self):
        self.ejecutar(main.reporte, ["z", "ab", "c"])
        self.assertEqual(self.salida.count("REPORTE"), 1)


class TestAdministracion(BaseTest):

    def clave(self, intentos):
        with mock.patch.object(main.getpass, "getpass", side_effect=intentos):
            return self.ejecutar(main.ingresar_clave_admin, [""])

    def test_clave_correcta_al_segundo_intento(self):
        self.assertTrue(self.clave(["mal", main.CLAVE_ADMIN]))
        self.assertIn("Le quedan 2 intentos", self.salida)

    def test_tres_intentos_fallidos(self):
        self.assertFalse(self.clave(["a", "b", "c"]))
        self.assertIn("Superó los 3 intentos", self.salida)

    def test_alta_categoria_rechaza_nombre_repetido_y_numera_consecutivo(self):
        self.crear_categoria(1, "Edad Famosos", [])
        self.ejecutar(main.alta_categoria, ["EDAD famosos", "Paises", "¿Qué país es más grande?", ""])
        self.assertIn("ya existe una categoría", self.salida)
        cat = leer_todos(main.FD_CATEGORIAS)[1]
        self.assertEqual(cat.nro_categoria, 2)
        self.assertEqual(main.recortar(cat.nombre_categoria), "Paises")
        self.assertEqual(cat.estado, "A")

    def test_modificacion_permite_mantener_su_propio_nombre(self):
        self.crear_categoria(1, "Edad", [])
        self.crear_categoria(2, "Peso", [])
        self.ejecutar(main.modificacion_categoria, ["2", "edad", "PESO", ""])
        self.assertIn("ya existe", self.salida)
        self.assertEqual(main.recortar(leer_todos(main.FD_CATEGORIAS)[1].nombre_categoria), "PESO")

    def test_baja_y_no_se_puede_modificar_inactiva(self):
        self.crear_categoria(1, "Edad", [])
        self.ejecutar(main.baja_categoria, ["1", "s", ""])
        self.assertEqual(leer_todos(main.FD_CATEGORIAS)[0].estado, "I")
        self.ejecutar(main.modificacion_categoria, [""])
        self.assertIn("No hay categorías activas", self.salida)

    def test_alta_opciones_sin_categorias(self):
        self.ejecutar(main.alta_opciones, [""])
        self.assertIn("se deben dar de alta categorías", self.salida)

    def test_alta_opciones_numera_y_rechaza_repetidos(self):
        self.crear_categoria(1, "Edad", [61])
        self.ejecutar(main.alta_opciones, ["1", "objeto 1-1", "Shakira", "x", "49", "n", ""])
        self.assertIn("ya está cargado", self.salida)
        self.assertIn("debe ingresar un número entero", self.salida)
        op = leer_todos(main.FD_OPCIONES)[1]
        self.assertEqual((op.nro_categoria, op.nro_opcion, main.recortar(op.objeto), op.valor), (1, 2, "Shakira", 49))

    def test_consulta_opciones(self):
        self.crear_categoria(1, "Edad", [61, 49])
        self.ejecutar(main.consulta_opciones, ["1", ""])
        self.assertIn("Objeto 1-2 - Valor: 49", self.salida)


class TestConsigna(unittest.TestCase):
    # Restricciones de la cátedra verificadas sobre el código fuente de main.py

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(CARPETA_TP3, "main.py"), encoding="utf-8") as archivo:
            cls.arbol = ast.parse(archivo.read())

    def test_solo_importa_bibliotecas_estandar(self):
        modulos = set()
        for nodo in ast.walk(self.arbol):
            if isinstance(nodo, ast.Import):
                modulos.update(alias.name for alias in nodo.names)
            elif isinstance(nodo, ast.ImportFrom):
                modulos.add(nodo.module)
        self.assertEqual(modulos, {"random", "os", "pickle", "getpass"})

    def test_sin_break_continue_ni_exit(self):
        for nodo in ast.walk(self.arbol):
            self.assertNotIsInstance(nodo, (ast.Break, ast.Continue))
            if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name):
                self.assertNotIn(nodo.func.id, ("exit", "quit", "sorted"))
            if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Attribute):
                self.assertNotIn(nodo.func.attr, ("sort", "find", "join", "append", "exit"))
            if isinstance(nodo, ast.While):
                self.assertFalse(isinstance(nodo.test, ast.Constant) and nodo.test.value is True)

    def test_return_solo_al_final_y_con_valor(self):
        for nodo in ast.walk(self.arbol):
            if isinstance(nodo, ast.FunctionDef):
                retornos = [n for n in ast.walk(nodo) if isinstance(n, ast.Return)]
                if retornos:
                    self.assertEqual(retornos, [nodo.body[-1]], nodo.name)
                    self.assertIsNotNone(retornos[0].value, nodo.name)


class TestProgramaCompleto(unittest.TestCase):
    # Corre main.py como programa real, en una copia aparte para no crear jugadores.dat en la entrega

    def test_navegar_menu_y_salir(self):
        carpeta = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, carpeta, True)
        shutil.copy(os.path.join(CARPETA_TP3, "main.py"), carpeta)
        entradas = "\n" + "z\n" + "e\n" + "a\n" + "\n" + "c\n" + "g\n" + "\n"
        entorno = dict(os.environ, PYTHONIOENCODING="utf-8")
        proceso = subprocess.run([sys.executable, "main.py"], cwd=carpeta, input=entradas,
                                 capture_output=True, text=True, encoding="utf-8", env=entorno, timeout=30)
        self.assertEqual(proceso.returncode, 0, proceso.stderr)
        self.assertIn("PROHIBIDOS PARA MENORES", proceso.stdout)
        self.assertIn("Ingreso inválido", proceso.stdout)
        self.assertIn("Todavía no hay jugadores registrados", proceso.stdout)
        self.assertIn("Gracias por jugar", proceso.stdout)
        # Sin .dat en la carpeta, el programa los crea con los datos de ejemplo
        self.assertTrue(os.path.exists(os.path.join(carpeta, "categorias.dat")))
        self.assertTrue(os.path.exists(os.path.join(carpeta, "opciones.dat")))


if __name__ == "__main__":
    unittest.main()
