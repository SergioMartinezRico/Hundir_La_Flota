import numpy as np   # type: ignore
import random
import time

#clases

#clase barco


class Barco:
    """
    Representa un barco:
    - Tiene una eslora (tamaño)
    - Guarda sus posiciones
    - Registra los impactos recibidos
    - Sabe si está hundido
    """

    def __init__(self, eslora):
        self.eslora = eslora
        self.coordenadas = []  # lista de tuplas (fila, columna)
        self.disparos = 0

    def registrar_disparo(self):
        """Suma un impacto al barco"""
        self.disparos += 1

    def hundido(self):
        """True si los impactos igualan o superan la eslora"""
        if self.disparos >= self.eslora:
            return True
        else:
            return False

#clase tablero

class Tablero:
    """
    Representa un tablero de Hundir la Flota:
    - self.tablero_juego: posiciones reales de los barcos
    - self.tablero_mostrar: lo que se va mostrando al jugador
    - self.posiciones : lista de posiciones
    - self.libre : lista de casillas que tienen que estar libres alrededor de un barco
    """

    def __init__(self, tamano=10):
        self.tamano = tamano
        self.tablero_juego = np.full((tamano, tamano), "_")   # tablero interno
        self.tablero_mostrar = np.full((tamano, tamano), "⬜") # tablero que se muestra
        self.posiciones = []  # lista de todos los barcos
        self.libres = set()   # celdas alrededor de barcos

    # comprobamos si un barco se puede colocar

    def puede_colocar(self, posiciones):
        for fila, col in posiciones:
            if (fila, col) in self.libres:
                return False
            if fila < 0 or fila >= self.tamano or col < 0 or col >= self.tamano:
                return False
        return True

   #colocar un barco dandole una eslora

    def colocar_barco(self, eslora):
        colocado = False
        intentos = 0
        while colocado == False and intentos < 1000:
            intentos += 1
            barco = Barco(eslora)
            orientacion = random.choice("HV")

            if orientacion == "H":
                fila = random.randint(0, self.tamano - 1)
                col = random.randint(0, self.tamano - eslora)
                posiciones = [(fila, col + i) for i in range(eslora)]
            else:
                fila = random.randint(0, self.tamano - eslora)
                col = random.randint(0, self.tamano - 1)
                posiciones = [(fila + i, col) for i in range(eslora)]

            if self.puede_colocar(posiciones):
                barco.coordenadas = posiciones
                self.posiciones.append(barco)
                for f, c in posiciones:
                    self.tablero_juego[f, c] = "B"
                    # marcar alrededor como libre
                adyacentes = set()
                for i in range(f-1, f+2):
                    for j in range(c-1, c+2):
                        if 0 <= i < self.tamano and 0 <= j < self.tamano:
                            adyacentes.add((i, j))
                self.libres.update(adyacentes)
                colocado = True

                

    #repite colocar con una lista de valores
    def colocar_flota(self, flota):
        for eslora in flota:
            self.colocar_barco(eslora)

   #disparar

    def disparar(self, fila, col):
        if fila < 0 or fila >= self.tamano or col < 0 or col >= self.tamano:
            return "fuera"

        if self.tablero_mostrar[fila, col] != "⬜":
            return "repetido"

        if self.tablero_juego[fila, col] == "B":
            self.tablero_mostrar[fila, col] = "💥"
            for barco in self.posiciones:
                if (fila, col) in barco.coordenadas:
                    barco.registrar_disparo()
                    if barco.hundido() == True:
                        return "hundido"
                    break
            return "tocado"
        else:
            self.tablero_mostrar[fila, col] = "🌊"
            return "agua"

   # comprobamos si todos estan hundidos

    def todos_hundidos(self):
        for barco in self.posiciones:
            if barco.hundido() == False:
                return False
        return True

  # mostrar tablero

    def mostrar(self):

        tablero = self.tablero_mostrar.copy().astype(str)
        # Columna de números 
        col_numeros = np.array([[" 1"], [" 2"], [" 3"], [" 4"], [" 5"],[" 6"], [" 7"], [" 8"], [" 9"], ["10"]])
        # Fila de letras mas un hueco para cuadrar
        fila_letras = np.array([["  ", " A", " B", " C", " D", " E", " F", " G", " H", " I", " J"]])
        # Concatenar números a la izquierda
        tablero_numerado = np.hstack((col_numeros, tablero))
        # Concatenar letras arriba
        tablero_final = np.vstack((fila_letras, tablero_numerado))
        print(tablero_final)

#funciones

#match letras numeros


def match_letras(letra):
    """Convierte letra A-J en índice 0-9"""
    dicc_col = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9}
    letra = letra.upper()
    if letra in dicc_col:
        return dicc_col[letra]
    else:
        return -1  # fuera de rango

def match_numeros(numero): #para la demo
    """Convierte letra A-J en índice 0-9"""
    dicc_col = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H",8:"I",9:"J"}
    if numero in dicc_col:
        return dicc_col[numero]

def pedir_coordenadas():
    """Pide al jugador fila y columna válidas"""
    valido = False
    while valido == False:
        try:
            print("Dispara")
            fila = int(input("Dime una fila (1-10): ")) - 1
            col = input("Dime una columna (A-J): ")
            col = match_letras(col)
            if fila < 0 or fila > 9 or col == -1: #comprobamos si no estan en el rango
                print("Coordenadas fuera de rango. Intenta de nuevo.")
            else:
                valido = True
        except ValueError:
            print("Entrada no válida. Intenta de nuevo.")
    return fila, col

def turno_jugador(tablero_enemigo):
    """Turno del jugador:
     -pìde coordenadas con la funcion 
     -usa el metodo disparar de tablero
     -con el resultado, decide si tocado o agua
     -comprueba si fuera o repetido
     -se basa en una variable jugar que cuando pasa a false acaba el turno
       """
    jugar = True
    while jugar == True:
        fila, col = pedir_coordenadas()
        resultado = tablero_enemigo.disparar(fila, col)
        
        if resultado == "tocado":
            print("💥💥💥Has tocado un barco!💥💥💥")
            time.sleep(1)
            tablero_enemigo.mostrar()
            # si todos los barcos del enemigo están hundidos, termina el juego
            if tablero_enemigo.todos_hundidos():
                return "ganado" #se acaba el while
            # si no, el jugador sigue disparando

        elif resultado == "hundido":
            print("💥💥💥Has hundido un barco!💥💥💥")
            time.sleep(1)
            tablero_enemigo.mostrar()
            # si todos los barcos del enemigo están hundidos, termina el juego
            if tablero_enemigo.todos_hundidos():
                return "ganado" #se acaba el while
            # si no, el jugador sigue disparando

        elif resultado == "agua":
            print("🌊🌊🌊Has fallado. Agua.🌊🌊🌊")
            time.sleep(1)
            tablero_enemigo.mostrar()
            jugar = False  # termina el turno del jugador

        elif resultado == "repetido":
            print("Ya habías disparado ahí. Prueba otra vez.")

        elif resultado == "fuera":
            print("Coordenadas fuera del tablero. Prueba otra vez.")

def turno_enemigo(tablero_jugador):
    """Turno de el enemigo
     -crea coordenadas random
     -usa el metodo disparar de tablero
     -con el resultado, decide si tocado o agua
     -comprueba si fuera o repetido
     -se basa en una variable jugar que cuando pasa a false acaba el turno
    """
    jugar = True
    while jugar == True:
        fila = random.randint(0, 9)
        col = random.randint(0, 9)
        resultado = tablero_jugador.disparar(fila, col)
        letra = match_numeros(col)
        numero = fila + 1

        if resultado == "tocado":
            time.sleep(0.5)
            print(f"💥💥💥el enemigo dispara a {numero}{letra}: Tocado!💥💥💥")
            time.sleep(1)
            tablero_jugador.mostrar()
            # si todos los barcos del jugador están hundidos, termina el juego
            if tablero_jugador.todos_hundidos():
                return "perdido" #se acaba el while
            # si no, el enemigo sigue disparando
        
        elif resultado == "hundido":
            print("💥💥💥Te han hundido un barco!💥💥💥")
            time.sleep(1)
            tablero_jugador.mostrar()
            # si todos los barcos del enemigo están hundidos, termina el juego
            if tablero_jugador.todos_hundidos():
                return "perdido" #se acaba el while
            # si no, el jugador sigue disparando

        elif resultado == "agua":
            time.sleep(0.5)
            print(f"🌊🌊🌊el enemigo dispara a {numero}{letra}: Agua.🌊🌊🌊")
            time.sleep(2)
            tablero_jugador.mostrar()
            jugar = False  # termina el turno de el enemigo

        elif resultado == "repetido":
            print(f"el enemigo dispara a {numero}{letra}: Repetido.")
            # intenta otra vez con nuevas coordenadas
            continue

        elif resultado == "fuera":
            print(f"el enemigo dispara a {numero}{letra}: Incorrecto.")
            # intenta otra vez
            continue

#juego

def jugar_partida():
    """Bucle principal de juego
    se dan las esloras de las flotas
    se crean los tableros
    se colocan las flotas
    se empieza a jugar
    """
    flota = [4,3,3,2,2,2]

    tablero_jugador = Tablero()
    tablero_enemigo = Tablero()

    tablero_jugador.colocar_flota(flota)
    tablero_enemigo.colocar_flota(flota)

    jugando = True
    print("Comienza la partida!\n")

    while jugando == True: #cuando jugando pase a ser false se acaba la partida
        
        # Turno del jugador
        print('\n' * 5)
        print("\nTu turno:")
        print('\n' * 2)
        print("TABLERO DEL ENEMIGO")
        print('\n' * 2)
        tablero_enemigo.mostrar()
        time.sleep(1)
        estado = turno_jugador(tablero_enemigo)
        if estado == "ganado":
            print("Has ganado! Todos los barcos enemigos están hundidos.")
            jugando = False
            break

        # Turno del enemigo
        print('\n' * 5)
        print("\nTurno del enemigo:")
        print('\n' * 2)
        print("TABLERO DEL JUGADOR")
        print('\n' * 2)
        tablero_jugador.mostrar()
        time.sleep(1)
        estado = turno_enemigo(tablero_jugador)
        if estado == "perdido":
            print("Has perdido. El enemigo ha hundido todos tus barcos.")
            jugando = False
            break

def jugar_demo():
    """Bucle principal de juego
    se dan las esloras de las flotas
    se crean los tableros
    se colocan las flotas
    se empieza a jugar
    """
    flota = [2,2]

    tablero_jugador = Tablero()
    tablero_enemigo = Tablero()

    tablero_jugador.colocar_flota(flota)
    tablero_enemigo.colocar_flota(flota)

     # Mostrar las coordenadas del enemigo (para DEMO)
    print("\n=== COORDENADAS DEL ENEMIGO ===")
    for barco in tablero_enemigo.posiciones:
        coord = [(sorted(barco.coordenadas))]
        for lista in coord:
          for fila, col in lista:
              print (fila + 1 , match_numeros(col) )
    print("===============================\n")

    jugando = True
    print("Comienza la partida!\n")

    while jugando == True: #cuando jugando pase a ser false se acaba la partida

        # Turno del jugador
        print('\n' * 2)
        print("\nTu turno:")
        print('\n' * 2)
        print("TABLERO DEL ENEMIGO")
        print('\n' * 2)
        tablero_enemigo.mostrar()
        estado = turno_jugador(tablero_enemigo)
        if estado == "ganado":
            print("🎉🚢✨ ¡VICTORIA! ¡EL MAR ES TUYO! ✨🚢🎉")
            print("Todos los barcos enemigos están hundidos.")
            print("⚓🏆 ¡HAS GANADO LA BATALLA NAVAL! 🏆⚓")
            jugando = False
            break

        # Turno del enemigo
        print('\n' * 2)
        print("\nTurno del enemigo:")
        print('\n' * 2)
        print("TABLERO DEL JUGADOR")
        print('\n' * 2)
        tablero_jugador.mostrar()
        estado = turno_enemigo(tablero_jugador)
        if estado == "perdido":
            print ("🌊💀💔 ¡DERROTA NAVAL! ¡TU FLOTA HA CAÍDO! 💔💀🌊")
            print("Has perdido. El enemigo ha hundido todos tus barcos.")
            print("😭🕯️ ¡LA PRÓXIMA VEZ SERÁ TUYA! 🕯️😭")
            jugando = False
            break

    