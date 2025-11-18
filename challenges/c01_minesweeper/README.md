# Challenge 1 — Minesweeper Neighbour Counter

## 📝 Descripción General
Este challenge implementa la lógica del juego **Minesweeper**: para cada celda del tablero se calcula cuántas minas hay en las 8 posiciones adyacentes.

- **Input**: matriz 2D de enteros:
  - `0` → espacio vacío
  - `1` → mina
- **Output**: matriz 2D de enteros del mismo tamaño:
  - `9` → indica que la celda original contenía una mina
  - `0-8` → número de minas vecinas en las 8 direcciones

Problema: recorrido matricial, control de límites y conteo local.

---

## ✅ Requerimientos formales (firma obligatoria)

**Función obligatoria:**
```python
def count_neighbouring_mines(board: list) -> list:
    """
    Counts neighbouring mines for each cell in a Minesweeper board.

    Parameters:
        board (list): A 2D list where 0 represents an empty space and 1 represents a mine.

    Returns:
        list: A 2D list where each cell contains the count of neighbouring mines,
              or 9 if the cell contains a mine.
    """

---

# 📌 Ejemplo 

### Entrada:

```
[
  [0, 1, 0, 0],

  [0, 0, 1, 0],

  [0, 1, 0, 1],

  [1, 1, 0, 0]
]
```

### Salida esperada:

```
[
  [1, 9, 2, 1],
  [2, 3, 9, 2],
  [3, 9, 4, 9],
  [9, 9, 3, 1]
]
```

---

# 🧠 Reglas importantes del reto

1. La función debe llamarse **exactamente**:
   ```
   count_neighbouring_mines(board: list) -> list
   ```
2. El valor **1** en la entrada representa una mina.  
3. En la salida, las minas deben convertirse en **9**.  
4. El valor para cada celda vacía es el conteo de minas adyacentes.  
5. Se consideran las 8 direcciones:
   - Horizontal  
   - Vertical  
   - Diagonal  

---

# 🧪 Tests del reto

Los tests automáticos están ubicados en:

```
challenges/c01_minesweeper/tests/test_minesweeper.py
```

Puedes ejecutarlos con:

```bash
make test
```

o directamente:

```bash
pytest -q
```

---

# 🚀 Ejemplo de uso

```python
from challenges.c01_minesweeper.solution_minesweeper import count_neighbouring_mines

board = [
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 1, 0, 0]
]

result = count_neighbouring_mines(board)
print(result)
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

---

# 📂 Estructura del reto

```
c01_minesweeper/
├── solution_minesweeper.py
├── tests/
│   └── test_minesweeper.py
└── README.md
```

---

