# Hundir_La_Flota

Este proyecto implementa una versión simple del clásico juego de mesa Hundir la Flota (Battleship) en Python, utilizando la librería numpy para la gestión de los tableros.

⚙️ Requisitos
Necesitas tener instalada la librería numpy

💻 Estructura del Código
El código se organiza en dos clases principales y varias funciones.

Clases Principales
Barco:

Gestiona la eslora, las coordenadas y el número de impactos.

Método clave: hundido() (verifica si los impactos igualan la eslora).

Tablero:

Gestiona dos tableros de 10x10:

tablero_juego: Posiciones reales de los barcos ("B"). Es el tablero oculto.

tablero\*mostrar: Lo que ve el jugador ("💥": tocado, "🌊": agua, "⬜": sin disparar).

Método clave: colocar_barco() y disparar(fila, col) (procesa los disparos).

Asegura la separación de una casilla entre barcos mediante el conjunto self.libres.

Funciones de Juego

match_letras(letra) / match_numeros(numero): Convierten entre letras de columna (A-J) y sus índices numéricos (0-9).

pedir_coordenadas(): Solicita la entrada del usuario (ej. 1-10 y A-J) y valida el rango.

turno_jugador(tablero_enemigo):

Pide coordenadas.

Dispara.

Si acierta (tocado/hundido), el jugador repite turno.

turno_enemigo(tablero_jugador):

Dispara a coordenadas aleatorias.

Si acierta (tocado/hundido), el enemigo repite turno.

jugar_partida(): Inicializa los tableros con la flota estándar ([4,3,3,2,2,2]) y ejecuta el bucle principal de turnos hasta que un jugador gana.

jugar_demo(): Versión más corta ([4,3,2]) que muestra las coordenadas del enemigo al inicio.

🎮 Cómo Jugar
Asegúrate de que la función jugar_partida() (o jugar_demo()) se llama al final del script.

Ejecuta el archivo Python juego.py

Durante tu turno, ingresa la fila (1-10) y la columna (A-J) para disparar al tablero enemigo.

El juego termina cuando todos los barcos en un tablero son hundidos.
