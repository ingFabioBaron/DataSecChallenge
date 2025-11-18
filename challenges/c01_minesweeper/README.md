# Challenge 1 – Minesweeper

Este reto consiste en implementar la función obligatoria definida en el documento oficial:

```
def count_neighbouring_mines(board: list) -> list:
```

La función recibe un tablero representado como una lista de listas con valores **0** (vacío)  
y **1** (mina). La salida debe ser una nueva matriz donde:

- Las minas se representan como **9**  
- Cada celda vacía contiene la cantidad de minas adyacentes (en las 8 direcciones)

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

# ✔ Estado del reto

Este reto ya está implementado siguiendo:

- Python 3.11.9  
- La firma estricta requerida por el PDF  
- Buenas prácticas de diseño y testeo  

---
