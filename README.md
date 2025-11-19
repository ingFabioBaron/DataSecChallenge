# 🚀 Solución al Mercado Libre DataSec Challenge

## 🌟 Descripción General del Proyecto

Este repositorio contiene la **implementación completa** de la prueba técnica solicitada para el **Mercado Libre DataSec Challenge**.

La solución está desarrollada en **Python 3.11.9** y organizada bajo una arquitectura de **monorepo**. Cada desafío reside en su propia carpeta bajo `challenges/`, lo que garantiza la **modularidad e independencia** de las soluciones.

El proyecto también incluye un módulo **`common/`** para albergar funcionalidades transversales, mejorando la reutilización y el mantenimiento del código.

## 🎯 Enfoque y Metodología

La solución se desarrolló priorizando la **calidad, la automatización y la mantenibilidad** del código:

- **Conformidad con PEP 8:** Adherencia a los estándares de estilo de código de Python.
- **Modularidad:** Cada reto está autocontenido y diseñado para ser ejecutable de forma independiente.
- **Gestión de Dependencias Robusta:** Utilización de **Poetry** para entornos virtuales aislados y gestión precisa de dependencias.
- **Control de Calidad:** Integración de herramientas de _linting_ como **Ruff** para el análisis estático y la detección de errores.

## 🛠️ Tecnologías y Herramientas de Desarrollo

| Categoría | Tecnología/Librería | Versión | Propósito |
|-----------|---------------------|---------|-----------|
| **Lenguaje Base** | Python | 3.11.9 | Plataforma de desarrollo principal. |
| **Gestión de Entorno** | Poetry | 2.x | Configuración y gestión de dependencias del proyecto. |
| **Base de Datos** | SQLite3 | (Estándar) | Usado en Challenge 3 para simular la base de datos de reportes de fallas. |
| **GenAI / NLP** | HuggingFace | (Depende del modelo) | Usado en Challenge 4 para consumir modelos de _Text Summarizer_ (implementado en Python, a pesar del título original del desafío). |
| **Análisis Estático** | Ruff | - | _Linting_ y chequeo de calidad de código (`make lint`). |
| **Pruebas** | pytest | - | Marco de trabajo para la ejecución de pruebas unitarias (`make test`). |

## ⚙️ Instalación y Preparación del Entorno

Este proyecto utiliza **Poetry** para una configuración de entorno consistente y reproducible.

### 1. Clonar el Repositorio

Abra su terminal y ejecute:
```bash
git clone https://github.com/ingFabioBaron/DataSecChallenge.git
cd DataSecChallenge
```

### 2. Requisitos Previos (Poetry)

Asegúrese de tener **Poetry 2.x** instalado.

### 3. Configuración e Instalación de Dependencias

Ejecute los siguientes comandos para crear el entorno virtual y resolver todas las dependencias:
```bash
poetry install
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

Si no tiene Make, puede usar **Poetry** directamente para ejecutar las tareas de desarrollo:

| Tarea                      | Comando Manual (Poetry)       | Comando con Make     |
|----------------------------|-------------------------------|-----------------------|
| Instalar dependencias      | `poetry install`              | `make install`        |
| Correr tests               | `poetry run pytest -q`        | `make test`           |
| Formatear código (Black)   | `poetry run black .`          | `make format`         |
| Ejecutar linters (Ruff)    | `poetry run ruff check .`     | `make lint`           |

#### 4.3. ⭐ Recomendación de Instalación (Windows)

Si está en Windows y desea usar Make (opción recomendada), puede instalarlo fácilmente mediante:

- **Git Bash:** (Viene incluido con la instalación estándar)
- **WSL (Ubuntu):** `sudo apt install make`
- **MSYS2:** `pacman -S make`
- **Windows (nativo):** `winget install ezwinports.make`

## 🧩 Variables de Entorno (Archivo `.env.example`)

El proyecto requiere la configuración de algunas variables de entorno para su correcta ejecución, especialmente en el **Challenge 4**. Se proporciona el archivo `.env.example` que debe ser copiado a un archivo **`.env`** y rellenado.

| Variable | Challenge | Descripción y Obligatoriedad |
|----------|-----------|------------------------------|
| **`LOG_LEVEL`** | Transversal | Nivel de logging para todo el proyecto (ej: `INFO`, `DEBUG`). |
| **`DB_PATH`** | Challenge 3 | Ruta local para el archivo de la base de datos SQLite. |
| **`HF_API_TOKEN`** | Challenge 4 | **Obligatorio.** Token de API de HuggingFace necesario para el funcionamiento del Summarizer. |
| **`HF_MODEL`** | Challenge 4 | Opcional. Permite especificar un modelo diferente para el Summarizer. |

## 🚀 Automatización de Tareas (Makefile)

El repositorio incluye un `Makefile` completo para simplificar la ejecución de las tareas de desarrollo y los desafíos individuales.

> **Recomendación:** Se recomienda enfáticamente tener **Make** instalado para una ejecución más ágil y estandarizada de las tareas comunes (`test`, `lint`, `run-chX`). Es importante notar que **todos los comandos listados pueden ser ejecutados de forma manual utilizando `poetry run ...`** si no dispone de `make`.

| Tarea | Comando Make | Descripción |
|-------|--------------|-------------|
| **Instalación** | `make install` | Instala todas las dependencias con Poetry. |
| **Pruebas** | `make test` | Ejecuta todos los tests unitarios con `pytest`. |
| **Análisis Estático** | `make lint` | Ejecuta el linter `ruff` sobre todo el código base. |
| **Ejecución C1** | `make run-ch1` | Ejecuta la solución del Challenge 1 (Minesweeper). |
| **Ejecución C2** | `make run-ch2` | Ejecuta la solución del Challenge 2 (Best In Genre). |
| **Ejecución C3** | `make run-ch3` | Ejecuta la solución del Challenge 3 (SQL Failures). |
| **Ejecución C4** | `make run-ch4` | Ejecuta las 3 modalidades del Challenge 4 (Summarizer: bullet, medium, short). |
| **Limpieza** | `make clean` | Elimina archivos temporales (`__pycache__`, `.pytest_cache`). |
| **Ayuda** | `make help` | Muestra la lista completa de comandos disponibles. |

## 📂 Estructura del Proyecto
```
DataSecChallenge/
├── challenges/
│   ├── c01_minesweeper/   <- Desafío 1: Minesweeper
│   ├── c02_best_in_genre/ <- Desafío 2: Best In Genre
│   ├── c03_sql_failures/  <- Desafío 3: SQL Failures
│   └── c04_summarizer/    <- Desafío 4: Summarizer
├── common/
│   └── logging_config.py  <- Módulo de configuración de logging
├── docs/                  <- Documentación adicional (ADRs, Arquitectura)
├── Makefile               <- Archivo para automatización de comandos
├── pyproject.toml         <- Configuración de Poetry
└── README.md              <- Este archivo
```

## 💡 Navegación a los Challenges Individuales

Para evaluar cada solución, diríjase a los directorios específicos. La documentación detallada para cada desafío se encuentra en su respectivo `README.md`.

| Challenge | Título del Challenge | Carpeta | Acceder a la Documentación |
|-----------|----------------------|---------|----------------------------|
| **Challenge 1** | Minesweeper | `c01_minesweeper/` | [Ver README Detallado](challenges/c01_minesweeper/README.md) |
| **Challenge 2** | Best In Genre | `c02_best_in_genre/` | [Ver README Detallado](challenges/c02_best_in_genre/README.md) |
| **Challenge 3** | SQL Failures | `c03_sql_failures/` | [Ver README Detallado](challenges/c03_sql_failures/README.md) |
| **Challenge 4** | Summarizer | `c04_summarizer/` | [Ver README Detallado](challenges/c04_summarizer/README.md) |

## 👤 Autor y Contacto

Si tiene alguna pregunta sobre la implementación o las decisiones de diseño, no dude en contactarme.

- **Autor:** Fabio Barón
- **LinkedIn:** [www.linkedin.com/in/fabio-baron-barrera](https://www.linkedin.com/in/fabio-baron-barrera)
- **Email:** fabiaon@gmail.com

## 📄 Licencia

Este proyecto fue desarrollado únicamente con fines **académicos y de evaluación técnica** para el proceso de selección.