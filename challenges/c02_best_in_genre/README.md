Challenge 2: REST API – Best TV Shows in Genre
Objetivo del Desafío

El objetivo de este challenge es consultar una API pública y determinar cuál es la serie de televisión con mejor calificación en un género específico.

La función debe:

Recibir un parámetro genre como texto (por ejemplo: "Action", "Comedy", "Drama").

Realizar múltiples solicitudes HTTP GET a la API paginada:
https://jsonmock.hackerrank.com/api/tvseries

Analizar todas las páginas para obtener la totalidad de las series.

Filtrar únicamente las series cuyo campo genre contenga el género dado, sin importar mayúsculas o minúsculas.

Comparar las series filtradas por su valor imdb_rating.

En caso de empate, retornar el nombre alfabéticamente menor.

Retornar únicamente el nombre de la serie como texto.

Debe implementarse exactamente la función:
def bestInGenre(genre: str) -> str

Solución Implementada

Enfoque Algorítmico
La solución realiza lo siguiente:

Se envía la primera solicitud HTTP GET para obtener la información inicial y determinar cuántas páginas tiene la API.

Se recorren todas las páginas con solicitudes completas usando el parámetro page.

Se convierten los géneros de cada serie en una lista, separando por coma y normalizando mayúsculas/minúsculas.

Se seleccionan únicamente las series que incluyen el género indicado.

Se identifica la serie con el mayor imdb_rating.

Si dos o más series tienen el mismo rating, se aplica un desempate lexicográfico comparando los nombres.

Finalmente, se retorna únicamente el nombre de la mejor serie del género.

Este enfoque asegura la cobertura completa de la API, un filtrado correcto y una comparación precisa según las reglas de negocio.

Estructura del Código
Los archivos están organizados así:

challenges/c02_best_in_genre/solution_best_in_genre.py
Contiene la función bestInGenre con toda la lógica de consultas, filtrado y selección.

challenges/c02_best_in_genre/run.py
Script ejecutable que permite probar la función solicitando un género y mostrando la serie resultante.

challenges/c02_best_in_genre/tests/test_best_in_genre.py
Pruebas unitarias diseñadas para verificar que la función maneje correctamente géneros simples, múltiples géneros por serie, empates y comportamiento general.

Instrucciones de Ejecución

Ubicarse en la raíz del proyecto.

Opción A: usando make
make run-ch2

Opción B: usando Poetry
poetry run python challenges/c02_best_in_genre/run.py

Ejemplo de Entrada y Salida

Input:
Action

Output esperado:
Game of Thrones

Explicación:
Entre todas las series del género Action, "Game of Thrones" posee la calificación más alta (9.3).
En el archivo PDF del challenge se listan también otras series de referencia, pero ninguna supera esa puntuación.

Pruebas Unitarias

Las pruebas de este challenge están en:
challenges/c02_best_in_genre/tests/test_best_in_genre.py

Para ejecutarlas:
poetry run pytest challenges/c02_best_in_genre/