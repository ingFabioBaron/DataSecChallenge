# DataSecChallenge – Soluciones en Python

Este repositorio contiene la implementación en **Python 3.11.9** de los retos incluidos en el  
**Mercado Libre DataSec Challenge**.

Toda la estructura del proyecto está organizada como un **monorepo**, donde cada reto vive dentro
de la carpeta `challenges/`.  
Además, se incluye un módulo común (`common/`) para funcionalidades compartidas entre los retos.

---

## 🧩 Logging centralizado

El proyecto incluye un sistema de logging compartido ubicado en:

```
common/logging_config.py
```

Puedes utilizarlo en cualquier challenge de la siguiente manera:

```python
from common.logging_config import get_logger

logger = get_logger(__name__)
logger.info("Mensaje de ejemplo")
```

### ✔ Características del logger

- Formato de log profesional y uniforme  
- Evita duplicación de handlers  
- Respeta la variable de entorno `LOG_LEVEL`  
- Nivel predeterminado: `INFO`  
- Compatible con cualquier challenge dentro del monorepo

### ✔ Definir nivel de log (opcional)

```bash
LOG_LEVEL=DEBUG
```

Si no defines esta variable, el logger utilizará el nivel `INFO`.

---

## ⚙️ Configuración del entorno

Este proyecto utiliza **Poetry 2.x** para gestionar dependencias y entornos virtuales.

Verificar instalación de Poetry:

```
poetry --version
```

Crear o sincronizar el entorno virtual:

```
poetry install
```

Activar el entorno virtual usando el mecanismo moderno:

```
poetry env activate
```

O instalar el plugin para recuperar el comportamiento clásico:

```
poetry self add poetry-plugin-shell
poetry shell
```

---

## 🚀 Ejecutar el proyecto con y sin Make

Este repositorio incluye un `Makefile` para simplificar la ejecución de comandos frecuentes.  
Sin embargo, el uso de Make es **opcional** — si no está instalado, puedes ejecutar los  
comandos manualmente usando Poetry.

---

## ✔ Verificar si tienes Make instalado

En Windows (PowerShell o CMD):

```
make --version
```

Si ves un mensaje como:

```
'make' no se reconoce...
```

entonces Make no está instalado.

En Linux o macOS:

```
make --version
```

Make suele venir preinstalado.

---

## 🚀 Ejecutar usando Make (recomendado)

Si tienes Make disponible:

```
make install     # instala dependencias
make test        # ejecuta todos los tests
make fmt         # formatea con Black
make lint        # corre Ruff
```

---

## 🚀 Ejecutar sin Make (comandos manuales)

Si no tienes Make, puedes usar Poetry directamente:

Instalar dependencias:

```
poetry install
```

Correr tests:

```
poetry run pytest -q
```

Formatear código:

```
poetry run black .
```

Ejecutar linters:

```
poetry run ruff check .
```

---

## ⭐ Recomendación

Si estás en Windows y deseas usar Make, puedes instalarlo fácilmente mediante:

- Git Bash (viene incluido)
- WSL (Ubuntu): `sudo apt install make`
- MSYS2: `pacman -S make`
- Windows (nativo):  
  ```
  winget install ezwinports.make
  ```

---

## 📁 Estructura general del proyecto

```
DataSecChallenge/
├── challenges/
│   ├── c01_minesweeper/
│   ├── c02_best_in_genre/
│   ├── c03_sql_failures/
│   └── c04_summarizer/
├── common/
│   └── logging_config.py
├── docs/
│   ├── adr/
│   └── architecture/
├── .github/
│   └── workflows/
│       └── ci.yml   (cuando se agregue)
├── Makefile
├── pyproject.toml
└── README.md
```

---

## 📄 Licencia

Este proyecto es únicamente para fines académicos y de evaluación técnica.
