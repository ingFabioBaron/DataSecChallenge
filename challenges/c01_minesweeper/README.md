# Challenge 1 · Minesweeper – Conteo de Minas Vecinas

## 📋 Resumen del problema
Se recibe un tablero de Minesweeper como matriz de números (0 = celda vacía, 1 = mina).  
La meta es construir **un nuevo tablero del mismo tamaño** donde:

- Las minas se representan con `9` para diferenciarlas claramente.
- Las celdas vacías muestran **cuántas minas hay en las 8 posiciones adyacentes**.
- La adyacencia contempla verticales, horizontales y diagonales.
- La función obligatoria es `count_neighbouring_mines(board: list) -> list`.

## ✅ Reglas funcionales clave
- Sólo se aceptan valores `0` y `1` como entrada.
- El tablero debe ser rectangular (todas las filas con la misma longitud).
- Tableros vacíos son válidos y retornan otra matriz vacía.
- Cualquier infracción dispara excepciones descriptivas (`ValueError` o `TypeError`).

## 🧠 Estrategia de solución
1. **Validación estricta** mediante `_validate_board`, evitando datos corruptos antes de procesar.
2. **Recorrido completo del tablero**; cada posición decide entre:
   - Copiar `9` si la celda original es una mina.
   - Contar vecinos usando las 8 direcciones precalculadas en `_NEIGHBOR_DIRECTIONS`.
3. **Construcción de un tablero nuevo** para mantener inmutable la entrada.
4. **Registro detallado** con `common.logging_config` para auditar entradas y salidas.

La complejidad temporal es `O(n*m)` con `n` filas y `m` columnas (cada celda evalúa un máximo de 8 vecinos).  
La complejidad espacial también es `O(n*m)` por el tablero resultante.

## 🗂️ Organización de archivos
- `solution_minesweeper.py`: implementación completa, validaciones y utilidades de logging.
- `run.py`: ejecutable de referencia que arma un tablero de ejemplo y muestra el resultado.
- `tests/test_solution_minesweeper.py`: suite de `pytest` con casos felices, bordes y errores.

## ▶️ Ejecución
Ubicarse en la raíz del repositorio.

**Con Make (recomendado)**
```bash
make run-ch1
```

**Sólo con Poetry**
```bash
poetry run python challenges/c01_minesweeper/run.py
```

## 🧪 Pruebas unitarias
```bash
poetry run pytest challenges/c01_minesweeper/
```
Casos cubiertos:
- Tableros no cuadrados y validaciones de tipo.
- Tablas sin minas, sólo minas y configuraciones mixtas.
- Conteo correcto en bordes y esquinas.

## 🧾 Ejemplo de I/O
Entrada:
```
[
  [0, 1, 0, 0],
  [0, 0, 1, 0],
  [0, 1, 0, 1],
  [1, 1, 0, 0]
]
```

Salida:
```
[
  [1, 9, 2, 1],
  [2, 3, 9, 2],
  [3, 9, 4, 9],
  [9, 9, 3, 1]
]
```

## 🚧 Edge cases cubiertos
- Tableros vacíos (`[]`).
- Filas con longitud desigual (se rechazan).
- Valores distintos de 0/1 (error explícito).
- Entradas `None` o tipos que no son listas.