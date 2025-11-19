Challenge 1: Minesweeper Number of Neighbouring Mines
Objetivo del Desafío

El objetivo de este challenge es implementar una función que procese un tablero de Minesweeper representado como una matriz bidimensional de números enteros. Cada celda del tablero contiene un 0 (espacio vacío) o un 1 (mina).

La función debe generar y retornar un nuevo tablero de igual tamaño donde cada celda contenga:

El número de minas adyacentes (valores entre 0 y 8) si la celda original es un espacio vacío.

El valor 9 si la celda original contiene una mina.

La definición de "adyacencia" incluye las 8 posibles direcciones: arriba, abajo, izquierda, derecha y diagonales.

La función debe implementarse exactamente con la firma especificada:
def count_neighbouring_mines(board: list) -> list

Solución Implementada

Enfoque Algorítmico
Se utiliza un recorrido completo de la matriz. Para cada celda se determina si es mina o espacio vacío.

Si la celda es una mina (valor 1), se asigna el valor 9 directamente en el resultado.

Si la celda es un espacio vacío, se cuentan las minas adyacentes recorriendo las 8 posiciones posibles alrededor de la celda.

Se valida que las coordenadas adyacentes estén dentro del rango de la matriz para evitar errores de índice.

La solución funciona únicamente con enteros 0 y 1 tal como lo exige el enunciado.

No se modifica el tablero original; se construye uno nuevo siguiendo los requisitos.

Este enfoque garantiza una solución clara, eficiente y totalmente alineada con el comportamiento esperado de Minesweeper.

Estructura del Código
El challenge está organizado de la siguiente manera:

challenges/c01_minesweeper/solution_minesweeper.py
Contiene la función count_neighbouring_mines con toda la lógica requerida.

challenges/c01_minesweeper/run.py
Script ejecutable que carga un ejemplo de tablero, llama la función y muestra el resultado por consola.

challenges/c01_minesweeper/tests/test_solution_minesweeper.py
Archivo de pruebas unitarias encargado de validar el funcionamiento correcto de la solución según múltiples escenarios.

Instrucciones de Ejecución

Ubicarse en la raíz del proyecto.

Opción A: usando make
make run-ch1

Opción B: usando Poetry
poetry run python challenges/c01_minesweeper/run.py

Ejemplo de Entrada y Salida

Input:
[
[0, 1, 0, 0],
[0, 0, 1, 0],
[0, 1, 0, 1],
[1, 1, 0, 0]
]

Output:
[
[1, 9, 2, 1],
[2, 3, 9, 2],
[3, 9, 4, 9],
[9, 9, 3, 1]
]

Pruebas Unitarias

Las pruebas correspondientes a este challenge se encuentran en:
challenges/c01_minesweeper/tests/test_solution_minesweeper.py

Para ejecutar solo estas pruebas:
poetry run pytest challenges/c01_minesweeper/