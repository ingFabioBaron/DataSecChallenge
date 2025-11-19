# Challenge 2 · REST API – Best TV Show per Genre

## 📋 Resumen del problema
Consumir la API pública paginada `https://jsonmock.hackerrank.com/api/tvseries` y responder con **el nombre de la serie con mejor `imdb_rating` para un género dado**.  
Requisitos principales:
- Entrada: `genre` como texto (p. ej. `"Action"`).
- Comparar todas las páginas de la API (no basta con la primera).
- Coincidencia de género **case-insensitive** y tolerante a espacios.
- En caso de empate en rating, devolver el nombre alfabéticamente menor.
- Firma requerida: `def bestInGenre(genre: str) -> str`.

## 🔍 Consideraciones funcionales
- Se valida que `genre` sea `str` y no esté vacío → errores explícitos (`TypeError`, `ValueError`).
- Se toleran datos incompletos de la API (ratings vacíos o géneros mal formados).
- Cualquier error de red/HTTP se loguea y retorna `""` para evitar fallas silenciosas.
- Tiempo de espera configurado en `REQUEST_TIMEOUT = 5s` para cada request.

## 🧠 Estrategia de solución
1. **Descubrimiento de paginación**: la primera respuesta informa `total_pages`; se itera hasta cubrirlas todas.
2. **Normalización de datos**:
   - `genre` → `casefold()` + `strip()` para comparaciones consistentes.
   - Campo `genre` de la API dividido por comas y tokens normalizados con `_normalize_genre_token`.
3. **Selección del candidato**:
   - Se convierte cada `imdb_rating` a `float`. Valores inválidos se tratan como `0`.
   - Se actualiza `best_rating` y `best_name` sólo cuando se supera el rating o se resuelve un empate lexicográfico.
4. **Trazabilidad**: el módulo usa `common.logging_config` para registrar requests, coincidencias y métricas finales.

Complejidad temporal: `O(p * r)` con `p` páginas y `r` registros por página.  
Espacial: `O(1)` fuera del buffer de respuesta (se procesa streaming de páginas).

## 🗂️ Organización
- `solution_best_in_genre.py`: función principal, validaciones y utilidades de networking.
- `run.py`: permite solicitar el género por consola y mostrar la respuesta.
- `tests/test_best_in_genre.py`: mocks de la API y casos de prueba (éxito, empates, errores de red, inputs inválidos).

## ▶️ Ejecución
Desde la raíz del repo:

**Con Make**
```bash
make run-ch2
```

**Con Poetry puro**
```bash
poetry run python challenges/c02_best_in_genre/run.py
```

## 🧪 Pruebas unitarias
```bash
poetry run pytest challenges/c02_best_in_genre/
```
Cobertura relevante:
- Géneros simples y mezclas (`"Action, Drama"`).
- Empates de rating y resolución lexicográfica.
- Manejo de `RequestException` o JSON inválido.
- Validaciones de entrada.

## 🧾 Ejemplo de uso
Entrada:
```
Action
```

Salida esperada:
```
Game of Thrones
```
Porque es la serie de acción con rating 9.3, superior al resto, según los datos mock de HackerRank.

## 🚧 Edge cases considerados
- Género con espacios extra (`"  drama  "`).
- Página sin datos (API parcial) → se continúa sin fallar.
- Campos `genre` no string → se ignoran.
- API que retorna 0 páginas → resultado vacío.