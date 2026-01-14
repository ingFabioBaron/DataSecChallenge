# 🚀 Solución al Mercado Libre DataSec Challenge

## 🌟 Descripción General del Proyecto

Este repositorio contiene la **implementación completa** de la prueba técnica solicitada para el **Mercado Libre DataSec Challenge**.

La solución está desarrollada principalmente en **Python 3.11.9**, con una sección en **GoLang (versión 1.25.5)** para el Challenge 4, sirviendo como ejemplo de migración de Python a Go. Está organizada bajo una arquitectura de **monorepo**. Cada desafío reside en su propia carpeta bajo `challenges/`, lo que garantiza la **modularidad e independencia** de las soluciones.

El proyecto también incluye un módulo **`common/`** para albergar funcionalidades transversales, mejorando la reutilización y el mantenimiento del código.

El Challenge 4 (`c04_summarizer`) es el foco de la migración, con la versión Python en `c04_summarizer_py` y la versión Go en `c04_summarizer`.

## 🎯 Enfoque y Metodología

La solución se desarrolló priorizando la **calidad, la automatización y la mantenibilidad** del código:

- **Conformidad con PEP 8:** Adherencia a los estándares de estilo de código de Python.
- **Modularidad:** Cada reto está autocontenido y diseñado para ser ejecutable de forma independiente.
- **Gestión de Dependencias Robusta:** Utilización de **Poetry** para entornos virtuales aislados y gestión precisa de dependencias (Python).
- **Control de Calidad:** Integración de herramientas de _linting_ como **Ruff** para el análisis estático y la detección de errores (Python).

## 🛠️ Tecnologías y Herramientas de Desarrollo

| Categoría         | Tecnología/Librería | Versión        | Propósito                                                  |
|-------------------|---------------------|----------------|------------------------------------------------------------|
| **Lenguaje Base** | Python              | 3.11.9         | Plataforma de desarrollo principal.                        |
| **Lenguaje Adicional**| GoLang             | 1.25.5         | Utilizado para la migración del Challenge 4.              |
| **CLI Framework (Go)**| Cobra              | 1.10.2+        | Construcción de interfaces de línea de comandos en Go.     |
| **Env Vars (Go)** | godotenv            | 1.5.1+         | Carga de variables de entorno desde archivos `.env` en Go. |
| **Gestión de Entorno** | Poetry             | 2.x            | Configuración y gestión de dependencias del proyecto (Python). |
| **Base de Datos** | SQLite3             | (Estándar)     | Usado en Challenge 3 para simular la base de datos de reportes de fallas. |
| **GenAI / NLP**   | HuggingFace         | (Depende del modelo)| Usado en Challenge 4 para consumir modelos de _Text Summarizer_ (versiones Python y Go). |
| **Análisis Estático** | Ruff               | -              | _Linting_ y chequeo de calidad de código (`make lint`) (Python). |
| **Pruebas (Python)** | pytest             | -              | Marco de trabajo para la ejecución de pruebas unitarias (Python). |
| **Pruebas (Go)**  | Go `testing`        | (Estándar)     | Framework de pruebas nativo de Go.                         |

## ⚙️ Instalación y Preparación del Entorno

Este proyecto utiliza **Poetry** para una configuración de entorno consistente y reproducible (para Python), y **Go Modules** para la gestión de dependencias en Go.

### 1. Clonar el Repositorio

Abra su terminal y ejecute:
```bash
git clone https://github.com/ingFabioBaron/DataSecChallenge.git
cd DataSecChallenge
```

### 2. Requisitos Previos

*   **Poetry 2.x**: Asegúrese de tener Poetry instalado para las partes de Python.
*   **GoLang 1.25.5+**: Asegúrese de tener Go instalado para la solución del Challenge 4 en Go.

### 3. Configuración e Instalación de Dependencias

Ejecute los siguientes comandos para crear el entorno virtual de Python y resolver todas las dependencias:
```bash
poetry install
```

Para las dependencias de Go, una vez que haya configurado el módulo principal (ya hecho en este punto si está siguiendo la migración), Go gestionará automáticamente las dependencias. Sin embargo, puede ejecutar:
```bash
go mod tidy
```

### 4. Verificación y Ejecución Manual de Tareas

#### 4.1. Verificar si tiene Make instalado

En **Windows** (PowerShell o CMD):
```bash
make --version
```

Si ve un mensaje como: `'make' no se reconoce...`, entonces Make no está instalado.

En **Linux o macOS**:
```bash
make --version
```

Make suele venir preinstalado.

#### 4.2. Ejecutar sin Make (Comandos Manuales)

Si no tiene Make, puede usar **Poetry** (para Python) o **Go** directamente para ejecutar las tareas de desarrollo:

| Tarea                      | Comando Manual                  | Comando con Make        |
|----------------------------|-----------------------------------|-------------------------|
| Instalar dependencias      | `poetry install` (Python)         | `make install`          |
| Correr tests (Python)      | `poetry run pytest -q`            | `make test`             |
| Formatear código (Black)   | `poetry run black .`              | `make format` (si existe) |
| Ejecutar linters (Ruff)    | `poetry run ruff check .`         | `make lint`             |
| Ejecutar C4 (Go)           | `go run challenges/c04_summarizer`| `make run-ch4`          |
| Ejecutar tests C4 (Go)     | `go test ./challenges/c04_summarizer/summarizer`| `make test-ch4`         |

#### 4.3. ⭐ Recomendación de Instalación (Windows)

Si está en Windows y desea usar Make (opción recomendada), puede instalarlo fácilmente mediante:

- **Git Bash:** (Viene incluido con la instalación estándar)
- **WSL (Ubuntu):** `sudo apt install make`
- **MSYS2:** `pacman -S make`
- **Windows (nativo):** `winget install ezwinports.make`

## 🧩 Variables de Entorno (Archivo `.env.example`)

El proyecto requiere la configuración de algunas variables de entorno para su correcta ejecución, especialmente en el **Challenge 4**. Se proporciona el archivo `.env.example` que debe ser copiado a un archivo **`.env`** y rellenado.

| Variable          | Challenge   | Descripción y Obligatoriedad                     |
|-------------------|-------------|--------------------------------------------------|
| **`LOG_LEVEL`**   | Transversal | Nivel de logging para todo el proyecto (ej: `INFO`, `DEBUG`). |
| **`DB_PATH`**     | Challenge 3 | Ruta local para el archivo de la base de datos SQLite.          |
| **`HF_API_TOKEN`**| Challenge 4 | **Obligatorio.** Token de API de HuggingFace necesario para el funcionamiento del Summarizer (Python y Go). |
| **`HF_MODEL`**    | Challenge 4 | Opcional. Permite especificar un modelo diferente para el Summarizer (Python y Go). |
| **`ARTICLE_PATH`**| Challenge 4 | Opcional. Ruta al archivo de texto que se utilizará como artículo de entrada por defecto para la versión Go. Por defecto `articles/article.txt` si no se proporciona. |

## 🚀 Automatización de Tareas (Makefile)

El repositorio incluye un `Makefile` completo para simplificar la ejecución de las tareas de desarrollo y los desafíos individuales.

> **Recomendación:** Se recomienda enfáticamente tener **Make** instalado para una ejecución más ágil y estandarizada de las tareas comunes (`test`, `lint`, `run-chX`). Es importante notar que **todos los comandos listados pueden ser ejecutados de forma manual utilizando `poetry run ...`** (para Python) o los comandos nativos de `go` (para Go) si no dispone de `make`.

| Tarea                | Comando Make       | Descripción                                             |
|----------------------|--------------------|---------------------------------------------------------|
| **Instalación**      | `make install`     | Instala todas las dependencias con Poetry (Python).     |
| **Pruebas (Python)** | `make test`        | Ejecuta todos los tests unitarios con `pytest` (Python). |
| **Análisis Estático**| `make lint`        | Ejecuta el linter `ruff` sobre todo el código base (Python). |
| **Ejecución C1**     | `make run-ch1`     | Ejecuta la solución del Challenge 1 (Minesweeper - Python). |
| **Ejecución C2**     | `make run-ch2`     | Ejecuta la solución del Challenge 2 (Best In Genre - Python). |
| **Ejecución C3**     | `make run-ch3`     | Ejecuta la solución del Challenge 3 (SQL Failures - Python). |
| **Ejecución C4 (Python)**| `make run-ch4-py`  | Ejecuta las 3 modalidades del Challenge 4 (Summarizer - Python). |
| **Ejecución C4 (Go)**| `make run-ch4`     | Ejecuta las 3 modalidades del Challenge 4 (Summarizer - Go). |
| **Pruebas C4 (Go)**  | `make test-ch4`    | Ejecuta los tests unitarios del Challenge 4 (Go).       |
| **Limpieza**         | `make clean`       | Elimina archivos temporales de Python (`__pycache__`, `.pytest_cache`). |
| **Ayuda**            | `make help`        | Muestra la lista completa de comandos disponibles.       |

## 📂 Estructura del Proyecto
```
DataSecChallenge/
├── challenges/
│   ├── c01_minesweeper/   <- Desafío 1: Minesweeper
│   ├── c02_best_in_genre/ <- Desafío 2: Best In Genre
│   ├── c03_sql_failures/  <- Desafío 3: SQL Failures
│   ├── c04_summarizer/    <- Desafío 4: Summarizer (versión Go)
│   └── c04_summarizer_py/ <- Desafío 4: Summarizer (versión Python)
├── common/
│   └── logging_config.py  <- Módulo de configuración de logging
├── docs/                  <- Documentación adicional (ADRs, Arquitectura)
├── Makefile               <- Archivo para automatización de comandos
├── go.mod                 <- Definición del módulo Go principal (para desafíos en Go)
├── go.sum                 <- Sumas de verificación de dependencias de Go
├── pyproject.toml         <- Configuración de Poetry (para Python)
└── README.md              <- Este archivo
```

## 💡 Navegación a los Challenges Individuales

Para evaluar cada solución, diríjase a los directorios específicos. La documentación detallada para cada desafío se encuentra en su respectivo `README.md`.

| Challenge | Título del Challenge | Carpeta | Acceder a la Documentación |
|-----------|----------------------|---------|----------------------------|
| **Challenge 1** | Minesweeper | `c01_minesweeper/` | [Ver README Detallado](challenges/c01_minesweeper/README.md) |
| **Challenge 2** | Best In Genre | `c02_best_in_genre/` | [Ver README Detallado](challenges/c02_best_in_genre/README.md) |
| **Challenge 3** | SQL Failures | `c03_sql_failures/` | [Ver README Detallado](challenges/c03_sql_failures/README.md) |
| **Challenge 4 (Go)** | Summarizer | `c04_summarizer/` | [Ver README Detallado (Go)](challenges/c04_summarizer/README.md) |
| **Challenge 4 (Python)**| Summarizer | `c04_summarizer_py/` | [Ver README Detallado (Python)](challenges/c04_summarizer_py/README.md) |

## 👤 Autor y Contacto

Si tiene alguna pregunta sobre la implementación o las decisiones de diseño, no dude en contactarme.

- **Autor:** Fabio Barón
- **LinkedIn:** [www.linkedin.com/in/fabio-baron-barrera](https://www.linkedin.com/in/fabio-baron-barrera)
- **Email:** fabiaon@gmail.com

## 📄 Licencia

Este proyecto fue desarrollado únicamente con fines **académicos y de evaluación técnica** para el proceso de selección.
